"""
list of dictionaries (one dict per opcode name)
opcodes have name, optional description, and optional game-specific info dicts

info dicts have id, param_cnt, and optional param_info
param_info is a list with len == param_cnt, where each element is a dict or None
param_info dicts have name, desc, type, required.
Non-required params also have default.

if a param_info type is derived from pydiva.util.stringenum.StringEnum
(`issubclass(type, StringEnum)`), use .choices to get a list of valid strings.

list of game-specific info dicts:
  info_PDA12, info_F2, info_FT, info_PSP1, info_PSP2, info_X, info_F
  (also info_default)

use info_default if no info exists for the game you're parsing
if no game-specific or default info is found, the game is not supported

additionally, an id of None indicates an unsupported opcode
"""

from pydiva.util.stringenum import StringEnum
from pydiva.util.stringbitfieldenum import StringBitfieldEnum
from pydiva.util.divatime import DivaTime
from pydiva.util.fixeddecimal import FixedDecimal
from pydiva.util.scaledint import ScaledInt

fixeddecimal_3 = type('fixeddecimal_3', (FixedDecimal,), {'dec_places': 3})
scaledint_pct_3dec = type('scaledint_pct_3dec', (ScaledInt,), {'value_min': 0, 'value_max': 1000})

dsc_op_db = [
    {
        'name': 'AGEAGE_CTRL',
        'desc': 'Set control parameters for the AgeAge Again hair effmodule effect.',
        'info_FT': {
            'id': 105,
            'param_cnt': 8,
            'param_info': [
                {'name': 'chara', 'desc': 'chara slot', 'required': True, 'type': int},
                {'name': 'side', 'desc': 'which side to control', 'required': True, 'type': type('ageage_ctrl_side_enum', (StringEnum,), {'choices': ['both', 'left', 'right']})},
                {'name': 'unk2', 'desc': 'should enable or disable something(?)', 'required': True, 'type': int},
                {'name': 'scale', 'desc': 'scale of the effect?', 'required': True, 'type': int},
                {'name': 'unk_flag4', 'desc': 'related to scaling?', 'required': False, 'default': -1, 'type': int},
                {'name': 'unk5', 'desc': 'might enable/disable the effect?', 'required': True, 'type': int},
                None,
                None
            ]
        }
    },
    {
        'name': 'AIM',
        'info_default': {
            'id': 46,
            'param_cnt': 3
        },
        'info_PDA12': {
            'id': None,
            'param_cnt': None
        },
        'info_PSP1': {
            'id': None,
            'param_cnt': None
        }
    },
    {
        'name': 'ANNOTATION',
        'info_X': {
            'id': 110,
            'param_cnt': 5
        }
    },
    {
        'name': 'AUTO_BLINK',
        'info_default': {
            'id': 56,
            'param_cnt': 2
        },
        'info_PDA12': {
            'id': None,
            'param_cnt': None
        },
        'info_PSP1': {
            'id': None,
            'param_cnt': None
        }
    },
    {
        'name': 'AUTO_CAPTURE',
        'desc': 'Automatically capture frames to CONT slot.',
        'info_default': {
            'id': 97,
            'param_cnt': 1,
            'param_info': [
                {'name': 'enable', 'desc': 'enable/disable capturing', 'required': True, 'type': bool}
            ]
        },
        'info_PDA12': {
            'id': None,
            'param_cnt': None
        },
        'info_PSP1': {
            'id': None,
            'param_cnt': None
        },
        'info_PSP2': {
            'id': None,
            'param_cnt': None
        },
        'info_F': {
            'id': None,
            'param_cnt': None
        }
    },
    {
        'name': 'BANK_BRANCH',
        'info_X': {
            'id': 131,
            'param_cnt': 2
        }
    },
    {
        'name': 'BANK_END',
        'info_X': {
            'id': 132,
            'param_cnt': 2
        }
    },
    {
        'name': 'BAR_POINT',
        'info_X': {
            'id': 85,
            'param_cnt': 1
        }
    },
    {
        'name': 'BAR_TIME_SET',
        'desc': 'Set the length of a measure/bar.',
        'info_default': {
            'id': 28,
            'param_cnt': 2,
            'param_info': [
                {'name': 'bpm', 'desc': 'BPM to use for calculation', 'required': True, 'type': int},
                {'name': 'beats', 'desc': 'number of quarter note beats minus 1 (3 for 4/4)', 'required': True, 'type': int}
            ]
        }
    },
    {
        'name': 'BEAT_POINT',
        'info_X': {
            'id': 86,
            'param_cnt': 1
        }
    },
    {
        'name': 'BLOOM',
        'desc': 'Set bloom data.',
        'info_default': {
            'id': 93,
            'param_cnt': 2,
            'param_info': [
                {'name': 'id', 'desc': 'bloom preset/mode?', 'required': True, 'type': int},
                {'name': 'unk1', 'desc': 'maybe amount??', 'required': True, 'type': int}
            ]
        },
        'info_PDA12': {
            'id': None,
            'param_cnt': None
        },
        'info_PSP1': {
            'id': None,
            'param_cnt': None
        },
        'info_PSP2': {
            'id': None,
            'param_cnt': None
        },
        'info_F': {
            'id': None,
            'param_cnt': None
        }
    },
    {
        'name': 'CHANGE_FIELD',
        'desc': 'Change the PV field.',
        'info_default': {
            'id': 14,
            'param_cnt': 1,
            'param_info': [
                {'name': 'id', 'desc': 'field number', 'required': True, 'type': int}
            ]
        },
        'info_F2': {
            'id': 14,
            'param_cnt': 2
        },
        'info_X': {
            'id': 14,
            'param_cnt': 2
        }
    },
    {
        'name': 'CHARA_ALPHA',
        'info_default': {
            'id': 96,
            'param_cnt': 4
        },
        'info_PDA12': {
            'id': None,
            'param_cnt': None
        },
        'info_PSP1': {
            'id': None,
            'param_cnt': None
        },
        'info_PSP2': {
            'id': None,
            'param_cnt': None
        },
        'info_F': {
            'id': None,
            'param_cnt': None
        }
    },
    {
        'name': 'CHARA_COLOR',
        'info_default': {
            'id': 72,
            'param_cnt': 2
        },
        'info_PDA12': {
            'id': None,
            'param_cnt': None
        },
        'info_PSP1': {
            'id': None,
            'param_cnt': None
        },
        'info_PSP2': {
            'id': None,
            'param_cnt': None
        }
    },
    {
        'name': 'CHARA_EFFECT',
        'info_X': {
            'id': 124,
            'param_cnt': 3
        }
    },
    {
        'name': 'CHARA_EFFECT_CHARA_LIGHT',
        'info_X': {
            'id': 126,
            'param_cnt': 3
        }
    },
    {
        'name': 'CHARA_HEIGHT_ADJUST',
        'info_default': {
            'id': 60,
            'param_cnt': 2
        },
        'info_PDA12': {
            'id': None,
            'param_cnt': None
        },
        'info_PSP1': {
            'id': None,
            'param_cnt': None
        }
    },
    {
        'name': 'CHARA_LIGHT',
        'info_FT': {
            'id': 103,
            'param_cnt': 3
        }
    },
    {
        'name': 'CHARA_POS_ADJUST',
        'info_default': {
            'id': 62,
            'param_cnt': 4
        },
        'info_PDA12': {
            'id': None,
            'param_cnt': None
        },
        'info_PSP1': {
            'id': None,
            'param_cnt': None
        }
    },
    {
        'name': 'CHARA_SHADOW_QUALITY',
        'info_X': {
            'id': 74,
            'param_cnt': 2
        }
    },
    {
        'name': 'CHARA_SIZE',
        'desc': 'Set a character\'s size scale.',
        'info_default': {
            'id': 59,
            'param_cnt': 2,
            'param_info': [
                {'name': 'chara', 'desc': 'chara slot', 'required': True, 'type': int},
                {'name': 'size', 'desc': 'chara size -- values 0~3 are special', 'required': True, 'type': int}
            ]
        },
        'info_PDA12': {
            'id': None,
            'param_cnt': None
        },
        'info_PSP1': {
            'id': None,
            'param_cnt': None
        }
    },
    {
        'name': 'CHROMATIC_ABERRATION',
        'info_X': {
            'id': 80,
            'param_cnt': 3
        }
    },
    {
        'name': 'CLOTH_WET',
        'info_default': {
            'id': 50,
            'param_cnt': 2
        },
        'info_PDA12': {
            'id': 35,
            'param_cnt': 1
        },
        'info_PSP1': {
            'id': 35,
            'param_cnt': 1
        }
    },
    {
        'name': 'COLOR_CORRECT',
        'info_default': {
            'id': 94,
            'param_cnt': 3
        },
        'info_PDA12': {
            'id': None,
            'param_cnt': None
        },
        'info_PSP1': {
            'id': None,
            'param_cnt': None
        },
        'info_PSP2': {
            'id': None,
            'param_cnt': None
        },
        'info_F': {
            'id': None,
            'param_cnt': None
        }
    },
    {
        'name': 'COMMON_EFFECT_AET_FRONT',
        'info_X': {
            'id': 118,
            'param_cnt': 2
        }
    },
    {
        'name': 'COMMON_EFFECT_AET_FRONT_LOW',
        'info_X': {
            'id': 119,
            'param_cnt': 2
        }
    },
    {
        'name': 'COMMON_EFFECT_PARTICLE',
        'info_X': {
            'id': 120,
            'param_cnt': 2
        }
    },
    {
        'name': 'COMMON_LIGHT',
        'info_X': {
            'id': 76,
            'param_cnt': 2
        }
    },
    {
        'name': 'CREDIT_TITLE',
        'info_X': {
            'id': 84,
            'param_cnt': 1
        }
    },
    {
        'name': 'CROSSFADE',
        'info_F2': {
            'id': 103,
            'param_cnt': 1
        }
    },
    {
        'name': 'DATA_CAMERA',
        'desc': 'Load camera data.',
        'info_default': {
            'id': 13,
            'param_cnt': 2,
            'param_info': [
                {'name': 'mode', 'desc': 'camera mode/type?', 'required': True, 'type': type('data_camera_mode_enum', (StringEnum,), {'choices': ['unk0', 'unk1', 'unk2']})},
                {'name': 'id', 'desc': 'camera number?', 'required': True, 'type': int}
            ]
        }
    },
    {
        'name': 'DATA_CAMERA_START',
        'desc': '(Re)start camera data(?).',
        'info_default': {
            'id': 66,
            'param_cnt': 2,
            'param_info': [
                {'name': 'mode', 'desc': 'camera mode/type?', 'required': True, 'type': type('data_camera_mode_enum', (StringEnum,), {'choices': ['unk0', 'unk1', 'unk2']})},
                {'name': 'id', 'desc': 'camera number?', 'required': True, 'type': int}
            ]
        },
        'info_PDA12': {
            'id': None,
            'param_cnt': None
        },
        'info_PSP1': {
            'id': None,
            'param_cnt': None
        },
        'info_PSP2': {
            'id': None,
            'param_cnt': None
        }
    },
    {
        'name': 'DOF',
        'desc': 'Set depth-of-field.',
        'info_default': {
            'id': 95,
            'param_cnt': 3,
            'param_info': [
                {'name': 'enable', 'desc': 'enable/disable', 'required': True, 'type': bool},
                {'name': 'id', 'desc': 'preset/mode?', 'required': True, 'type': int},
                {'name': 'unk2', 'desc': 'maybe focus distance??', 'required': True, 'type': int}
            ]
        },
        'info_PDA12': {
            'id': None,
            'param_cnt': None
        },
        'info_PSP1': {
            'id': None,
            'param_cnt': None
        },
        'info_PSP2': {
            'id': None,
            'param_cnt': None
        },
        'info_F': {
            'id': None,
            'param_cnt': None
        }
    },
    {
        'name': 'DUMMY',
        'info_X': {
            'id': 31,
            'param_cnt': 21
        }
    },
    {
        'name': 'EDIT_BLUSH',
        'info_default': {
            'id': 48,
            'param_cnt': 1
        },
        'info_PDA12': {
            'id': None,
            'param_cnt': None
        },
        'info_PSP1': {
            'id': None,
            'param_cnt': None
        }
    },
    {
        'name': 'EDIT_CAMERA',
        'info_F2': {
            'id': 81,
            'param_cnt': 22
        },
        'info_FT': {
            'id': 81,
            'param_cnt': 24
        },
        'info_F': {
            'id': 81,
            'param_cnt': 24
        }
    },
    {
        'name': 'EDIT_CAMERA_BOX',
        'info_F2': {
            'id': 108,
            'param_cnt': 112
        },
        'info_X': {
            'id': 103,
            'param_cnt': 112
        }
    },
    {
        'name': 'EDIT_CHANGE_FIELD',
        'info_F2': {
            'id': 110,
            'param_cnt': 1
        },
        'info_X': {
            'id': 105,
            'param_cnt': 1
        }
    },
    {
        'name': 'EDIT_DISP',
        'info_default': {
            'id': 44,
            'param_cnt': 1
        },
        'info_PDA12': {
            'id': None,
            'param_cnt': None
        },
        'info_PSP1': {
            'id': None,
            'param_cnt': None
        }
    },
    {
        'name': 'EDIT_EFFECT',
        'info_default': {
            'id': 43,
            'param_cnt': 2
        },
        'info_PDA12': {
            'id': None,
            'param_cnt': None
        },
        'info_PSP1': {
            'id': None,
            'param_cnt': None
        }
    },
    {
        'name': 'EDIT_EXPRESSION',
        'info_F2': {
            'id': 78,
            'param_cnt': 2
        },
        'info_FT': {
            'id': 78,
            'param_cnt': 2
        },
        'info_F': {
            'id': 78,
            'param_cnt': 2
        }
    },
    {
        'name': 'EDIT_EYE',
        'info_default': {
            'id': 41,
            'param_cnt': 2
        },
        'info_PDA12': {
            'id': None,
            'param_cnt': None
        },
        'info_PSP1': {
            'id': None,
            'param_cnt': None
        }
    },
    {
        'name': 'EDIT_EYELID',
        'info_default': {
            'id': 40,
            'param_cnt': 1
        },
        'info_PDA12': {
            'id': None,
            'param_cnt': None
        },
        'info_PSP1': {
            'id': None,
            'param_cnt': None
        }
    },
    {
        'name': 'EDIT_EYELID_ANIM',
        'info_F2': {
            'id': 75,
            'param_cnt': 3
        },
        'info_FT': {
            'id': 75,
            'param_cnt': 3
        },
        'info_F': {
            'id': 75,
            'param_cnt': 3
        }
    },
    {
        'name': 'EDIT_EYE_ANIM',
        'info_F2': {
            'id': 79,
            'param_cnt': 3
        },
        'info_FT': {
            'id': 79,
            'param_cnt': 3
        },
        'info_F': {
            'id': 79,
            'param_cnt': 3
        }
    },
    {
        'name': 'EDIT_FACE',
        'info_default': {
            'id': 30,
            'param_cnt': 1
        },
        'info_PDA12': {
            'id': 30,
            'param_cnt': 2
        },
        'info_PSP1': {
            'id': 30,
            'param_cnt': 2
        }
    },
    {
        'name': 'EDIT_HAND_ANIM',
        'info_default': {
            'id': 45,
            'param_cnt': 2
        },
        'info_PDA12': {
            'id': None,
            'param_cnt': None
        },
        'info_PSP1': {
            'id': None,
            'param_cnt': None
        }
    },
    {
        'name': 'EDIT_INSTRUMENT_ITEM',
        'info_F2': {
            'id': 76,
            'param_cnt': 2
        },
        'info_FT': {
            'id': 76,
            'param_cnt': 2
        },
        'info_F': {
            'id': 76,
            'param_cnt': 2
        }
    },
    {
        'name': 'EDIT_ITEM',
        'info_default': {
            'id': 42,
            'param_cnt': 1
        },
        'info_PDA12': {
            'id': None,
            'param_cnt': None
        },
        'info_PSP1': {
            'id': None,
            'param_cnt': None
        }
    },
    {
        'name': 'EDIT_LYRIC',
        'desc': 'Display an edit lyric.',
        'info_default': {
            'id': 34,
            'param_cnt': 2,
            'param_info': [
                {'name': 'id', 'desc': 'lyric line number', 'required': True, 'type': int},
                {'name': 'end_time', 'desc': 'time to hide lyric at', 'required': True, 'type': DivaTime}
            ]
        },
        'info_PDA12': {
            'id': None,
            'param_cnt': None
        },
        'info_PSP1': {
            'id': None,
            'param_cnt': None
        }
    },
    {
        'name': 'EDIT_MODE_SELECT',
        'desc': 'Start or end a special chart section (challenge time, etc) in an edit',
        'info_default': {
            'id': 82,
            'param_cnt': 1,
            'param_info': [
                {'name': 'mode', 'desc': 'mode to enter', 'required': True, 'type': type('mode_select_mode_enum', (StringEnum,), {'choices': ['unk0', 'challenge_start', 'unk2', 'challenge_end', 'unk4', 'unk5', 'unk6', 'unk7', 'technical_start', 'technical_end']})}
            ]
        },
        'info_PDA12': {
            'id': None,
            'param_cnt': None
        },
        'info_PSP1': {
            'id': None,
            'param_cnt': None
        },
        'info_PSP2': {
            'id': None,
            'param_cnt': None
        },
        'info_X': {
            'id': None,
            'param_cnt': None
        }
    },
    {
        'name': 'EDIT_MOTION',
        'info_default': {
            'id': 27,
            'param_cnt': 4
        },
        'info_PDA12': {
            'id': 27,
            'param_cnt': 2
        },
        'info_PSP1': {
            'id': 27,
            'param_cnt': 2
        }
    },
    {
        'name': 'EDIT_MOTION_F',
        'info_FT': {
            'id': 91,
            'param_cnt': 6
        }
    },
    {
        'name': 'EDIT_MOTION_LOOP',
        'info_F2': {
            'id': 77,
            'param_cnt': 4
        },
        'info_FT': {
            'id': 77,
            'param_cnt': 4
        },
        'info_F': {
            'id': 77,
            'param_cnt': 4
        }
    },
    {
        'name': 'EDIT_MOT_SMOOTH_LEN',
        'info_F2': {
            'id': 64,
            'param_cnt': 2
        },
        'info_FT': {
            'id': 64,
            'param_cnt': 2
        },
        'info_X': {
            'id': 64,
            'param_cnt': 2
        },
        'info_F': {
            'id': 64,
            'param_cnt': 2
        }
    },
    {
        'name': 'EDIT_MOUTH',
        'info_default': {
            'id': 36,
            'param_cnt': 1
        },
        'info_PDA12': {
            'id': None,
            'param_cnt': None
        },
        'info_PSP1': {
            'id': None,
            'param_cnt': None
        }
    },
    {
        'name': 'EDIT_MOUTH_ANIM',
        'info_F2': {
            'id': 80,
            'param_cnt': 2
        },
        'info_FT': {
            'id': 80,
            'param_cnt': 2
        },
        'info_F': {
            'id': 80,
            'param_cnt': 2
        }
    },
    {
        'name': 'EDIT_MOVE',
        'info_default': {
            'id': 38,
            'param_cnt': 7
        },
        'info_PDA12': {
            'id': None,
            'param_cnt': None
        },
        'info_PSP1': {
            'id': None,
            'param_cnt': None
        }
    },
    {
        'name': 'EDIT_MOVE_XYZ',
        'info_F2': {
            'id': 74,
            'param_cnt': 9
        },
        'info_FT': {
            'id': 74,
            'param_cnt': 9
        },
        'info_F': {
            'id': 74,
            'param_cnt': 9
        }
    },
    {
        'name': 'EDIT_SHADOW',
        'info_default': {
            'id': 39,
            'param_cnt': 1
        },
        'info_PDA12': {
            'id': None,
            'param_cnt': None
        },
        'info_PSP1': {
            'id': None,
            'param_cnt': None
        }
    },
    {
        'name': 'EDIT_STAGE_PARAM',
        'info_F2': {
            'id': 109,
            'param_cnt': 1
        },
        'info_X': {
            'id': 104,
            'param_cnt': 1
        }
    },
    {
        'name': 'EDIT_TARGET',
        'info_default': {
            'id': 35,
            'param_cnt': 5
        },
        'info_PDA12': {
            'id': None,
            'param_cnt': None
        },
        'info_PSP1': {
            'id': None,
            'param_cnt': None
        }
    },
    {
        'name': 'EFFECT',
        'info_default': {
            'id': 9,
            'param_cnt': 6
        },
        'info_PDA12': {
            'id': 9,
            'param_cnt': 5
        },
        'info_PSP1': {
            'id': 9,
            'param_cnt': 5
        }
    },
    {
        'name': 'EFFECT_OFF',
        'info_default': {
            'id': 11,
            'param_cnt': 1
        }
    },
    {
        'name': 'ENABLE_COMMON_LIGHT_TO_CHARA',
        'info_X': {
            'id': 127,
            'param_cnt': 2
        }
    },
    {
        'name': 'ENABLE_FXAA',
        'info_X': {
            'id': 128,
            'param_cnt': 2
        }
    },
    {
        'name': 'ENABLE_REFLECTION',
        'info_X': {
            'id': 130,
            'param_cnt': 2
        }
    },
    {
        'name': 'ENABLE_TEMPORAL_AA',
        'info_X': {
            'id': 129,
            'param_cnt': 2
        }
    },
    {
        'name': 'END',
        'desc': 'End the DSC file.',
        'info_default': {
            'id': 0,
            'param_cnt': 0
        }
    },
    {
        'name': 'EVENT_JUDGE',
        'info_F2': {
            'id': 105,
            'param_cnt': 36
        }
    },
    {
        'name': 'EXPRESSION',
        'info_default': {
            'id': 22,
            'param_cnt': 4
        },
        'info_PDA12': {
            'id': 22,
            'param_cnt': 3
        },
        'info_PSP1': {
            'id': 22,
            'param_cnt': 3
        }
    },
    {
        'name': 'EYE_ANIM',
        'info_default': {
            'id': 18,
            'param_cnt': 3
        },
        'info_PDA12': {
            'id': 18,
            'param_cnt': 2
        },
        'info_PSP1': {
            'id': 18,
            'param_cnt': 2
        }
    },
    {
        'name': 'FACE_TYPE',
        'info_FT': {
            'id': 89,
            'param_cnt': 1
        }
    },
    {
        'name': 'FADE',
        'info_X': {
            'id': 115,
            'param_cnt': 2
        }
    },
    {
        'name': 'FADEIN_FIELD',
        'info_default': {
            'id': 10,
            'param_cnt': 2
        }
    },
    {
        'name': 'FADEOUT_FIELD',
        'info_default': {
            'id': 17,
            'param_cnt': 2
        }
    },
    {
        'name': 'FADE_MODE',
        'info_default': {
            'id': 55,
            'param_cnt': 1
        },
        'info_PDA12': {
            'id': 39,
            'param_cnt': 1
        },
        'info_PSP1': {
            'id': None,
            'param_cnt': None
        }
    },
    {
        'name': 'FOG',
        'info_F2': {
            'id': 92,
            'param_cnt': 3
        },
        'info_FT': {
            'id': 92,
            'param_cnt': 3
        },
        'info_X': {
            'id': 92,
            'param_cnt': 3
        }
    },
    {
        'name': 'FOG_ENABLE',
        'info_F2': {
            'id': 107,
            'param_cnt': 2
        }
    },
    {
        'name': 'GAZE',
        'info_X': {
            'id': 148,
            'param_cnt': 2
        }
    },
    {
        'name': 'HAND_ANIM',
        'info_default': {
            'id': 20,
            'param_cnt': 5
        },
        'info_PDA12': {
            'id': 20,
            'param_cnt': 4
        },
        'info_PSP1': {
            'id': 20,
            'param_cnt': 4
        }
    },
    {
        'name': 'HAND_ITEM',
        'info_default': {
            'id': 47,
            'param_cnt': 3
        },
        'info_PDA12': {
            'id': None,
            'param_cnt': None
        },
        'info_PSP1': {
            'id': None,
            'param_cnt': None
        }
    },
    {
        'name': 'HAND_SCALE',
        'desc': 'Change the size of a character\'s hands.',
        'info_FT': {
            'id': 87,
            'param_cnt': 3,
            'param_info': [
                {'name': 'chara', 'desc': 'chara slot', 'required': True, 'type': int},
                {'name': 'hand', 'desc': 'which hand to change', 'required': True, 'type': type('hand_scale_hand_enum', (StringEnum,), {'choices': ['left', 'right']})},
                {'name': 'scale', 'desc': 'scale size', 'required': True, 'type': scaledint_pct_3dec}
            ]
        }
    },
    {
        'name': 'HIDE_FIELD',
        'info_default': {
            'id': 15,
            'param_cnt': 1
        }
    },
    {
        'name': 'IBL_COLOR',
        'info_X': {
            'id': 78,
            'param_cnt': 2
        }
    },
    {
        'name': 'ITEM_ALPHA',
        'info_F2': {
            'id': 101,
            'param_cnt': 4
        },
        'info_FT': {
            'id': 101,
            'param_cnt': 4
        },
        'info_X': {
            'id': 101,
            'param_cnt': 4
        }
    },
    {
        'name': 'ITEM_ANIM',
        'info_default': {
            'id': 61,
            'param_cnt': 4
        },
        'info_PDA12': {
            'id': None,
            'param_cnt': None
        },
        'info_PSP1': {
            'id': None,
            'param_cnt': None
        }
    },
    {
        'name': 'ITEM_ANIM_ATTACH',
        'info_FT': {
            'id': 85,
            'param_cnt': 3
        }
    },
    {
        'name': 'ITEM_LIGHT',
        'info_X': {
            'id': 123,
            'param_cnt': 3
        }
    },
    {
        'name': 'LIGHT_AUTH',
        'info_X': {
            'id': 114,
            'param_cnt': 2
        }
    },
    {
        'name': 'LIGHT_POS',
        'info_FT': {
            'id': 88,
            'param_cnt': 4
        }
    },
    {
        'name': 'LIGHT_ROT',
        'info_default': {
            'id': 51,
            'param_cnt': 3
        },
        'info_PDA12': {
            'id': None,
            'param_cnt': None
        },
        'info_PSP1': {
            'id': None,
            'param_cnt': None
        }
    },
    {
        'name': 'LOOK_ANIM',
        'info_default': {
            'id': 21,
            'param_cnt': 4
        },
        'info_PDA12': {
            'id': 21,
            'param_cnt': 3
        },
        'info_PSP1': {
            'id': 21,
            'param_cnt': 3
        }
    },
    {
        'name': 'LOOK_CAMERA',
        'info_default': {
            'id': 23,
            'param_cnt': 5
        },
        'info_PDA12': {
            'id': 23,
            'param_cnt': 4
        },
        'info_PSP1': {
            'id': 23,
            'param_cnt': 4
        }
    },
    {
        'name': 'LOOK_CAMERA_FACE_LIMIT',
        'info_X': {
            'id': 122,
            'param_cnt': 5
        }
    },
    {
        'name': 'LYRIC',
        'desc': 'Display a lyric.',
        'info_default': {
            'id': 24,
            'param_cnt': 2,
            'param_info': [
                {'name': 'id', 'desc': 'lyric line number', 'required': True, 'type': int},
                {'name': 'color', 'desc': 'color of lyrics', 'required': False, 'default': -1, 'type': int}
            ]
        },
        'info_PDA12': {
            'id': 24,
            'param_cnt': 1,
            'param_info': [
                {'name': 'id', 'desc': 'lyric line number', 'required': True, 'type': int}
            ]
        },
        'info_PSP1': {
            'id': 24,
            'param_cnt': 1,
            'param_info': [
                {'name': 'id', 'desc': 'lyric line number', 'required': True, 'type': int}
            ]
        }
    },
    {
        'name': 'LYRIC_2',
        'info_X': {
            'id': 107,
            'param_cnt': 2
        }
    },
    {
        'name': 'LYRIC_READ',
        'info_X': {
            'id': 108,
            'param_cnt': 2
        }
    },
    {
        'name': 'LYRIC_READ_2',
        'info_X': {
            'id': 109,
            'param_cnt': 2
        }
    },
    {
        'name': 'MANUAL_CAPTURE',
        'desc': 'Manually capture frame to chosen slot.',
        'info_default': {
            'id': 98,
            'param_cnt': 1,
            'param_info': [
                {'name': 'slot', 'desc': 'slot to capture to', 'required': True, 'type': type('capture_slot_enum', (StringEnum,), {'choices': ['A', 'B', 'C', 'D', 'E']})}
            ]
        },
        'info_PDA12': {
            'id': None,
            'param_cnt': None
        },
        'info_PSP1': {
            'id': None,
            'param_cnt': None
        },
        'info_PSP2': {
            'id': None,
            'param_cnt': None
        },
        'info_F': {
            'id': None,
            'param_cnt': None
        }
    },
    {
        'name': 'MARKER',
        'info_X': {
            'id': 125,
            'param_cnt': 2
        }
    },
    {
        'name': 'MIKUDAYO_ADJUST',
        'info_X': {
            'id': 106,
            'param_cnt': 7
        }
    },
    {
        'name': 'MIKU_DISP',
        'desc': 'Show or hide a character.',
        'info_default': {
            'id': 4,
            'param_cnt': 2,
            'param_info': [
                {'name': 'chara', 'desc': 'chara slot', 'required': True, 'type': int},
                {'name': 'visible', 'desc': 'visible or not', 'required': True, 'type': bool}
            ]
        },
        'info_PDA12': {
            'id': 4,
            'param_cnt': 1,
            'param_info': [
                {'name': 'visible', 'desc': 'visible or not', 'required': True, 'type': bool}
            ]
        },
        'info_PSP1': {
            'id': 4,
            'param_cnt': 1,
            'param_info': [
                {'name': 'visible', 'desc': 'visible or not', 'required': True, 'type': bool}
            ]
        }
    },
    {
        'name': 'MIKU_MOVE',
        'desc': 'Move a character.',
        'info_default': {
            'id': 2,
            'param_cnt': 4,
            'param_info': [
                {'name': 'chara', 'desc': 'chara slot', 'required': True, 'type': int},
                {'name': 'x', 'desc': 'x position', 'required': True, 'type': fixeddecimal_3},
                {'name': 'y', 'desc': 'y position', 'required': True, 'type': fixeddecimal_3},
                {'name': 'z', 'desc': 'z position', 'required': True, 'type': fixeddecimal_3}
            ]
        },
        'info_PDA12': {
            'id': 2,
            'param_cnt': 3,
            'param_info': [
                {'name': 'x', 'desc': 'x position', 'required': True, 'type': fixeddecimal_3},
                {'name': 'y', 'desc': 'y position', 'required': True, 'type': fixeddecimal_3},
                {'name': 'z', 'desc': 'z position', 'required': True, 'type': fixeddecimal_3}
            ]
        },
        'info_PSP1': {
            'id': 2,
            'param_cnt': 3,
            'param_info': [
                {'name': 'x', 'desc': 'x position', 'required': True, 'type': fixeddecimal_3},
                {'name': 'y', 'desc': 'y position', 'required': True, 'type': fixeddecimal_3},
                {'name': 'z', 'desc': 'z position', 'required': True, 'type': fixeddecimal_3}
            ]
        }
    },
    {
        'name': 'MIKU_ROT',
        'desc': 'Rotate a character.',
        'info_default': {
            'id': 3,
            'param_cnt': 2,
            'param_info': [
                {'name': 'chara', 'desc': 'chara slot', 'required': True, 'type': int},
                {'name': 'angle', 'desc': 'angle', 'required': True, 'type': fixeddecimal_3}
            ]
        },
        'info_PDA12': {
            'id': 3,
            'param_cnt': 1,
            'param_info': [
                {'name': 'angle', 'desc': 'angle', 'required': True, 'type': fixeddecimal_3}
            ]
        },
        'info_PSP1': {
            'id': 3,
            'param_cnt': 1,
            'param_info': [
                {'name': 'angle', 'desc': 'angle', 'required': True, 'type': fixeddecimal_3}
            ]
        }
    },
    {
        'name': 'MIKU_SHADOW',
        'desc': 'Show or hide a character\'s shadow.',
        'info_default': {
            'id': 5,
            'param_cnt': 2,
            'param_info': [
                {'name': 'chara', 'desc': 'chara slot', 'required': True, 'type': int},
                {'name': 'visible', 'desc': 'shadow visible or not(?) (does nothing in AFT)', 'required': True, 'type': bool}
            ]
        },
        'info_PDA12': {
            'id': 5,
            'param_cnt': 1,
            'param_info': [
                {'name': 'visible', 'desc': 'shadow visible or not(?) (does nothing in AFT)', 'required': True, 'type': bool}
            ]
        },
        'info_PSP1': {
            'id': 5,
            'param_cnt': 1,
            'param_info': [
                {'name': 'visible', 'desc': 'shadow visible or not(?) (does nothing in AFT)', 'required': True, 'type': bool}
            ]
        }
    },
    {
        'name': 'MODE_SELECT',
        'desc': 'Start or end a special chart section (challenge time, etc)',
        'info_default': {
            'id': 26,
            'param_cnt': 2,
            'param_info': [
                {'name': 'difficulty', 'desc': 'difficulty to affect (not really sure how this works, and apparently ex_extreme should actually be easy_2 but I don\'t see why that would be the case)', 'required': True, 'type': type('mode_select_difficulty_enum', (StringBitfieldEnum,), {'choices': ['easy', 'normal', 'hard', 'extreme', 'ex_extreme']})}, # , 'easy_2', 'normal_2', 'hard_2', 'extreme_2'
                {'name': 'mode', 'desc': 'mode to enter', 'required': True, 'type': type('mode_select_mode_enum', (StringEnum,), {'choices': ['unk0', 'challenge_start', 'unk2', 'challenge_end', 'unk4', 'unk5', 'unk6', 'unk7', 'technical_start', 'technical_end']})}
            ]
        },
        'info_PDA12': {
            'id': 26,
            'param_cnt': 1
        },
        'info_PSP1': {
            'id': 26,
            'param_cnt': 1
        }
    },
    {
        'name': 'MOUTH_ANIM',
        'desc': 'Set a character\'s mouth animation.',
        'info_default': {
            'id': 19,
            'param_cnt': 5,
            'param_info': [
                {'name': 'chara', 'desc': 'chara slot', 'required': True, 'type': int},
                None, # not even read in aft
                {'name': 'id', 'desc': 'mouth animation number', 'required': True, 'type': int},
                {'name': 'in_time', 'desc': 'animation in time? (ms)', 'required': False, 'default': -1, 'type': int},
                {'name': 'speed', 'desc': 'animation speed? (ms)', 'required': False, 'default': -1, 'type': int},
            ]
        },
        'info_PDA12': {
            'id': 19,
            'param_cnt': 3,
            'param_info': [
                {'name': 'id', 'desc': 'mouth animation number', 'required': True, 'type': int},
                {'name': 'in_time', 'desc': 'animation in time? (ms)', 'required': False, 'default': -1, 'type': int},
                {'name': 'speed', 'desc': 'animation speed? (ms)', 'required': False, 'default': -1, 'type': int},
            ]
        },
        'info_PSP1': {
            'id': 19,
            'param_cnt': 3,
            'param_info': [
                {'name': 'id', 'desc': 'mouth animation number', 'required': True, 'type': int},
                {'name': 'in_time', 'desc': 'animation in time? (ms)', 'required': False, 'default': -1, 'type': int},
                {'name': 'speed', 'desc': 'animation speed? (ms)', 'required': False, 'default': -1, 'type': int},
            ]
        }
    },
    {
        'name': 'MOVE_CAMERA',
        'info_default': {
            'id': 31,
            'param_cnt': 21
        },
        'info_PDA12': {
            'id': 31,
            'param_cnt': 19
        },
        'info_PSP1': {
            'id': 31,
            'param_cnt': 19
        },
        'info_X': {
            'id': None,
            'param_cnt': None
        }
    },
    {
        'name': 'MOVE_FIELD',
        'info_default': {
            'id': 16,
            'param_cnt': 3
        }
    },
    {
        'name': 'MOVIE_CUT',
        'info_F2': {
            'id': 102,
            'param_cnt': 1
        },
        'info_X': {
            'id': 102,
            'param_cnt': 1
        }
    },
    {
        'name': 'MOVIE_CUT_CHG',
        'info_FT': {
            'id': 102,
            'param_cnt': 1
        }
    },
    {
        'name': 'MOVIE_DISP',
        'desc': 'Show a movie.',
        'info_default': {
            'id': 68,
            'param_cnt': 1,
            'param_info': [
                {'name': 'id', 'desc': 'movie id (ignored by AFT)', 'required': True, 'type': int}
            ]
        },
        'info_PDA12': {
            'id': None,
            'param_cnt': None
        },
        'info_PSP1': {
            'id': None,
            'param_cnt': None
        },
        'info_PSP2': {
            'id': None,
            'param_cnt': None
        }
    },
    {
        'name': 'MOVIE_PLAY',
        'desc': 'Start movie playback.',
        'info_default': {
            'id': 67,
            'param_cnt': 1,
            'param_info': [
                {'name': 'play', 'desc': 'play or not (must be true for AFT to do anything)', 'required': True, 'type': bool}
            ]
        },
        'info_PDA12': {
            'id': None,
            'param_cnt': None
        },
        'info_PSP1': {
            'id': None,
            'param_cnt': None
        },
        'info_PSP2': {
            'id': None,
            'param_cnt': None
        }
    },
    {
        'name': 'MUSIC_PLAY',
        'desc': 'Start music playback.',
        'info_default': {
            'id': 25,
            'param_cnt': 0
        }
    },
    {
        'name': 'NEAR_CLIP',
        'info_default': {
            'id': 49,
            'param_cnt': 2
        },
        'info_PDA12': {
            'id': 34,
            'param_cnt': 2
        },
        'info_PSP1': {
            'id': 34,
            'param_cnt': 2
        }
    },
    {
        'name': 'OSAGE_MV_CCL',
        'info_F2': {
            'id': 71,
            'param_cnt': 3
        },
        'info_FT': {
            'id': 71,
            'param_cnt': 3
        },
        'info_X': {
            'id': 71,
            'param_cnt': 3
        },
        'info_F': {
            'id': 71,
            'param_cnt': 3
        }
    },
    {
        'name': 'OSAGE_STEP',
        'info_F2': {
            'id': 70,
            'param_cnt': 3
        },
        'info_FT': {
            'id': 70,
            'param_cnt': 3
        },
        'info_X': {
            'id': 70,
            'param_cnt': 3
        },
        'info_F': {
            'id': 70,
            'param_cnt': 3
        }
    },
    {
        'name': 'PARTS_DISP',
        'info_default': {
            'id': 57,
            'param_cnt': 3
        },
        'info_PDA12': {
            'id': None,
            'param_cnt': None
        },
        'info_PSP1': {
            'id': None,
            'param_cnt': None
        }
    },
    {
        'name': 'PSE',
        'info_FT': {
            'id': 106,
            'param_cnt': 2
        }
    },
    {
        'name': 'PV_AUTH_LIGHT_PRIORITY',
        'info_F2': {
            'id': 88,
            'param_cnt': 2
        },
        'info_X': {
            'id': 88,
            'param_cnt': 2
        }
    },
    {
        'name': 'PV_BRANCH_MODE',
        'desc': 'Restrict future commands to either normal or success branch.',
        'info_default': {
            'id': 65,
            'param_cnt': 1,
            'param_info': [
                {'name': 'branch', 'desc': 'which branch to set', 'required': True, 'type': type('pv_branch_enum', (StringEnum,), {'choices': ['none', 'normal', 'success']})}
            ]
        },
        'info_PDA12': {
            'id': None,
            'param_cnt': None
        },
        'info_PSP1': {
            'id': None,
            'param_cnt': None
        },
        'info_PSP2': {
            'id': None,
            'param_cnt': None
        }
    },
    {
        'name': 'PV_CHARA_LIGHT',
        'info_F2': {
            'id': 89,
            'param_cnt': 3
        },
        'info_X': {
            'id': 89,
            'param_cnt': 3
        }
    },
    {
        'name': 'PV_END',
        'desc': 'End PV playback.',
        'info_default': {
            'id': 32,
            'param_cnt': 0
        }
    },
    {
        'name': 'PV_END_FADEOUT',
        'info_F2': {
            'id': 83,
            'param_cnt': 2
        },
        'info_FT': {
            'id': 83,
            'param_cnt': 2
        },
        'info_X': {
            'id': 83,
            'param_cnt': 2
        },
        'info_F': {
            'id': 83,
            'param_cnt': 2
        }
    },
    {
        'name': 'PV_STAGE_LIGHT',
        'info_F2': {
            'id': 90,
            'param_cnt': 3
        },
        'info_X': {
            'id': 90,
            'param_cnt': 3
        }
    },
    {
        'name': 'REFLECTION',
        'info_X': {
            'id': 79,
            'param_cnt': 2
        }
    },
    {
        'name': 'REFLECTION_QUALITY',
        'info_X': {
            'id': 82,
            'param_cnt': 2
        }
    },
    {
        'name': 'RESERVE',
        'info_F2': {
            'id': 87,
            'param_cnt': 9
        },
        'info_X': {
            'id': 117,
            'param_cnt': 2
        }
    },
    {
        'name': 'SATURATE',
        'info_default': {
            'id': 54,
            'param_cnt': 1
        },
        'info_PDA12': {
            'id': 38,
            'param_cnt': 1
        },
        'info_PSP1': {
            'id': None,
            'param_cnt': None
        }
    },
    {
        'name': 'SCENE_FADE',
        'info_default': {
            'id': 52,
            'param_cnt': 6
        },
        'info_PDA12': {
            'id': 36,
            'param_cnt': 6
        },
        'info_PSP1': {
            'id': None,
            'param_cnt': None
        }
    },
    {
        'name': 'SCENE_ROT',
        'info_default': {
            'id': 63,
            'param_cnt': 1
        },
        'info_PDA12': {
            'id': None,
            'param_cnt': None
        },
        'info_PSP1': {
            'id': None,
            'param_cnt': None
        }
    },
    {
        'name': 'SET_CAMERA',
        'info_default': {
            'id': 12,
            'param_cnt': 6
        }
    },
    {
        'name': 'SET_CHARA',
        'info_default': {
            'id': 37,
            'param_cnt': 1
        },
        'info_PDA12': {
            'id': None,
            'param_cnt': None
        },
        'info_PSP1': {
            'id': None,
            'param_cnt': None
        }
    },
    {
        'name': 'SET_MOTION',
        'desc': 'Set a character\'s motion.',
        'info_default': {
            'id': 7,
            'param_cnt': 4
        },
        'info_PDA12': {
            'id': 7,
            'param_cnt': 3
        },
        'info_PSP1': {
            'id': 7,
            'param_cnt': 3
        }
    },
    {
        'name': 'SET_PLAYDATA',
        'info_default': {
            'id': 8,
            'param_cnt': 2
        },
        'info_PDA12': {
            'id': 8,
            'param_cnt': 1
        },
        'info_PSP1': {
            'id': 8,
            'param_cnt': 1
        }
    },
    {
        'name': 'SET_STAGE_EFFECT_ENV',
        'info_X': {
            'id': 116,
            'param_cnt': 2
        }
    },
    {
        'name': 'SE_EFFECT',
        'info_F2': {
            'id': 73,
            'param_cnt': 1
        },
        'info_FT': {
            'id': 73,
            'param_cnt': 1
        },
        'info_X': {
            'id': 73,
            'param_cnt': 1
        },
        'info_F': {
            'id': 73,
            'param_cnt': 1
        }
    },
    {
        'name': 'SHADOWHEIGHT',
        'desc': 'Set the height of a character\'s shadow(?).',
        'info_default': {
            'id': 29,
            'param_cnt': 2,
            'param_info': [
                {'name': 'chara', 'desc': 'chara slot', 'required': True, 'type': int},
                {'name': 'height', 'desc': 'height (length?) of the shadow(?) (does nothing in AFT)', 'required': True, 'type': int}
            ]
        },
        'info_PDA12': {
            'id': 29,
            'param_cnt': 1,
            'param_info': [
                {'name': 'height', 'desc': 'height (length?) of the shadow(?) (does nothing in AFT)', 'required': True, 'type': int}
            ]
        },
        'info_PSP1': {
            'id': 29,
            'param_cnt': 1,
            'param_info': [
                {'name': 'height', 'desc': 'height (length?) of the shadow(?) (does nothing in AFT)', 'required': True, 'type': int}
            ]
        }
    },
    {
        'name': 'SHADOWPOS',
        'info_default': {
            'id': 33,
            'param_cnt': 3
        },
        'info_PDA12': {
            'id': 33,
            'param_cnt': 2
        },
        'info_PSP1': {
            'id': 33,
            'param_cnt': 2
        }
    },
    {
        'name': 'SHADOW_CAST',
        'info_FT': {
            'id': 90,
            'param_cnt': 2
        }
    },
    {
        'name': 'SHADOW_RANGE',
        'info_FT': {
            'id': 86,
            'param_cnt': 1
        }
    },
    {
        'name': 'SHIMMER',
        'info_F2': {
            'id': 100,
            'param_cnt': 3
        },
        'info_FT': {
            'id': 100,
            'param_cnt': 3
        },
        'info_X': {
            'id': 100,
            'param_cnt': 3
        }
    },
    {
        'name': 'SONG_EFFECT',
        'info_X': {
            'id': 112,
            'param_cnt': 3
        }
    },
    {
        'name': 'SONG_EFFECT_ALPHA_SORT',
        'info_X': {
            'id': 121,
            'param_cnt': 3
        }
    },
    {
        'name': 'SONG_EFFECT_ATTACH',
        'info_X': {
            'id': 113,
            'param_cnt': 3
        }
    },
    {
        'name': 'STAGE_EFFECT',
        'info_X': {
            'id': 111,
            'param_cnt': 2
        }
    },
    {
        'name': 'STAGE_LIGHT',
        'info_FT': {
            'id': 104,
            'param_cnt': 3
        }
    },
    {
        'name': 'STAGE_SHADOW',
        'info_X': {
            'id': 81,
            'param_cnt': 2
        }
    },
    {
        'name': 'STAGE_SHADOW_QUALITY',
        'info_X': {
            'id': 75,
            'param_cnt': 2
        }
    },
    {
        'name': 'SUBFRAMERENDER',
        'info_F2': {
            'id': 104,
            'param_cnt': 1
        }
    },
    {
        'name': 'TARGET',
        'desc': 'Add a rhythm game note.',
        'info_default': {
            'id': 6,
            'param_cnt': 7,
            'param_info': [
                {'name': 'type', 'desc': 'note type id', 'required': True, 'type': int},
                {'name': 'pos_x', 'desc': 'x position', 'required': True, 'type': fixeddecimal_3},
                {'name': 'pos_y', 'desc': 'y position', 'required': True, 'type': fixeddecimal_3},
                {'name': 'angle', 'desc': 'fly angle', 'required': True, 'type': fixeddecimal_3},
                {'name': 'dist', 'desc': 'fly distance', 'required': False, 'default': fixeddecimal_3(300000), 'type': fixeddecimal_3},
                {'name': 'amp', 'desc': 'flying wave amplitude', 'required': False, 'default': fixeddecimal_3(500), 'type': fixeddecimal_3},
                {'name': 'freq', 'desc': 'flying wave frequency', 'required': False, 'default': 0, 'type': int}
            ]
        },
        'info_FT': {
            'id': 6,
            'param_cnt': 7,
            'param_info': [
                {'name': 'type', 'desc': 'note type id', 'required': True, 'type': type('target_type_ft_enum', (StringEnum,), {'choices': [
                    'triangle', 'circle', 'cross', 'square',
                    'triangle_hold', 'circle_hold', 'cross_hold', 'square_hold',
                    'random', 'random_hold', 'repeat',
                    'unimp_star', 'slide_l', 'slide_r',
                    'unimp_chainstar', 'chainslide_l', 'chainslide_r',
                    'unk17',
                    'triangle_success', 'circle_success', 'cross_success', 'square_success',
                    'unimp_star_success', 'slide_l_success', 'slide_r_success'
                ]})},
                {'name': 'pos_x', 'desc': 'x position', 'required': True, 'type': fixeddecimal_3},
                {'name': 'pos_y', 'desc': 'y position', 'required': True, 'type': fixeddecimal_3},
                {'name': 'angle', 'desc': 'fly angle', 'required': True, 'type': fixeddecimal_3},
                {'name': 'dist', 'desc': 'fly distance', 'required': False, 'default': fixeddecimal_3(300000), 'type': fixeddecimal_3},
                {'name': 'amp', 'desc': 'flying wave amplitude', 'required': False, 'default': fixeddecimal_3(500), 'type': fixeddecimal_3},
                {'name': 'freq', 'desc': 'flying wave frequency', 'required': False, 'default': 0, 'type': int}
            ]
        },
        'info_F2': {
            'id': 6,
            'param_cnt': 12
        },
        'info_X': {
            'id': 6,
            'param_cnt': 12
        },
        'info_F': {
            'id': 6,
            'param_cnt': 11
        }
    },
    {
        'name': 'TARGET_EFFECT',
        'info_F2': {
            'id': 91,
            'param_cnt': 11
        },
        'info_X': {
            'id': 91,
            'param_cnt': 11
        }
    },
    {
        'name': 'TARGET_FLAG',
        'info_FT': {
            'id': 84,
            'param_cnt': 1
        }
    },
    {
        'name': 'TARGET_FLYING_TIME',
        'desc': 'Set the flying in time for rhythm game notes.',
        'info_default': {
            'id': 58,
            'param_cnt': 1,
            'param_info': [
                {'name': 'time', 'desc': 'flying time', 'required': True, 'type': DivaTime}
            ]
        },
        'info_PDA12': {
            'id': None,
            'param_cnt': None
        },
        'info_PSP1': {
            'id': None,
            'param_cnt': None
        }
    },
    {
        'name': 'TECH_DEMO_GESUTRE',
        'info_X': {
            'id': 149,
            'param_cnt': 2
        }
    },
    {
        'name': 'TIME',
        'desc': 'Wait until a certain game time.',
        'info_default': {
            'id': 1,
            'param_cnt': 1,
            'param_info': [{'name': 'time', 'desc': 'time to wait until', 'required': True, 'type': DivaTime}]
        }
    },
    {
        'name': 'TONE_MAP',
        'info_X': {
            'id': 77,
            'param_cnt': 2
        }
    },
    {
        'name': 'TONE_TRANS',
        'info_default': {
            'id': 53,
            'param_cnt': 6
        },
        'info_PDA12': {
            'id': 37,
            'param_cnt': 6
        },
        'info_PSP1': {
            'id': None,
            'param_cnt': None
        }
    },
    {
        'name': 'TOON',
        'info_FT': {
            'id': 99,
            'param_cnt': 3
        }
    },
    {
        'name': 'TOON_EDGE',
        'info_F2': {
            'id': 99,
            'param_cnt': 3
        },
        'info_X': {
            'id': 99,
            'param_cnt': 3
        }
    },
    {
        'name': 'TOON＿EDGE',
        'info_F2': {
            'id': 106,
            'param_cnt': 2
        }
    },
    {
        'name': 'VR_CHARA_PSMOVE',
        'info_X': {
            'id': 143,
            'param_cnt': 2
        }
    },
    {
        'name': 'VR_CHEER',
        'info_X': {
            'id': 142,
            'param_cnt': 2
        }
    },
    {
        'name': 'VR_CHEMICAL_LIGHT_COLOR',
        'info_X': {
            'id': 150,
            'param_cnt': 2
        }
    },
    {
        'name': 'VR_LIVE_CHARA_VOICE',
        'info_X': {
            'id': 162,
            'param_cnt': 2
        }
    },
    {
        'name': 'VR_LIVE_CHEER',
        'info_X': {
            'id': 154,
            'param_cnt': 5
        }
    },
    {
        'name': 'VR_LIVE_CLONE',
        'info_X': {
            'id': 156,
            'param_cnt': 7
        }
    },
    {
        'name': 'VR_LIVE_FLY',
        'info_X': {
            'id': 161,
            'param_cnt': 5
        }
    },
    {
        'name': 'VR_LIVE_GESTURE',
        'info_X': {
            'id': 155,
            'param_cnt': 3
        }
    },
    {
        'name': 'VR_LIVE_HAIR_OSAGE',
        'info_X': {
            'id': 152,
            'param_cnt': 9
        }
    },
    {
        'name': 'VR_LIVE_LOOK_CAMERA',
        'info_X': {
            'id': 153,
            'param_cnt': 9
        }
    },
    {
        'name': 'VR_LIVE_MOB',
        'info_X': {
            'id': 151,
            'param_cnt': 5
        }
    },
    {
        'name': 'VR_LIVE_MOVIE',
        'info_X': {
            'id': 141,
            'param_cnt': 2
        }
    },
    {
        'name': 'VR_LIVE_ONESHOT_EFFECT',
        'info_X': {
            'id': 158,
            'param_cnt': 6
        }
    },
    {
        'name': 'VR_LIVE_PRESENT',
        'info_X': {
            'id': 159,
            'param_cnt': 9
        }
    },
    {
        'name': 'VR_LIVE_TRANSFORM',
        'info_X': {
            'id': 160,
            'param_cnt': 5
        }
    },
    {
        'name': 'VR_LOOP_EFFECT',
        'info_X': {
            'id': 157,
            'param_cnt': 7
        }
    },
    {
        'name': 'VR_MOVE_PATH',
        'info_X': {
            'id': 144,
            'param_cnt': 2
        }
    },
    {
        'name': 'VR_SET_BASE',
        'info_X': {
            'id': 145,
            'param_cnt': 2
        }
    },
    {
        'name': 'VR_TECH_DEMO_EFFECT',
        'info_X': {
            'id': 146,
            'param_cnt': 2
        }
    },
    {
        'name': 'VR_TRANSFORM',
        'info_X': {
            'id': 147,
            'param_cnt': 2
        }
    },
    {
        'name': 'WIND',
        'info_F2': {
            'id': 69,
            'param_cnt': 3
        },
        'info_FT': {
            'id': 69,
            'param_cnt': 3
        },
        'info_X': {
            'id': 69,
            'param_cnt': 3
        },
        'info_F': {
            'id': 69,
            'param_cnt': 3
        }
    }
]

"""list of supported game names"""
dsc_db_games = ['PDA12', 'F2', 'FT', 'PSP1', 'PSP2', 'X', 'F']

"""
dsc_op_db indices for opcode ids
each entry will be a dict with keys for game names
"""
dsc_lookup_ids = {}

"""
dsc_op_db indices for opcode names
this is just a flat dictionary
"""
dsc_lookup_names = {}

def _generate_dsc_lookups():
    global dsc_lookup_ids
    global dsc_lookup_names

    for i, op in enumerate(dsc_op_db):
        dsc_lookup_names[op['name']] = i
        
        for g in dsc_db_games:
            info = op.get('info_{}'.format(g), op.get('info_default'))
            if info and info['id'] != None:
                id = info['id']
                if not id in dsc_lookup_ids:
                    dsc_lookup_ids[id] = {}
                dsc_lookup_ids[id][g] = i

_generate_dsc_lookups()