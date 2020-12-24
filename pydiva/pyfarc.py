"""
pyfarc reader and writer for farc archives
"""

from copy import deepcopy
from io import BytesIO
from secrets import token_bytes
from os import getenv
import gzip
import zlib # gzip module's decompress doesn't handle junk at end of file
from pydiva.pyfarc_formats import _farc_types
from pydiva.pyfarc_ft_helpers import _is_FT_FARC, _decrypt_FT_FARC_header, _encrypt_FT_FARC_header

try:
    from Cryptodome.Cipher import AES
    from Cryptodome.Util.Padding import pad
    _cryptodome_installed = True
except Exception:
    _cryptodome_installed = False


class UnsupportedFarcTypeException(Exception):
    pass

def check_farc_type(t):
    """Checks if a farc type is supported and returns a remarks string. Raises UnsupportedFarcTypeException if not supported."""
    
    if not t in _farc_types:
        raise UnsupportedFarcTypeException("{} type not supported".format(t))
    
    if _farc_types[t]['encryption_type'] and not _cryptodome_installed:
        raise UnsupportedFarcTypeException("{} type only supported with Cryptodome module installed".format(t))
    
    return _farc_types[t]['remarks']


def _files_header_size_calc(files, farc_type):
    """Sums the size of the files header section for the given files and farc_type data."""
    
    size = 0
    for fname, info in files.items():
        size += len(fname) + 1
        size += farc_type['files_header_fields_size']
    return size

def _prep_files(files, alignment, farc_type, flags):
    """Gets files ready for writing by compressing them and calculating pointers."""
    
    def _compress_files(files, farc_type):
        for fname, info in files.items():
            if info['flags']['compressed']:
                data_compressed = gzip.compress(info['data'], mtime=39) # set mtime for reproducible output
                if farc_type['compression_forced'] or (len(data_compressed) < len(info['data'])):
                    info['data'] = data_compressed
                    info['flags']['compressed'] = True
                else:
                    # this is an optimisation where files that don't compress well can be stored uncompressed in some
                    # farc types -- by not replacing data, compressed and uncompressed lengths will be the same
                    info['flags']['compressed'] = False
            
            info['len_compressed'] = len(info['data'])
    
    def _encrypt_files(files, farc_type):
        for fname, info in files.items():
            if not info['flags']['encrypted']:
                continue
            
            data = info['data']
            
            if farc_type['encryption_type'] == 'DT':
                while len(data) % 16:
                    data += b'\x00'
                cipher = AES.new(b'project_diva.bin', AES.MODE_ECB)
                data = cipher.encrypt(data)
            elif farc_type['encryption_type'] == 'FT':
                data = pad(data, 16, 'pkcs7')
                if getenv('PYFARC_NULL_IV'):
                    iv = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                else:
                    iv = token_bytes(16)
                cipher = AES.new(b'\x13\x72\xD5\x7B\x6E\x9E\x31\xEB\xA2\x39\xB8\x3C\x15\x57\xC6\xBB', AES.MODE_CBC, iv=iv)
                data = iv + cipher.encrypt(data)
                
                # encrypted FT FARC "compressed" length seems to include IV and be aligned
                info['len_compressed'] = len(data)
            
            info['data'] = data
       
    def _set_files_pointers(files, alignment, farc_type, encrypted):
        pos = 8 + farc_type['fixed_header_size'] + _files_header_size_calc(files, farc_type)
        
        if encrypted and farc_type['encryption_type'] == 'FT':
            pos += 16 # leave space for header IV
            if pos % 16: pos += 16 - (pos % 16) # ensure space exists for AES
        
        for fname, info in files.items():
            if pos % alignment: pos += alignment - (pos % alignment)
            info['pointer'] = pos
            pos += len(info['data']) # don't use previously obtained length because encryption might change the data size
    
    for fname, info in files.items():
        info['len_uncompressed'] = len(info['data'])
        
        if (not 'flags' in info) or (not farc_type['has_per_file_flags']):
            info['flags'] = {}
        if not 'encrypted' in info['flags']:
            info['flags']['encrypted'] = flags.get('encrypted')
        if not 'compressed' in info['flags']:
            info['flags']['compressed'] = flags.get('compressed')
    
    if farc_type['compression_support']:
        _compress_files(files, farc_type)
    
    if farc_type['encryption_type']:
        _encrypt_files(files, farc_type)
    
    _set_files_pointers(files, alignment, farc_type, flags.get('encrypted', False))


