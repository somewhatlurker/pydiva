import unittest
from os import listdir
from os.path import join as joinpath, dirname, exists as pathexists
import json
from io import BytesIO
from itertools import combinations
from pydiva import pydsc
from pydiva.pydsc_op_db import dsc_op_db, dsc_lookup_ids, dsc_lookup_names
from pydiva.pydsc_util import annotate_string
from pydiva.util.stringenum import StringEnum

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
                    self.assertNotEqual(opse_data, None)
                    self.assertEqual(data['id'], opse_data['id'])
                    self.assertEqual(data['param_cnt'], opse_data['len'])
    
    def test_check_missing_ops(self):
        expected_ops = list(opse_db.keys())
        for op in dsc_op_db:
            self.assertTrue(op['name'] in expected_ops)
            expected_ops.remove(op['name'])
        
        self.assertEqual(expected_ops, [])
    
    # and some basic integrity checks on expected states of information
    
    def test_check_name_uppercase(self):
        for op in dsc_op_db:
            self.assertEqual(op['name'], op['name'].upper())
    
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
    
    def test_check_param_info_missing_fields(self):
        for op in dsc_op_db:
            for key in game_info_keys:
                data = op.get(key[0], op.get('info_default'))
                
                if data is not None and 'param_info' in data:
                    for p in data['param_info']:
                        if not p:
                            continue
                        self.assertTrue('name' in p)
                        self.assertTrue('desc' in p)
                        self.assertTrue('type' in p)
                        self.assertTrue('required' in p)
                        if not p['required']:
                            self.assertTrue('default' in p)
                        if 'default' in p:
                            self.assertFalse(p['required'])
    
    def test_check_param_info_names_unique(self):
        for op in dsc_op_db:
            for key in game_info_keys:
                data = op.get(key[0], op.get('info_default'))
                
                if data is not None and 'param_info' in data:
                    for c in combinations(data['param_info'], 2):
                        if c[0] == None or c[1] == None:
                            continue
                        self.assertNotEqual(c[0]['name'], c[1]['name'])
    
    def test_check_param_info_names_lowercase(self):
        for op in dsc_op_db:
            for key in game_info_keys:
                data = op.get(key[0], op.get('info_default'))
                
                if data is not None and 'param_info' in data:
                    for c in data['param_info']:
                        if c:
                            self.assertEqual(c['name'], c['name'].lower())
    
    def test_enum_choices_access(self):
        for op in dsc_op_db:
            for key in game_info_keys:
                data = op.get(key[0], op.get('info_default'))
                
                if data is not None and 'param_info' in data:
                    for p in data['param_info']:
                        if not p or not issubclass(p['type'], StringEnum):
                            continue
                        
                        self.assertTrue(p['type'].choices)


