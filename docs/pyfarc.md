pyfarc Documentation
====================

pyfarc supports reading and writing farc types used by Project DIVA games. (FArc, FArC, FARC)  
All features except writing encrypted Future Tone FARC format files should be supported.

## Usage
### Dictionary Representation
The main API makes use of nested python dictionaries to represent data:
```
{
    'farc_type': 'FARC',             # format-specific signature (FArc/FArC/FARC)
    'files': {                       # dictionary of contained files
        'filename': {                # keys of 'files' are filenames, values are dicts
            'data': b'file_content',
            'flags': {               # per-file flags (only for FT FARC, recommended to omit for user-supplied data)
                'encrypted': False,
                'compressed': True
            }
        }
    },
    'alignment': 16,                 # alignment of files (can be omitted)
    'flags': {                       # feature flags (only for FARC, can be omitted)
        'encrypted': False,
        'compressed': True
    },
    'format': 1                      # sub-format (only for FARC, 0=DT/F/X, 1=FT/M39)
}
```

### Reading Data
Use `pyfarc.from_stream` or `pyfarc.from_bytes` to convert raw data to the dictionary representation.  
Example:
```
with open('test.farc', 'rb') as f:
    farc_from_stream = pyfarc.from_stream(f)
    
    f.seek(0)
    farc_from_bytes = pyfarc.from_bytes(f.read())
```

`pyfarc.UnsupportedFarcTypeException` will be raised if the supplied file is not a known farc type.

Setting the argument `files_whitelist` to a list of strings will make `from_stream` and `from_bytes` return a
dictionary that only contains files with names in the whitelist. (non-matching files won't be processed to save time)


`pydiva.farc_load_helper.farc_load_helper` can be used to quickly get the content of a list of filenames from a farc.  
If not a supported farc, the original file's content will be returned as a nameless file so you can read it directly.  
Useful for easy fallback to reading already extracted files.  
Example:
```
with open('farc_or_bin?', 'rb') as f:
    farc_files = farc_load_helper(f, ['test.bin', 'test2.bin'])

if len(farc_files) == 0:
    raise Exception('Found farc but it didn\'t contain test.bin or test2.bin')

for f in farc_files:
    if f[0]:
        print ('Loading {} from farc'.format(f[0]))
    else
        print ('Loading original file directly (maybe it\'s already extracted)')

    process_file(f[1])
```


### Writing Data
Use `pyfarc.to_stream` or `pyfarc.to_bytes` to convert the dictionary representation to raw data.  
Example:
```
farcdata = {'farc_type': 'FArC', 'files': {'test': {'data': b'test'}}}
with open('test.farc', 'wb') as f:
    pyfarc.to_stream(farcdata, f)
farc_to_bytes = pyfarc.to_bytes(farcdata, no_copy=True)
```

Setting `no_copy` provides a speedup and memory usage reduction, but the input will be contaminated with internal data
created during processing. Only enable this if you won't reuse the dictionary.

`pyfarc.UnsupportedFarcTypeException` will be raised if the farc_type is unknown or used with unsupported options.


## Command Line
pyfarc also has simple command line functionality to pack/extract archives.  
Use `python -m pydiva.pyfarc` to run it.

If input is a directory, a farc archive with the same name will be created.  
If input is a file, the farc archive will be extracted to a directory with the same name.

　

## Development Info
Yep, so farc is actually four distinct formats. Fortunately they're all pretty basic.
Structs from `pydiva/pyfarc_formats.py` are probably the closest thing to documentation, but MikuMikuModel is good for
reference too.
`pydiva/pyfarc_ft_helpers.py` is worth special mention as FARC type detection and FT header encryption/decryption is
handled there rather than in a generic way. (honestly, it'd be a pain to do it generically within construct)