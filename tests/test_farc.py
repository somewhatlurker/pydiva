import unittest
from os import listdir, environ
from os.path import join as joinpath, dirname
import json
import hashlib
from collections import namedtuple
from pydiva import pyfarc
from pydiva.farc_load_helper import farc_load_helper

environ['PYFARC_NULL_IV'] = '1'

cli_args = namedtuple('args', ['type', 'compress', 'encrypt', 'alignment', 'null_iv', 'force', 'silent', 'input'])

def files_from_dir(path):
    """Returns list of (filename, bytes) tuples containing all files in path."""
    
    out = []
    for fname in listdir(path):
        with open(joinpath(path, fname), 'rb') as f: 
            out += [(fname, f.read())]
    
    return sorted(out, key=lambda f: f[0])

def files_from_farc_bytes(b):
    farc = pyfarc.from_bytes(b)
    
    out = []
    for fname, info in farc['files'].items():
        out += [(fname, info['data'])]
    
    return sorted(out, key=lambda f: f[0])

def farc_bytes_from_files(files, farc_type, alignment=16, compress=True, encrypt=True):
    farc = {
        'farc_type': 'FARC' if farc_type == 'FARC_FT' else farc_type,
        'format': 1 if farc_type == 'FARC_FT' else 0,
        'alignment': alignment,
        'flags': {
            'encrypted': encrypt,
            'compressed': compress
        },
        'files': {}
    }
    
    for fname, data in files:
        farc['files'][fname] = {'data': data}
    
    return pyfarc.to_bytes(farc, no_copy=True)

module_dir = dirname(__file__)

with open(joinpath(module_dir, 'data', 'checksums.json'), 'r') as f:
    checksums = json.load(f)

#for f, c in checksums.items():
#    checksums[f] = bytes.fromhex(c)


customdata = files_from_dir(joinpath(module_dir, 'data', 'customdata'))


class TestFarcPacking(unittest.TestCase):
    
    # customdata tests ensure that archiving files, then unarchiving the results works correctly
    # (or at least with no regressions)
    
    def test_customdata_FArc(self):
        b = farc_bytes_from_files(customdata, 'FArc', 16)
        c = hashlib.sha1(b).hexdigest()
        self.assertEqual(c, checksums['customdata.FArc'])
        f = files_from_farc_bytes(b)
        self.assertEqual(f, customdata)
    
    def test_customdata_FArC(self):
        b = farc_bytes_from_files(customdata, 'FArC', 16)
        c = hashlib.sha1(b).hexdigest()
        self.assertEqual(c, checksums['customdata.FArC'])
        f = files_from_farc_bytes(b)
        self.assertEqual(f, customdata)
    
    def test_customdata_FARC(self):
        b = farc_bytes_from_files(customdata, 'FARC', 16, False, False)
        c = hashlib.sha1(b).hexdigest()
        self.assertEqual(c, checksums['customdata.FARC'])
        f = files_from_farc_bytes(b)
        self.assertEqual(f, customdata)
    
    def test_customdata_FARC_c_e(self):
        b = farc_bytes_from_files(customdata, 'FARC', 16, True, True)
        c = hashlib.sha1(b).hexdigest()
        self.assertEqual(c, checksums['customdata_c_e.FARC'])
        f = files_from_farc_bytes(b)
        self.assertEqual(f, customdata)
    
    def test_customdata_FARC_FT(self):
        b = farc_bytes_from_files(customdata, 'FARC_FT', 16, False, False)
        c = hashlib.sha1(b).hexdigest()
        self.assertEqual(c, checksums['customdata.FARC_FT'])
        f = files_from_farc_bytes(b)
        self.assertEqual(f, customdata)
    
    def test_customdata_FARC_FT_c_e(self):
        b = farc_bytes_from_files(customdata, 'FARC_FT', 16, True, True)
        c = hashlib.sha1(b).hexdigest()
        self.assertEqual(c, checksums['customdata_c_e.FARC_FT'])
        f = files_from_farc_bytes(b)
        self.assertEqual(f, customdata)
    
    # fontmap tests are pretty much like customdata tests, but compare against known-good files that games can read
    
    def test_fontmap_aft(self):
        file = files_from_dir(joinpath(module_dir, 'data', 'fontmap_aft'))
        b = farc_bytes_from_files(file, 'FArC', 1) # accidentally generated this with alignment 1
        c = hashlib.sha1(b).hexdigest()
        self.assertEqual(c, checksums['fontmap_aft.farc'])
        f = files_from_farc_bytes(b)
        self.assertEqual(f, file)
    
    def test_fontmap_m39(self):
        file = files_from_dir(joinpath(module_dir, 'data', 'fontmap_m39'))
        b = farc_bytes_from_files(file, 'FARC_FT', 16, True, True)
        c = hashlib.sha1(b).hexdigest()
        self.assertEqual(c, checksums['fontmap_m39.farc'])
        f = files_from_farc_bytes(b)
        self.assertEqual(f, file)
    
    def test_fontmap_x(self):
        file = files_from_dir(joinpath(module_dir, 'data', 'fontmap_x'))
        b = farc_bytes_from_files(file, 'FARC', 16, True, True)
        c = hashlib.sha1(b).hexdigest()
        self.assertEqual(c, checksums['fontmap_x.farc'])
        f = files_from_farc_bytes(b)
        self.assertEqual(f, file)