def to_stream(data, stream, no_copy=False):
    """
    Converts a farc dictionary (formatted like the dictionary returned by from_stream) to farc data and writes it to a stream.
    
    Set no_copy to True for a speedup and memory usage reduction if you don't mind your input data being contaminated.
    """
    
    magic_str = data['farc_type']
    check_farc_type(magic_str)
    farc_type = _farc_types[magic_str]
    
    if farc_type['format_field']:
        format = data.get('format', 0)
        if format >= len(farc_type['format_field']):
            raise UnsupportedFarcTypeException('Unknown sub-format {} for {} type'.format(format, magic_str))
        
        magic_str = farc_type['format_field'][format]
        farc_type = _farc_types[magic_str]
    
    if not farc_type['write_support']:
        raise UnsupportedFarcTypeException('Writing {} type not supported'.format(magic_str))
    
    alignment = data.get('alignment', 16)
    
    flags = {'encrypted': False, 'compressed': farc_type['compression_forced']}
    if farc_type['has_flags'] and 'flags' in data:
        flags['compressed'] = data['flags'].get('compressed')
        flags['encrypted'] = data['flags'].get('encrypted')
    
    if flags['encrypted'] and not farc_type['encryption_write_support']:
        raise UnsupportedFarcTypeException('Writing {} type with encryption not supported'.format(magic_str))
    
    
    if no_copy:
        files = data['files']
    else:
        files = deepcopy(data['files'])
    _prep_files(files, alignment, farc_type, flags)
    
    if flags['encrypted'] and farc_type['encryption_type'] == 'FT':
        og_stream = stream
        stream = BytesIO()
    
    if farc_type['compression_support']:
        farc_type['struct'].build_stream(dict(
            header_size=farc_type['fixed_header_size'] + _files_header_size_calc(files, farc_type),
            flags=flags,
            entry_count=len(files),
            alignment=alignment,
            files=[dict(
                name=fname,
                pointer=info['pointer'],
                compressed_size=info['len_compressed'],
                uncompressed_size=info['len_uncompressed'],
                flags=info['flags'],
                data=info['data']
            ) for fname, info in files.items()]
        ), stream)
    else:
        farc_type['struct'].build_stream(dict(
            header_size=farc_type['fixed_header_size'] + _files_header_size_calc(files, farc_type),
            flags=flags,
            entry_count=len(files),
            alignment=alignment,
            files=[dict(
                name=fname,
                pointer=info['pointer'],
                size=info['len_uncompressed'],
                flags=info['flags'],
                data=info['data']
            ) for fname, info in files.items()]
        ), stream)
    
    if flags['encrypted'] and farc_type['encryption_type'] == 'FT':
        stream.seek(0)
        _encrypt_FT_FARC_header(stream, og_stream)
        stream.close()

def to_bytes(data, no_copy=False):
    """
    Converts a farc dictionary (formatted like the dictionary returned by from_bytes) to an in-memory bytes object containing farc data.
    
    Set no_copy to True for a speedup and memory usage reduction if you don't mind your input data being contaminated.
    """
    
    with BytesIO() as s:
        to_stream(data, s, no_copy)
        return s.getvalue()


