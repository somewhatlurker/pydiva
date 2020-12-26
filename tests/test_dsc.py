import unittest
from os.path import join as joinpath, dirname
import json
from io import BytesIO
from itertools import combinations
from pydiva import pydsc
from pydiva.pydsc_op_db import dsc_op_db, dsc_lookup_ids, dsc_lookup_names

module_dir = dirname(__file__)

with open(joinpath(module_dir, 'data', 'dsc_db.json'), 'r', encoding='utf-8') as f:
    opse_db = json.load(f)

game_info_keys = [('info_PDA12', 'info_A12'), ('info_F2', 'info_F2'), ('info_FT', 'info_FT'), ('info_PSP1', 'info_PSP1'), ('info_PSP2', 'info_PSP2'), ('info_X', 'info_X'), ('info_F', 'info_f')]
hand_scale_enum = dsc_op_db[dsc_lookup_names['HAND_SCALE']]['info_FT']['param_info'][1]['type']

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
    
    def test_check_param_info_names_unique(self):
        for op in dsc_op_db:
            for key in game_info_keys:
                data = op.get(key[0], op.get('info_default'))
                
                if data is not None and 'param_info' in data:
                    for c in combinations(data['param_info'], 2):
                        if c[0] == None or c[1] == None:
                            continue
                        self.assertNotEqual(c[0]['name'], c[1]['name'])


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
    
    def test_op_from_id_params_enum(self):
        op = pydsc.DscOp.from_id('FT', 87, [0, 'right', 1000])
        self.assertEqual(op.game, 'FT')
        self.assertEqual(op.op_id, 87)
        self.assertEqual(op.op_name, 'HAND_SCALE')
        self.assertEqual(op.param_values, [0, hand_scale_enum('right'), 1000])
        self.assertEqual(op.param_info, dsc_op_db[dsc_lookup_names['HAND_SCALE']]['info_FT']['param_info'])
    
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
    
    def test_op_from_name_params_enum(self):
        op = pydsc.DscOp.from_name('FT', 'HAND_SCALE', [0, 'right', 1000])
        self.assertEqual(op.game, 'FT')
        self.assertEqual(op.op_id, 87)
        self.assertEqual(op.op_name, 'HAND_SCALE')
        self.assertEqual(op.param_values, [0, hand_scale_enum('right'), 1000])
        self.assertEqual(op.param_info, dsc_op_db[dsc_lookup_names['HAND_SCALE']]['info_FT']['param_info'])
    
    def test_op_from_string(self):
        op = pydsc.DscOp.from_string('FT', 'MIKU_MOVE(chara=0, z= 3, x =1,y=2 )')
        self.assertEqual(op.game, 'FT')
        self.assertEqual(op.op_id, 2)
        self.assertEqual(op.op_name, 'MIKU_MOVE')
        self.assertEqual(op.param_values, [0, 1, 2, 3])
        self.assertEqual(op.param_info, dsc_op_db[dsc_lookup_names['MIKU_MOVE']]['info_default']['param_info'])
    
    def test_op_from_string_sparse(self):
        op = pydsc.DscOp.from_string('FT', 'MIKU_MOVE(chara=1, z=3)')
        self.assertEqual(op.game, 'FT')
        self.assertEqual(op.op_id, 2)
        self.assertEqual(op.op_name, 'MIKU_MOVE')
        self.assertEqual(op.param_values, [1, 0, 0, 3])
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
    
    def test_op_from_string_params_enum(self):
        op = pydsc.DscOp.from_string('FT', 'HAND_SCALE(0, hand=right, 1000)')
        self.assertEqual(op.game, 'FT')
        self.assertEqual(op.op_id, 87)
        self.assertEqual(op.op_name, 'HAND_SCALE')
        self.assertEqual(op.param_values, [0, hand_scale_enum('right'), 1000])
        self.assertEqual(op.param_info, dsc_op_db[dsc_lookup_names['HAND_SCALE']]['info_FT']['param_info'])
    
    def test_params_enum_from_int(self):
        op = pydsc.DscOp.from_id('FT', 87, [0, 1, 1000])
        self.assertEqual(op.param_values[1], hand_scale_enum('right'))
    
    def test_params_enum_from_instance(self):
        op = pydsc.DscOp.from_id('FT', 87, [0, hand_scale_enum('right'), 1000])
        self.assertEqual(op.param_values[1], hand_scale_enum('right'))
    
    def test_params_enum_compare_instance(self):
        op = pydsc.DscOp.from_id('FT', 87, [0, hand_scale_enum('right'), 1000])
        self.assertEqual(op.param_values[1], hand_scale_enum('right'))
    
    def test_params_enum_compare_string(self):
        op = pydsc.DscOp.from_id('FT', 87, [0, hand_scale_enum('right'), 1000])
        self.assertEqual(op.param_values[1], 'right')
    
    def test_params_enum_compare_int(self):
        op = pydsc.DscOp.from_id('FT', 87, [0, hand_scale_enum('right'), 1000])
        self.assertEqual(op.param_values[1], 1)
    
    def test_params_bool(self):
        op = pydsc.DscOp.from_name('FT', 'MIKU_DISP', [0, True])
        self.assertTrue(op.param_values[1])
        op = pydsc.DscOp.from_name('FT', 'MIKU_DISP', [0, 1])
        self.assertTrue(op.param_values[1])
        op = pydsc.DscOp.from_name('FT', 'MIKU_DISP', [0, 't'])
        self.assertTrue(op.param_values[1])
        op = pydsc.DscOp.from_name('FT', 'MIKU_DISP', [0, 'TRUE'])
        self.assertTrue(op.param_values[1])
        op = pydsc.DscOp.from_name('FT', 'MIKU_DISP', [0, False])
        self.assertFalse(op.param_values[1])
        op = pydsc.DscOp.from_name('FT', 'MIKU_DISP', [0, 0])
        self.assertFalse(op.param_values[1])
        op = pydsc.DscOp.from_name('FT', 'MIKU_DISP', [0, 'f'])
        self.assertFalse(op.param_values[1])
        op = pydsc.DscOp.from_name('FT', 'MIKU_DISP', [0, 'false'])
        self.assertFalse(op.param_values[1])


