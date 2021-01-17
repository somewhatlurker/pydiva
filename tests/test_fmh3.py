import unittest
from os.path import join as joinpath, dirname, exists as pathexists
import json
import hashlib
from pydiva import pyfarc, pyfmh3

def files_dict_from_farc_stream(s):
    farc = pyfarc.from_stream(s)
    
    out = {}
    for fname, info in farc['files'].items():
        out[fname] = info['data']
    
    return out

def fmh_from_file(path):
    with open(path, 'rb') as f:
        return pyfmh3.from_stream(f)

module_dir = dirname(__file__)

with open(joinpath(module_dir, 'data', 'checksums.json'), 'r') as f:
    checksums = json.load(f)

with open(joinpath(module_dir, 'data', 'fontmap_ref_json.farc'), 'rb') as f:
    refdata = files_dict_from_farc_stream(f)


class TestFmhRead(unittest.TestCase):
    def test_read_aft(self):
        fmh = fmh_from_file(joinpath(module_dir, 'data', 'fontmap_aft', 'fontmap.bin'))
        self.assertEqual(fmh, json.loads(refdata['fontmap_aft.json']))
    
    def test_read_m39(self):
        fmh = fmh_from_file(joinpath(module_dir, 'data', 'fontmap_m39', 'fontmap.bin'))
        self.assertEqual(fmh, json.loads(refdata['fontmap_m39.json']))
    
    def test_read_x(self):
        fmh = fmh_from_file(joinpath(module_dir, 'data', 'fontmap_x', 'fontmap.fnm'))
        self.assertEqual(fmh, json.loads(refdata['fontmap_x.json']))
    
    if pathexists(joinpath(module_dir, '..', 'copyright!', 'script')):
        def test_read_x_cprt(self):
            fmh = fmh_from_file(joinpath(module_dir, '..', 'copyright!', 'fontmap_x.fnm'))
            self.assertEqual(fmh, json.loads(refdata['fontmap_x.json']))
            fmh = fmh_from_file(joinpath(module_dir, '..', 'copyright!', 'fontmap_X_reversed_enrs_pof.fnm'))
            self.assertEqual(fmh, json.loads(refdata['fontmap_x.json']))

class TestFmhWrite(unittest.TestCase):
    def test_write_aft(self):
        fmh = json.loads(refdata['fontmap_aft.json'])
        b = pyfmh3.to_bytes(fmh)
        c = hashlib.sha1(b).hexdigest()
        self.assertEqual(c, checksums['fontmap_aft.bin'])
    
    def test_write_m39(self):
        fmh = json.loads(refdata['fontmap_m39.json'])
        b = pyfmh3.to_bytes(fmh)
        c = hashlib.sha1(b).hexdigest()
        self.assertEqual(c, checksums['fontmap_m39.bin'])
    
    def test_write_x(self):
        fmh = json.loads(refdata['fontmap_x.json'])
        b = pyfmh3.to_bytes(fmh)
        c = hashlib.sha1(b).hexdigest()
        self.assertEqual(c, checksums['fontmap_x.fnm'])