def _parsed_to_dict(farcdata, farc_type, files_whitelist=None):
    """
    Converts the raw construct data to our standard dictionary format.
    Setting files_whitelist will return a dictionary that only contains files with names in the whitelist.
    """
    
    files = {}
    
    if farc_type['has_flags']:
        flags = farcdata['flags']
        
        for f in farcdata['files']:
            if files_whitelist and not f['name'] in files_whitelist:
                continue
            
            data = f['data']
            
            if farc_type['has_per_file_flags']:
                flags = f['flags']
            
            if flags.get('encrypted'):
                if farc_type['encryption_type'] == 'DT':
                    cipher = AES.new(b'project_diva.bin', AES.MODE_ECB)
                    data = cipher.decrypt(data)
                elif farc_type['encryption_type'] == 'FT':
                    cipher = AES.new(b'\x13\x72\xD5\x7B\x6E\x9E\x31\xEB\xA2\x39\xB8\x3C\x15\x57\xC6\xBB', AES.MODE_CBC, iv=data[:16])
                    data = cipher.decrypt(data[16:])
            
            if flags.get('compressed') and (farc_type['compression_forced'] or (f['uncompressed_size'] != f['compressed_size'])):
                data = zlib.decompress(data, wbits=16+zlib.MAX_WBITS, bufsize=f['uncompressed_size'])
            else:
                if flags.get('encrypted'): # if encrypted but not compressed, need to strip padding manually
                    data = data[:f['uncompressed_size']]
            
            files[f['name']] = {'data': data}
            if farc_type['has_per_file_flags']:
                files[f['name']]['flags'] = dict(flags)
                del files[f['name']]['flags']['_io']
    
    elif farc_type['compression_support']:
        for f in farcdata['files']:
            if files_whitelist and not f['name'] in files_whitelist:
                continue
            
            data = f['data']
            
            if farc_type['compression_forced'] or (f['uncompressed_size'] != f['compressed_size']):
                data = zlib.decompress(data, wbits=16+zlib.MAX_WBITS, bufsize=f['uncompressed_size'])
            
            files[f['name']] = {'data': data}
    
    else:
        for f in farcdata['files']:
            if files_whitelist and not f['name'] in files_whitelist:
                continue
            
            data = f['data']
            files[f['name']] = {'data': data}
    
    out = {'farc_type': farcdata['signature'].decode('ascii'), 'files': files, 'alignment': farcdata['alignment']}
    if farc_type['has_flags']:
        out['flags'] = dict(farcdata['flags'])
        del out['flags']['_io']
    if farc_type['format_field']:
        out['format'] = farcdata['format']
    return out

def from_stream(s, files_whitelist=None):
    """
    Converts farc data from a stream to a dictionary.
    Setting files_whitelist will return a dictionary that only contains files with names in the whitelist.
    """
    
    pos = s.tell()
    magic_str = s.read(4).decode('ascii')
    s.seek(pos)
    check_farc_type(magic_str)
    farc_type = _farc_types[magic_str]
    
    close_ft_stream = False
    if _is_FT_FARC(s):
        farc_type = _farc_types['FARC_FT']
        decrypt_stream = _decrypt_FT_FARC_header(s)
        if decrypt_stream:
            s = decrypt_stream
            close_ft_stream = True
    
    farcdata = farc_type['struct'].parse_stream(s)
    
    if close_ft_stream: # explicitly close BytesIO from FT decryption if one was opened
        s.close()
    
    return _parsed_to_dict(farcdata, farc_type, files_whitelist)

def from_bytes(b, files_whitelist=None):
    """
    Converts farc data from bytes to a dictionary.
    Setting files_whitelist will return a dictionary that only contains files with names in the whitelist.
    """
    
    with BytesIO(b) as s:
        return from_stream(s, files_whitelist)