class TestDscOpInit(unittest.TestCase):
    
    # testing of various DscOp initialisation methods
    
    def test_op_from_id(self):
        op = pydsc.DscOp.from_id('FT', 1, [39])
        self.assertEqual(op.game, 'FT')
        self.assertEqual(op.op_id, 1)
        self.assertEqual(op.op_name, 'TIME')
        self.assertEqual(op.param_values, [39])
        self.assertEqual(op.param_info, dsc_op_db[dsc_lookup_names['TIME']]['info_default']['param_info'])
    
    def test_op_from_id_auto_params(self):
        op = pydsc.DscOp.from_id('FT', 24, [1])
        self.assertEqual(op.game, 'FT')
        self.assertEqual(op.op_id, 24)
        self.assertEqual(op.op_name, 'LYRIC')
        self.assertEqual(op.param_values, [1, -1])
        self.assertEqual(op.param_info, dsc_op_db[dsc_lookup_names['LYRIC']]['info_default']['param_info'])
    
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
    
    def test_op_from_name_lowercase(self):
        op = pydsc.DscOp.from_name('F', 'time', [39])
        self.assertEqual(op.game, 'F')
        self.assertEqual(op.op_id, 1)
        self.assertEqual(op.op_name, 'TIME')
        self.assertEqual(op.param_values, [39])
        self.assertEqual(op.param_info, dsc_op_db[dsc_lookup_names['TIME']]['info_default']['param_info'])
    
    def test_op_from_name_auto_params(self):
        op = pydsc.DscOp.from_name('X', 'LYRIC', [1])
        self.assertEqual(op.game, 'X')
        self.assertEqual(op.op_id, 24)
        self.assertEqual(op.op_name, 'LYRIC')
        self.assertEqual(op.param_values, [1, -1])
        self.assertEqual(op.param_info, dsc_op_db[dsc_lookup_names['LYRIC']]['info_default']['param_info'])
    
    def test_op_from_name_params_enum(self):
        op = pydsc.DscOp.from_name('FT', 'HAND_SCALE', [0, 'right', 1000])
        self.assertEqual(op.game, 'FT')
        self.assertEqual(op.op_id, 87)
        self.assertEqual(op.op_name, 'HAND_SCALE')
        self.assertEqual(op.param_values, [0, hand_scale_enum('right'), 1000])
        self.assertEqual(op.param_info, dsc_op_db[dsc_lookup_names['HAND_SCALE']]['info_FT']['param_info'])
    
    def test_op_from_name_none_id(self):
        try:
            op = pydsc.DscOp.from_name('PDA12', 'CHARA_HEIGHT_ADJUST', [])
            self.assertTrue(False) # should fail with UnknownDscOpException
        except pydsc.UnknownDscOpException:
            pass
    
    def test_op_from_string(self):
        op = pydsc.DscOp.from_string('FT', 'MIKU_MOVE(chara=0, z= i3, x =i1,y=i2 )')
        self.assertEqual(op.game, 'FT')
        self.assertEqual(op.op_id, 2)
        self.assertEqual(op.op_name, 'MIKU_MOVE')
        self.assertEqual(op.param_values, [0, 1, 2, 3])
        self.assertEqual(op.param_info, dsc_op_db[dsc_lookup_names['MIKU_MOVE']]['info_default']['param_info'])
    
    def test_op_from_string_mixed_case(self):
        op = pydsc.DscOp.from_string('FT', 'mIKU_MOvE(Chara=0, z= i3, X =i1,y=i2 )')
        self.assertEqual(op.game, 'FT')
        self.assertEqual(op.op_id, 2)
        self.assertEqual(op.op_name, 'MIKU_MOVE')
        self.assertEqual(op.param_values, [0, 1, 2, 3])
        self.assertEqual(op.param_info, dsc_op_db[dsc_lookup_names['MIKU_MOVE']]['info_default']['param_info'])
    
    def test_op_from_string_sparse(self):
        op = pydsc.DscOp.from_string('FT', 'TARGET(type=cross, pos_x=i1, pos_y=i2, i3, amp=i5)')
        self.assertEqual(op.game, 'FT')
        self.assertEqual(op.op_id, 6)
        self.assertEqual(op.op_name, 'TARGET')
        pinfo = dsc_op_db[dsc_lookup_names['TARGET']]['info_FT']['param_info']
        self.assertEqual(op.param_values, ['cross', 1, 2, 3, pinfo[4]['default'], 5, pinfo[6]['default']])
        self.assertEqual(op.param_info, pinfo)
    
    def test_op_from_string_positional(self):
        op = pydsc.DscOp.from_string('FT', 'MIKU_MOVE(0, i1,i2, i3)')
        self.assertEqual(op.game, 'FT')
        self.assertEqual(op.op_id, 2)
        self.assertEqual(op.op_name, 'MIKU_MOVE')
        self.assertEqual(op.param_values, [0, 1, 2, 3])
        self.assertEqual(op.param_info, dsc_op_db[dsc_lookup_names['MIKU_MOVE']]['info_default']['param_info'])
    
    def test_op_from_string_auto_params(self):
        op = pydsc.DscOp.from_string('FT', 'LYRIC(1)')
        self.assertEqual(op.game, 'FT')
        self.assertEqual(op.op_id, 24)
        self.assertEqual(op.op_name, 'LYRIC')
        self.assertEqual(op.param_values, [1, -1])
        self.assertEqual(op.param_info, dsc_op_db[dsc_lookup_names['LYRIC']]['info_default']['param_info'])
    
    def test_op_from_string_auto_params(self):
        op = pydsc.DscOp.from_string('FT', 'LYRIC(id=1);')
        self.assertEqual(op.game, 'FT')
        self.assertEqual(op.op_id, 24)
        self.assertEqual(op.op_name, 'LYRIC')
        self.assertEqual(op.param_values, [1, -1])
        self.assertEqual(op.param_info, dsc_op_db[dsc_lookup_names['LYRIC']]['info_default']['param_info'])
    
    def test_op_from_string_params_enum(self):
        op = pydsc.DscOp.from_string('FT', 'HAND_SCALE(0, hand=right, i1000)')
        self.assertEqual(op.game, 'FT')
        self.assertEqual(op.op_id, 87)
        self.assertEqual(op.op_name, 'HAND_SCALE')
        self.assertEqual(op.param_values, [0, hand_scale_enum('right'), 1000])
        self.assertEqual(op.param_info, dsc_op_db[dsc_lookup_names['HAND_SCALE']]['info_FT']['param_info'])
    
    def test_op_from_string_none_id(self):
        try:
            op = pydsc.DscOp.from_string('PDA12', 'CHARA_HEIGHT_ADJUST()')
            self.assertTrue(False) # should fail with UnknownDscOpException
        except pydsc.UnknownDscOpException:
            pass
    
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
    
    def test_params_missing_none_param(self):
        op = pydsc.DscOp.from_string('FT', 'MOUTH_ANIM(chara=0, id=10, in_time=i20, speed=i30)')
        self.assertEqual(op.param_values, [0, 0, 10, 20, 30]) # second param is NoneType
    
    
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
    
    # Test going from DscOps to file and back
    
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
        
        b = pydsc.to_bytes(dsc)
        dsc_out = pydsc.from_bytes(b)
        
        self.assertEqual(dsc, dsc_out)


