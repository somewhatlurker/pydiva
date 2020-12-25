import unittest
from os.path import join as joinpath, dirname
import json
from pydiva.pydsc_op_db import dsc_op_db

module_dir = dirname(__file__)

with open(joinpath(module_dir, 'data', 'dsc_db.json'), 'r', encoding='utf-8') as f:
    opse_db = json.load(f)

game_info_keys = ['info_A12', 'info_F2', 'info_FT', 'info_PSP1', 'info_PSP2', 'info_X', 'info_f']

class CheckDb(unittest.TestCase):
    
    # make sure the db hasn't accidentally diverged from Open PD Script Editor's
    
    def test_compare_to_opse_db(self):
        for op in dsc_op_db:
            opse_op = opse_db.get(op['name'])
            self.assertTrue(opse_op is not None)
            
            for key in game_info_keys:
                data = op.get(key, op.get('info_default'))
                opse_data = opse_op.get(key)
                
                if data is None or data['id'] is None:
                    self.assertEqual(opse_data, None)
                else:
                    self.assertEqual(data['id'], opse_data['id'])
                    self.assertEqual(data['param_cnt'], opse_data['len'])
    
    def test_check_missing_ops(self):
        expected_ops = list(opse_db.keys())
        for op in dsc_op_db:
            expected_ops.remove(op['name'])
        
        self.assertEqual(expected_ops, [])
    
    def test_check_none_id_matches_params_cnt(self):
        for op in dsc_op_db:
            for key in game_info_keys:
                data = op.get(key, op.get('info_default'))
                
                if data is not None and data['id'] is None:
                    self.assertEqual(data['param_cnt'], None)