#test_farc = {'farc_type': 'FArc', 'files': {'aaa': {'data': b'test1'}, 'bbb': {'data': b'test2'}, 'ccc': {'data': b'aaaaaaaaaaaaaaaaaaaaaaaa'}}, 'alignment': 16}
#test_farc = {'farc_type': 'FArC', 'files': {'aaa': {'data': b'test1'}, 'bbb': {'data': b'test2'}, 'ccc': {'data': b'aaaaaaaaaaaaaaaaaaaaaaaa'}}, 'alignment': 8}
#test_farc = {'farc_type': 'FARC', 'files': {'aaa': {'data': b'test1'}, 'bbb': {'data': b'test2'}, 'ccc': {'data': b'aaaaaaaaaaaaaaaaaaaaaaaa'}}, 'alignment': 4}
#test_farc = {'farc_type': 'FARC', 'files': {'aaa': {'data': b'test1'}, 'bbb': {'data': b'test2'}, 'ccc': {'data': b'aaaaaaaaaaaaaaaaaaaaaaaa'}}, 'alignment': 32, 'flags': {'encrypted': True}}
#test_farc = {'farc_type': 'FARC', 'files': {'aaa': {'data': b'test1'}, 'bbb': {'data': b'test2'}, 'ccc': {'data': b'aaaaaaaaaaaaaaaaaaaaaaaa'}}, 'flags': {'compressed': True}}
#test_farc = {'farc_type': 'FARC', 'files': {'aaa': {'data': b'test1'}, 'bbb': {'data': b'test2'}, 'ccc': {'data': b'aaaaaaaaaaaaaaaaaaaaaaaa'}}, 'flags': {'encrypted': True, 'compressed': True}}
#test_farc = {'farc_type': 'FARC', 'files': {'aaa': {'data': b'test1'}, 'bbb': {'data': b'test2'}, 'ccc': {'data': b'aaaaaaaaaaaaaaaaaaaaaaaa'}}, 'alignment': 8, 'format': 1}
#test_farc = {'farc_type': 'FARC', 'files': {'aaa': {'data': b'test1'}, 'bbb': {'data': b'test2'}, 'ccc': {'data': b'aaaaaaaaaaaaaaaaaaaaaaaa'}}, 'alignment': 16, 'flags': {'encrypted': True}, 'format': 1}
#test_farc = {'farc_type': 'FARC', 'files': {'aaa': {'data': b'test1'}, 'bbb': {'data': b'test2'}, 'ccc': {'data': b'aaaaaaaaaaaaaaaaaaaaaaaa'}}, 'flags': {'compressed': True}, 'format': 1}
#test_farc = {'farc_type': 'FARC', 'files': {'aaa': {'data': b'test1'}, 'bbb': {'data': b'test2'}, 'ccc': {'data': b'aaaaaaaaaaaaaaaaaaaaaaaa'}}, 'flags': {'encrypted': True, 'compressed': True}, 'format': 1}
#test_farc = {'farc_type': 'FARC', 'files': {'aaa': {'data': b'test1'}, 'bbb': {'data': b'test2', 'flags': {'encrypted': True}}, 'ccc': {'data': b'aaaaaaaaaaaaaaaaaaaaaaaa', 'flags': {'encrypted': True, 'compressed': True}}}, 'format': 1}
#print (test_farc)

#test_bytes = to_bytes(test_farc)
#print (test_bytes)
#print (from_bytes(test_bytes))

#with open('test.farc', 'wb') as f:
#    to_stream(test_farc, f, alignment=16)
#with open('test.farc', 'rb') as f:
#    print (from_stream(f))

#with open('shader_amd.farc', 'rb') as f:
#    shaderfarc = from_stream(f)
#with open('shader_amd_out.farc', 'wb') as f:
#    to_stream(shaderfarc, f, alignment=16, no_copy=True)

#with open('shader_amd_compressed.farc', 'rb') as f:
#    shaderfarc = from_stream(f)
#with open('shader_amd_out_compressed.farc', 'wb') as f:
#    to_stream(shaderfarc, f, alignment=1, no_copy=True)

#with open('fontmap.farc', 'rb') as f:
#    fontmapfarc = from_stream(f)
#with open('fontmap_out.farc', 'wb') as f:
#    to_stream(fontmapfarc, f, alignment=1, no_copy=True)