class TestDscString(unittest.TestCase):
    
    # Test string output
    
    def test_ft_string(self):
        strings = [
            'TIME(0);',
            '  MUSIC_PLAY();',
            '  CHANGE_FIELD(1);',
            '  MIKU_DISP(chara=0, visible=False);',
            '  MIKU_MOVE(chara=0, x=1.000, y=2.000, z=3.000);',
            '  HAND_SCALE(chara=0, hand=left, scale=122%);',
            '  MIKU_DISP(chara=0, visible=True);',
            '  TARGET(type=triangle_hold, pos_x=69.000, pos_y=420.000, angle=39.000, dist=1.000, amp=2.000, freq=3);',
            'PV_BRANCH_MODE(normal);',
            '    CHANGE_FIELD(2);',
            'TIME(1);',
            '    CHANGE_FIELD(3);',
            'PV_BRANCH_MODE(success);',
            '    CHANGE_FIELD(2);',
            'TIME(1);',
            '    CHANGE_FIELD(1);',
            'PV_BRANCH_MODE(none);',
            '  CHANGE_FIELD(4);',
            'TIME(1);',
            '  CHANGE_FIELD(5);',
            '  END();'
        ]
        strings_compat = [
            'TIME(i0);',
            'MUSIC_PLAY();',
            'CHANGE_FIELD(i1);',
            'MIKU_DISP(i0, i0);',
            'MIKU_MOVE(i0, i1000, i2000, i3000);',
            'HAND_SCALE(i0, i0, i1220);',
            'MIKU_DISP(i0, i1);',
            'TARGET(i4, i69000, i420000, i39000, i1000, i2000, i3);',
            'PV_BRANCH_MODE(i1);',
            'CHANGE_FIELD(i2);',
            'TIME(i100000);',
            'CHANGE_FIELD(i3);',
            'PV_BRANCH_MODE(i2);',
            'CHANGE_FIELD(i2);',
            'TIME(i100000);',
            'CHANGE_FIELD(i1);',
            'PV_BRANCH_MODE(i0);',
            'CHANGE_FIELD(i4);',
            'TIME(i100000);',
            'CHANGE_FIELD(i5);',
            'END();'
        ]
        
        dsc = [pydsc.DscOp.from_string('FT', s) for s in strings]
        
        self.maxDiff = None
        self.assertEqual(pydsc.dsc_to_string(dsc, indent=2), '\n'.join(strings))
        self.assertEqual(pydsc.dsc_to_string(dsc, compat_mode=True, indent=0), '\n'.join(strings_compat))
        self.assertEqual(dsc, [pydsc.DscOp.from_string('FT', s) for s in strings_compat])