class TestFarcHelper(unittest.TestCase):
    
    def test_farc_helper_success(self):
        dir_file = files_from_dir(joinpath(module_dir, 'data', 'fontmap_aft'))
        with open(joinpath(module_dir, 'data', 'fontmap_aft.farc'), 'rb') as f:
            farc_file = farc_load_helper(f, ['fontmap.bin'])
        self.assertEqual(farc_file, dir_file)
    
    def test_farc_helper_fail_missing_file(self):
        with open(joinpath(module_dir, 'data', 'fontmap_aft.farc'), 'rb') as f:
            farc_file = farc_load_helper(f, ['dummy.bin'])
        self.assertEqual(farc_file, [])
    
    def test_farc_helper_fail_not_farc(self):
        with open(joinpath(module_dir, 'data', 'files.txt'), 'rb') as f:
            farc_file = farc_load_helper(f, ['dummy.bin'])
            f.seek(0)
            original_bytes = f.read()
        self.assertEqual(farc_file, [(None, original_bytes)])


class TestFarcCli(unittest.TestCase):
    
    def test_pack_basic(self):
        a = cli_args(type='FARC_FT', compress=False, encrypt=False, alignment='16', null_iv=True, force=True, silent=True, input=joinpath(module_dir, 'data', 'cli_pack'))
        pyfarc._main(a)
        with open(joinpath(module_dir, 'data', 'cli_pack.farc'), 'rb') as f:
            b = f.read()
        c = hashlib.sha1(b).hexdigest()
        self.assertEqual(c, checksums['cli_pack.farc'])
    
    def test_pack_c_e(self):
        a = cli_args(type='FARC_FT', compress=True, encrypt=True, alignment='16', null_iv=True, force=True, silent=True, input=joinpath(module_dir, 'data', 'cli_pack_c_e'))
        pyfarc._main(a)
        with open(joinpath(module_dir, 'data', 'cli_pack_c_e.farc'), 'rb') as f:
            b = f.read()
        c = hashlib.sha1(b).hexdigest()
        self.assertEqual(c, checksums['cli_pack_c_e.farc'])
    
    def test_unpack(self):
        a = cli_args(type='FArC', compress=False, encrypt=False, alignment='16', null_iv=False, force=True, silent=True, input=joinpath(module_dir, 'data', 'cli_unpack.farc'))
        pyfarc._main(a)
        with open(joinpath(module_dir, 'data', 'cli_unpack', 'fontmap.bin'), 'rb') as f:
            b = f.read()
        c = hashlib.sha1(b).hexdigest()
        self.assertEqual(c, checksums['fontmap_aft.bin'])