class TestDscStream(unittest.TestCase):
    
    def test_ft_stream(self):
        dsc = [
            pydsc.DscOp.from_string('FT', 'TIME(0)'),
            pydsc.DscOp.from_string('FT', 'MUSIC_PLAY()'),
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


class TestDscString(unittest.TestCase):
    
    def test_ft_string(self):
        strings = [
            'TIME(0);',
            '  MUSIC_PLAY();',
            '  CHANGE_FIELD(1);',
            '  MIKU_DISP(chara=0, visible=False);',
            '  MIKU_MOVE(chara=0, x=1, y=2, z=3);',
            '  HAND_SCALE(chara=0, hand=left, scale=1220);',
            '  MIKU_DISP(chara=0, visible=True);',
            '  TARGET(type=tri_hold, pos_x=69, pos_y=420, angle=39, dist=1, amp=2, freq=3);',
            'PV_BRANCH_MODE(normal);',
            '    CHANGE_FIELD(2);',
            '  TIME(1);',
            '    CHANGE_FIELD(3);',
            'PV_BRANCH_MODE(success);',
            '    CHANGE_FIELD(2);',
            '  TIME(1);',
            '    CHANGE_FIELD(1);',
            'PV_BRANCH_MODE(none);',
            '  CHANGE_FIELD(4);',
            'TIME(1);',
            '  CHANGE_FIELD(5);',
            '  END();'
        ]
        strings_compat = [
            'TIME(0);',
            'MUSIC_PLAY();',
            'CHANGE_FIELD(1);',
            'MIKU_DISP(0, 0);',
            'MIKU_MOVE(0, 1, 2, 3);',
            'HAND_SCALE(0, 0, 1220);',
            'MIKU_DISP(0, 1);',
            'TARGET(4, 69, 420, 39, 1, 2, 3);',
            'PV_BRANCH_MODE(1);',
            'CHANGE_FIELD(2);',
            'TIME(1);',
            'CHANGE_FIELD(3);',
            'PV_BRANCH_MODE(2);',
            'CHANGE_FIELD(2);',
            'TIME(1);',
            'CHANGE_FIELD(1);',
            'PV_BRANCH_MODE(0);',
            'CHANGE_FIELD(4);',
            'TIME(1);',
            'CHANGE_FIELD(5);',
            'END();'
        ]
        
        dsc = [pydsc.DscOp.from_string('FT', s) for s in strings]
        
        self.maxDiff = None
        self.assertEqual(pydsc.dsc_to_string(dsc, indent=2), '\n'.join(strings))
        self.assertEqual(pydsc.dsc_to_string(dsc, compat_mode=True, indent=0), '\n'.join(strings_compat))