class TestStringAnnot(unittest.TestCase):
    
    # throw all kinds of bad input at annotate_string to make sure it doesn't randomly fail
    
    def test_dsc_string_annot_positional(self):
        t = annotate_string('FT', 'HAND_SCALE(0,right, 1000)')
        expect = [
            {'start': 0, 'end': 25, 'name': 'op'},
            {'start': 0, 'end': 10, 'name': 'op_name'},
            {'start': 11, 'end': 12, 'name': 'param_value', 'param_index': 0},
            {'start': 13, 'end': 18, 'name': 'param_value', 'param_index': 1},
            {'start': 20, 'end': 24, 'name': 'param_value', 'param_index': 2},
        ]
        self.assertEqual(t, expect)
    
    def test_dsc_string_annot_positional_compat(self):
        t = annotate_string('FT', 'HAND_SCALE(i0,i1, i1000)')
        expect = [
            {'start': 0, 'end': 24, 'name': 'op'},
            {'start': 0, 'end': 10, 'name': 'op_name'},
            {'start': 11, 'end': 13, 'name': 'param_value', 'param_index': 0},
            {'start': 14, 'end': 16, 'name': 'param_value', 'param_index': 1},
            {'start': 18, 'end': 23, 'name': 'param_value', 'param_index': 2},
        ]
        self.assertEqual(t, expect)
    
    def test_dsc_string_annot_named(self):
        t = annotate_string('FT', ' HAND_SCALE ( chara=0, scale = 1000, 1 ) ;')
        expect = [
            {'start': 1, 'end': 40, 'name': 'op'},
            {'start': 1, 'end': 11, 'name': 'op_name'},
            {'start': 14, 'end': 20, 'name': 'param_name', 'param_index': 0},
            {'start': 20, 'end': 21, 'name': 'param_value', 'param_index': 0},
            {'start': 23, 'end': 30, 'name': 'param_name', 'param_index': 2},
            {'start': 31, 'end': 35, 'name': 'param_value', 'param_index': 2},
            {'start': 37, 'end': 38, 'name': 'param_value', 'param_index': 1},
        ]
        self.assertEqual(t, expect)
    
    def test_dsc_string_annot_wrong_fmt_no_parens(self):
        t = annotate_string('FT', 'HAND_SCALE 0,1,2;')
        expect = [
            {'start': 0, 'end': 16, 'name': 'invalid', 'reason': 'bad format'},
        ]
        self.assertEqual(t, expect)
    
    def test_dsc_string_annot_wrong_fmt_no_name(self):
        self.maxDiff = None
        t = annotate_string('FT', '(0, true, left)')
        expect = [
            {'start': 0, 'end': 15, 'name': 'invalid', 'reason': 'bad format'},
        ]
        self.assertEqual(t, expect)
    
    def test_dsc_string_annot_wrong_fmt_extra_parens_1(self):
        self.maxDiff = None
        t = annotate_string('FT', 'HAND_SCALE(0, (true, left)')
        expect = [
            {'start': 0, 'end': 26, 'name': 'invalid', 'reason': 'bad format'},
        ]
        self.assertEqual(t, expect)
    
    def test_dsc_string_annot_wrong_fmt_extra_parens_2(self):
        self.maxDiff = None
        t = annotate_string('FT', 'HAND_SCALE(0, true), left)')
        expect = [
            {'start': 0, 'end': 26, 'name': 'invalid', 'reason': 'bad format'},
        ]
        self.assertEqual(t, expect)
    
    def test_dsc_string_annot_bad_op_name(self):
        t = annotate_string('FT', 'BAD_SCALE(0,1,2);')
        expect = [
            {'start': 0, 'end': 16, 'name': 'op'},
            {'start': 0, 'end': 9, 'name': 'op_name'},
            {'start': 0, 'end': 9, 'name': 'invalid', 'reason': 'unknown op name'},
        ]
        self.assertEqual(t, expect)
    
    def test_dsc_string_annot_named_bad_name(self):
        t = annotate_string('FT', ' HAND_SCALE ( chara=0, scala = 1000, 1 ) ;')
        expect = [
            {'start': 1, 'end': 40, 'name': 'op'},
            {'start': 1, 'end': 11, 'name': 'op_name'},
            {'start': 12, 'end': 40, 'name': 'invalid', 'reason': 'missing required parameter scale' },
            {'start': 14, 'end': 20, 'name': 'param_name', 'param_index': 0},
            {'start': 20, 'end': 21, 'name': 'param_value', 'param_index': 0},
            {'start': 23, 'end': 35, 'name': 'invalid', 'reason': 'unknown parameter name'},
            {'start': 37, 'end': 38, 'name': 'param_value', 'param_index': 1},
        ]
        self.assertEqual(t, expect)
    
    def test_dsc_string_annot_named_dupe_name(self):
        t = annotate_string('FT', ' HAND_SCALE ( chara=0, chara = 1000, 1 ) ;')
        expect = [
            {'start': 1, 'end': 40, 'name': 'op'},
            {'start': 1, 'end': 11, 'name': 'op_name'},
            {'start': 12, 'end': 40, 'name': 'invalid', 'reason': 'missing required parameter scale' },
            {'start': 14, 'end': 20, 'name': 'param_name', 'param_index': 0},
            {'start': 20, 'end': 21, 'name': 'param_value', 'param_index': 0},
            {'start': 23, 'end': 35, 'name': 'invalid', 'reason': 'duplicate parameter'},
            {'start': 37, 'end': 38, 'name': 'param_value', 'param_index': 1},
        ]
        self.assertEqual(t, expect)
    
    def test_dsc_string_annot_missing_args(self):
        t = annotate_string('FT', 'HAND_SCALE(chara=0, scale=1000);')
        expect = [
            {'start': 0, 'end': 31, 'name': 'op'},
            {'start': 0, 'end': 10, 'name': 'op_name'},
            {'start': 10, 'end': 31, 'name': 'invalid', 'reason': 'missing required parameter hand' },
            {'start': 11, 'end': 17, 'name': 'param_name', 'param_index': 0},
            {'start': 17, 'end': 18, 'name': 'param_value', 'param_index': 0},
            {'start': 20, 'end': 26, 'name': 'param_name', 'param_index': 2},
            {'start': 26, 'end': 30, 'name': 'param_value', 'param_index': 2},
        ]
        self.assertEqual(t, expect)
    
    def test_dsc_string_annot_extra_args(self):
        t = annotate_string('FT', 'HAND_SCALE(chara=0, 1, 2, scale=1000, 3);')
        expect = [
            {'start': 0, 'end': 40, 'name': 'op'},
            {'start': 0, 'end': 10, 'name': 'op_name'},
            {'start': 11, 'end': 17, 'name': 'param_name', 'param_index': 0},
            {'start': 17, 'end': 18, 'name': 'param_value', 'param_index': 0},
            {'start': 20, 'end': 21, 'name': 'param_value', 'param_index': 1},
            {'start': 23, 'end': 24, 'name': 'invalid', 'reason': 'too many parameters'},
            {'start': 26, 'end': 32, 'name': 'param_name', 'param_index': 2},
            {'start': 32, 'end': 36, 'name': 'param_value', 'param_index': 2},
            {'start': 38, 'end': 39, 'name': 'invalid', 'reason': 'too many parameters'},
        ]
        self.assertEqual(t, expect)
    
    def test_dsc_string_annot_wrong_types(self):
        self.maxDiff = None
        t = annotate_string('FT', 'HAND_SCALE(0, true, left)')
        expect = [
            {'start': 0, 'end': 25, 'name': 'op'},
            {'start': 0, 'end': 10, 'name': 'op_name'},
            {'start': 11, 'end': 12, 'name': 'param_value', 'param_index': 0},
            {'start': 14, 'end': 18, 'name': 'param_value', 'param_index': 1},
            {'start': 14, 'end': 18, 'name': 'invalid', 'reason': 'cannot convert to correct type (Invalid enum value \'true\')'},
            {'start': 20, 'end': 24, 'name': 'param_value', 'param_index': 2},
            {'start': 20, 'end': 24, 'name': 'invalid', 'reason': 'cannot convert to correct type (invalid literal for int() with base 10: \'left\')'},
        ]
        self.assertEqual(t, expect)
    
    def test_dsc_get_annotated_str_matches(self):
        dsc = [
            pydsc.DscOp.from_string('FT', 'TIME(0)'),
            pydsc.DscOp.from_string('FT', 'MUSIC_PLAY()'),
            pydsc.DscOp.from_string('FT', 'CHANGE_FIELD(1)'),
            pydsc.DscOp.from_string('FT', 'MIKU_DISP(chara=0, visible=False)'),
            pydsc.DscOp.from_string('FT', 'MIKU_MOVE(chara=0, x=1, y=2, z=3)'),
            pydsc.DscOp.from_string('FT', 'HAND_SCALE(chara=0, hand=left, scale=1220)'),
            pydsc.DscOp.from_string('FT', 'END()')
        ]
        
        for op in dsc:
            opstr, reftags = op.get_annotated_str()
            t = annotate_string(op.game, opstr)
            self.assertEqual(reftags, t)
    
    def test_dsc_string_annot_mixed_case(self):
        t = annotate_string('FT', ' HAnD_SCaLE ( cHara=0, Scale = 1000, 1 ) ;')
        expect = [
            {'start': 1, 'end': 40, 'name': 'op'},
            {'start': 1, 'end': 11, 'name': 'op_name'},
            {'start': 14, 'end': 20, 'name': 'param_name', 'param_index': 0},
            {'start': 20, 'end': 21, 'name': 'param_value', 'param_index': 0},
            {'start': 23, 'end': 30, 'name': 'param_name', 'param_index': 2},
            {'start': 31, 'end': 35, 'name': 'param_value', 'param_index': 2},
            {'start': 37, 'end': 38, 'name': 'param_value', 'param_index': 1},
        ]
        self.assertEqual(t, expect)
    
    def test_dsc_string_annot_empty_arg(self):
        t = annotate_string('FT', 'TIME()')
        expect = [
            {'start': 0, 'end': 6, 'name': 'op'},
            {'start': 0, 'end': 4, 'name': 'op_name'},
            {'start': 4, 'end': 6, 'name': 'invalid', 'reason': 'missing required parameter time' },
            {'start': 5, 'end': 5, 'name': 'param_value', 'param_index': 0},
        ]
        self.assertEqual(t, expect)
    
    def test_dsc_string_annot_no_args(self):
        t = annotate_string('FT', 'END( )')
        expect = [
            {'start': 0, 'end': 6, 'name': 'op'},
            {'start': 0, 'end': 3, 'name': 'op_name'},
        ]
        self.assertEqual(t, expect)
    
    def test_dsc_string_annot_arg_empty_whitespace(self):
        t = annotate_string('FT', 'TIME(  )')
        expect = [
            {'start': 0, 'end': 8, 'name': 'op'},
            {'start': 0, 'end': 4, 'name': 'op_name'},
            {'start': 4, 'end': 8, 'name': 'invalid', 'reason': 'missing required parameter time' },
            {'start': 7, 'end': 7, 'name': 'param_value', 'param_index': 0},
        ]
        self.assertEqual(t, expect)