def _main(args):
    """main func for command line"""
    
    from os.path import dirname, exists as pathexists, isfile, splitext, join as joinpath, basename
    from os import listdir, makedirs, remove as removefile, environ
    
    if not args.input:
        if not args.silent: print ('No input specified.')
        exit(1)

    if not pathexists(args.input):
        if not args.silent: print ('Can\'t find file or directory "{}"'.format(args.input))
        exit(1)
    
    if isfile(args.input):
        def clean_dir(d):
            files = listdir(d)
            for f in files:
                removefile(joinpath(d, f))
        
        if not args.silent: print ('Extracting "{}" to directory'.format(args.input))
        
        with open(args.input, 'rb') as f:
            farc = from_stream(f)
        
        out_dir = args.input
        while '.' in basename(out_dir):
            out_dir = splitext(out_dir)[0]
        
        if pathexists(out_dir):
            if not args.force:
                if not args.silent: print ('"{}" already exists. Use -f/--force to overwrite it.'.format(out_dir))
                exit(1)
            if isfile(out_dir):
                if not args.silent: print ('Can\'t output because "{}" is a file, not a directory.'.format(out_dir))
                exit(1)
            clean_dir(out_dir)
        else:
            makedirs(out_dir)
        
        for fname, info in farc['files'].items():
            with open(joinpath(out_dir, fname), 'wb') as f:
                f.write(info['data'])
            
    else:
        if not args.silent: print ('Building farc from directory "{}"'.format(args.input))
        
        farc = {
            'farc_type': 'FARC' if args.type == 'FARC_FT' else args.type,
            'format': 1 if args.type == 'FARC_FT' else 0,
            'alignment': int(args.alignment),
            'flags': {
                'encrypted': args.encrypt,
                'compressed': args.compress
            },
            'files': {}
        }
        
        for fname in listdir(args.input):
            with open(joinpath(args.input, fname), 'rb') as f: 
                farc['files'][fname] = {'data': f.read()}
        
        out_path = args.input
        if out_path[-1] in ['/', '\\']:
            out_path = out_path[:-1]
        
        out_path += '.farc'
        
        if pathexists(out_path):
            if not args.force:
                if not args.silent: print ('"{}" already exists. Use -f/--force to overwrite it.'.format(out_path))
                exit(1)
            if not isfile(out_path):
                if not args.silent: print ('Can\'t output because "{}" is a directory, not a file.'.format(out_path))
                exit(1)
        
        if args.null_iv:
            environ['PYFARC_NULL_IV'] = '1'
        elif 'PYFARC_NULL_IV' in environ:
            del environ['PYFARC_NULL_IV']
        
        with open(out_path, 'wb') as f:
            to_stream(farc, f)


if __name__ == '__main__':
    from os.path import dirname, exists as pathexists, isfile, splitext, join as joinpath, basename
    from os import listdir, makedirs, remove as removefile, environ
    import argparse
    
    def get_args():
        parser = argparse.ArgumentParser(description='pyfarc')
        
        parser.add_argument('-t', '--type', default='FArC', choices=['FArc', 'FArC', 'FARC', 'FARC_FT'], help='type of farc')
        parser.add_argument('-c', '--compress', action='store_true', help='compress output (only for FARC, FARC_FT types)')
        parser.add_argument('-e', '--encrypt', action='store_true', help='encrypt output (only for FARC, FARC_FT types)')
        parser.add_argument('-a', '--alignment', default='16', help='output farc alignment')
        parser.add_argument('--null_iv', action='store_true', help='use null encryption IVs (only for encrypted FARC_FT)')
        parser.add_argument('-f', '--force', action='store_true', help='force overwrite existing files/directories')
        parser.add_argument('-s', '--silent', action='store_true', help='disable command line output')
        parser.add_argument('input', default=None, help='input farc to extract or directory to archive')

        return parser.parse_args()

    _main(get_args())
    
