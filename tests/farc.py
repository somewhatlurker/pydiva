import unittest
from os import listdir, environ
from os.path import join as joinpath
import json
import hashlib
from pydiva import pyfarc

environ['PYFARC_NULL_IV'] = '1'

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


with open('data/checksums.json', 'r') as f:
    checksums = json.load(f)

#for f, c in checksums.items():
#    checksums[f] = bytes.fromhex(c)


customdata = files_from_dir('data/customdata')


class TestFarcPacking(unittest.TestCase):
    
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
    