class cprt_tests(unittest.TestCase):
    
    # test against some official DSCs (if user supplies them)
    # pretty much just round trips through some stuff to check for loss
    
    if False and pathexists(joinpath(module_dir, '..', 'copyright!', 'script')):
        def test_dsc_real(self):
            # seen_sigs = []
            self.maxDiff = None
            for dscfile in listdir(joinpath(module_dir, '..', 'copyright!', 'script')):
                if not dscfile.endswith('.dsc'):
                    continue
                print (dscfile)
                
                with open(joinpath(module_dir, '..', 'copyright!', 'script', dscfile), 'rb') as f:
                    dsc = pydsc.from_stream(f)
                    f.seek(0)
                    sig = f.read(12)
                    # if not sig in seen_sigs:
                    #     print (sig.hex())
                    #     seen_sigs += [sig]
                    dsc_bytes_in = f.read()
                
                # check string annotation is working fine and that it isn't way too slow
                game = dsc[0].game
                dsc = [op.get_annotated_str(True, False, True) for op in dsc]
                #dsc = [op.get_annotated_str(False, True, False) for op in dsc]
                for opstr, reftags in dsc:
                    t = annotate_string(game, opstr)
                    self.assertEqual(reftags, t)
                
                dsc = [pydsc.DscOp.from_string(game, op[0]) for op in dsc]
                
                dsc_bytes_out = pydsc.to_bytes(dsc)[12:]
                self.assertEqual(dsc_bytes_in, dsc_bytes_out)