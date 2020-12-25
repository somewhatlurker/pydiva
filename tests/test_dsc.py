import unittest
from os.path import join as joinpath, dirname
import json
from io import BytesIO
from pydiva import pydsc
from pydiva.pydsc_op_db import dsc_op_db, dsc_lookup_ids, dsc_lookup_names

module_dir = dirname(__file__)

with open(joinpath(module_dir, 'data', 'dsc_db.json'), 'r', encoding='utf-8') as f:
    opse_db = json.load(f)

game_info_keys = [('info_PDA', 'info_A12'), ('info_F2', 'info_F2'), ('info_FT', 'info_FT'), ('info_PSP1', 'info_PSP1'), ('info_PSP2', 'info_PSP2'), ('info_X', 'info_X'), ('info_F', 'info_f')]

class CheckDb(unittest.TestCase):
    
    # make sure the db hasn't accidentally diverged from Open PD Script Editor's
    
    def test_compare_to_opse_db(self):
        for op in dsc_op_db:
            opse_op = opse_db.get(op['name'])
            self.assertTrue(opse_op is not None)
            
            for key in game_info_keys:
                data = op.get(key[0], op.get('info_default'))
                opse_data = opse_op.get(key[1])
                
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
                data = op.get(key[0], op.get('info_default'))
                
                if data is not None and data['id'] is None:
                    self.assertEqual(data['param_cnt'], None)
    
    def test_check_none_param_cnt_matches_id(self):
        for op in dsc_op_db:
            for key in game_info_keys:
                data = op.get(key[0], op.get('info_default'))
                
                if data is not None and data['param_cnt'] is None:
                    self.assertEqual(data['id'], None)
    
    def test_check_param_info_len(self):
        for op in dsc_op_db:
            for key in game_info_keys:
                data = op.get(key[0], op.get('info_default'))
                
                if data is not None and 'param_info' in data:
                    self.assertEqual(data['param_cnt'], len(data['param_info']))


class TestDscOpInit(unittest.TestCase):
    
    def test_op_from_id(self):
        op = pydsc.DscOp.from_id('FT', 1, [39])
        self.assertEqual(op.game, 'FT')
        self.assertEqual(op.op_id, 1)
        self.assertEqual(op.op_name, 'TIME')
        self.assertEqual(op.param_values, [39])
        self.assertEqual(op.param_info, dsc_op_db[dsc_lookup_names['TIME']]['info_default']['param_info'])
    
    def test_op_from_id_auto_params(self):
        op = pydsc.DscOp.from_id('FT', 1)
        self.assertEqual(op.game, 'FT')
        self.assertEqual(op.op_id, 1)
        self.assertEqual(op.op_name, 'TIME')
        self.assertEqual(op.param_values, [0])
        self.assertEqual(op.param_info, dsc_op_db[dsc_lookup_names['TIME']]['info_default']['param_info'])
    
    def test_op_from_name(self):
        op = pydsc.DscOp.from_name('F', 'TIME', [39])
        self.assertEqual(op.game, 'F')
        self.assertEqual(op.op_id, 1)
        self.assertEqual(op.op_name, 'TIME')
        self.assertEqual(op.param_values, [39])
        self.assertEqual(op.param_info, dsc_op_db[dsc_lookup_names['TIME']]['info_default']['param_info'])
    
    def test_op_from_name_auto_params(self):
        op = pydsc.DscOp.from_name('X', 'TIME')
        self.assertEqual(op.game, 'X')
        self.assertEqual(op.op_id, 1)
        self.assertEqual(op.op_name, 'TIME')
        self.assertEqual(op.param_values, [0])
        self.assertEqual(op.param_info, dsc_op_db[dsc_lookup_names['TIME']]['info_default']['param_info'])
    
    def test_op_from_string(self):
        op = pydsc.DscOp.from_string('FT', 'MIKU_MOVE(chara=0, z= 3, x =1,y=2 )')
        self.assertEqual(op.game, 'FT')
        self.assertEqual(op.op_id, 2)
        self.assertEqual(op.op_name, 'MIKU_MOVE')
        self.assertEqual(op.param_values, [0, 1, 2, 3])
        self.assertEqual(op.param_info, dsc_op_db[dsc_lookup_names['MIKU_MOVE']]['info_default']['param_info'])
    
    def test_op_from_string_positional(self):
        op = pydsc.DscOp.from_string('FT', 'MIKU_MOVE(0, 1,2, 3)')
        self.assertEqual(op.game, 'FT')
        self.assertEqual(op.op_id, 2)
        self.assertEqual(op.op_name, 'MIKU_MOVE')
        self.assertEqual(op.param_values, [0, 1, 2, 3])
        self.assertEqual(op.param_info, dsc_op_db[dsc_lookup_names['MIKU_MOVE']]['info_default']['param_info'])
    
    def test_op_from_string_auto_params(self):
        op = pydsc.DscOp.from_string('FT', 'MIKU_MOVE( )')
        self.assertEqual(op.game, 'FT')
        self.assertEqual(op.op_id, 2)
        self.assertEqual(op.op_name, 'MIKU_MOVE')
        self.assertEqual(op.param_values, [0, 0, 0, 0])
        self.assertEqual(op.param_info, dsc_op_db[dsc_lookup_names['MIKU_MOVE']]['info_default']['param_info'])
    
    def test_op_from_string_auto_params_semicolon(self):
        op = pydsc.DscOp.from_string('FT', 'MIKU_MOVE( );')
        self.assertEqual(op.game, 'FT')
        self.assertEqual(op.op_id, 2)
        self.assertEqual(op.op_name, 'MIKU_MOVE')
        self.assertEqual(op.param_values, [0, 0, 0, 0])
        self.assertEqual(op.param_info, dsc_op_db[dsc_lookup_names['MIKU_MOVE']]['info_default']['param_info'])


class TestDscStream(unittest.TestCase):
    
    def test_aft_stream(self):
        dsc = [
            pydsc.DscOp.from_string('FT', 'TIME(0)'),
            pydsc.DscOp.from_string('FT', 'MUSIC_PLAY(0)'),
            pydsc.DscOp.from_string('FT', 'CHANGE_FIELD(1)'),
            pydsc.DscOp.from_string('FT', 'MIKU_DISP(chara=0, visible=False)'),
            pydsc.DscOp.from_string('FT', 'MIKU_MOVE(chara=0, x=1, y=2, z=3)'),
            pydsc.DscOp.from_string('FT', 'HAND_SCALE(chara=0, hand=left, scale=1220)'),
            pydsc.DscOp.from_string('FT', 'END()')
        ]
        
        with BytesIO() as s:
            pydsc.to_stream(dsc, s)
            s.seek(0)
            dsc_out = pydsc.from_stream(s)
        
        self.assertEqual(dsc, dsc_out)