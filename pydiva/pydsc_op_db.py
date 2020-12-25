"""
list of dictionaries (one dict per opcode name)
opcodes have name, optional description, and optional game-specific info dicts

list of game-specific info dict keys:
  info_A12, info_F2, info_FT, info_PSP1, info_PSP2, info_X, info_f
  (also info_default)

use info_default if no info exists for the game you're parsing
if no game-specific or default info is found, the game is not supported

additionally, an id of None indicates an unsupported opcode
"""
dsc_op_db = [
    {
        'name': 'AGEAGE_CTRL',
        'info_FT': {
            'id': 105,
            'param_cnt': 8
        }
    },
    {
        'name': 'AIM',
        'info_default': {
            'id': 46,
            'param_cnt': 3
        },
        'info_A12': {
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
        'name': 'AOTO_CAP',
        'info_FT': {
            'id': 97,
            'param_cnt': 1
        }
    },
    {
        'name': 'AUTO_BLINK',
        'info_default': {
            'id': 56,
            'param_cnt': 2
        },
        'info_A12': {
            'id': None,
            'param_cnt': None
        },
        'info_PSP1': {
            'id': None,
            'param_cnt': None
        }
    },
    {
        'name': 'AUTO_CAPTURE_BEGIN',
        'info_F2': {
            'id': 97,
            'param_cnt': 1
        },
        'info_X': {
            'id': 97,
            'param_cnt': 1
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
        'info_default': {
            'id': 28,
            'param_cnt': 2
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
        'info_F2': {
            'id': 93,
            'param_cnt': 2
        },
        'info_FT': {
            'id': 93,
            'param_cnt': 2
        },
        'info_X': {
            'id': 93,
            'param_cnt': 2
        }
    },
    {
        'name': 'CHANGE_FIELD',
        'info_default': {
            'id': 14,
            'param_cnt': 1
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
        'info_F2': {
            'id': 96,
            'param_cnt': 4
        },
        'info_FT': {
            'id': 96,
            'param_cnt': 4
        },
        'info_X': {
            'id': 96,
            'param_cnt': 4
        }
    },
    {
        'name': 'CHARA_COLOR',
        'info_F2': {
            'id': 72,
            'param_cnt': 2
        },
        'info_FT': {
            'id': 72,
            'param_cnt': 2
        },
        'info_X': {
            'id': 72,
            'param_cnt': 2
        },
        'info_f': {
            'id': 72,
            'param_cnt': 2
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
        'info_A12': {
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
        'info_A12': {
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
        'info_default': {
            'id': 59,
            'param_cnt': 2
        },
        'info_A12': {
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
        'info_A12': {
            'id': 35,
            'param_cnt': 1
        },
        'info_PSP1': {
            'id': 35,
            'param_cnt': 1
        }
    },
    {
        'name': 'COLOR_COLLE',
        'info_FT': {
            'id': 94,
            'param_cnt': 3
        }
    },
    {
        'name': 'COLOR_CORRECTION',
        'info_F2': {
            'id': 94,
            'param_cnt': 3
        },
        'info_X': {
            'id': 94,
            'param_cnt': 3
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
        'info_default': {
            'id': 13,
            'param_cnt': 2
        }
    },
    {
        'name': 'DATA_CAMERA_START',
        'info_F2': {
            'id': 66,
            'param_cnt': 2
        },
        'info_FT': {
            'id': 66,
            'param_cnt': 2
        },
        'info_X': {
            'id': 66,
            'param_cnt': 2
        },
        'info_f': {
            'id': 66,
            'param_cnt': 2
        }
    },
    {
        'name': 'DOF',
        'info_F2': {
            'id': 95,
            'param_cnt': 3
        },
        'info_FT': {
            'id': 95,
            'param_cnt': 3
        },
        'info_X': {
            'id': 95,
            'param_cnt': 3
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
        'info_A12': {
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
        'info_f': {
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
        'info_A12': {
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
        'info_A12': {
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
        'info_f': {
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
        'info_A12': {
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
        'info_A12': {
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
        'info_f': {
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
        'info_f': {
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
        'info_A12': {
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
        'info_A12': {
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
        'info_f': {
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
        'info_A12': {
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
        'info_default': {
            'id': 34,
            'param_cnt': 2
        },
        'info_A12': {
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
        'info_F2': {
            'id': 82,
            'param_cnt': 1
        },
        'info_FT': {
            'id': 82,
            'param_cnt': 1
        },
        'info_f': {
            'id': 82,
            'param_cnt': 1
        }
    },
    {
        'name': 'EDIT_MOTION',
        'info_default': {
            'id': 27,
            'param_cnt': 4
        },
        'info_A12': {
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
        'info_f': {
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
        'info_f': {
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
        'info_A12': {
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
        'info_f': {
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
        'info_A12': {
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
        'info_f': {
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
        'info_A12': {
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
        'info_A12': {
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
        'info_A12': {
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
        'desc': 'Ends the DSC file.',
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
        'info_A12': {
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
        'info_A12': {
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
        'info_A12': {
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
        'info_A12': {
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
        'info_A12': {
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
        'info_FT': {
            'id': 87,
            'param_cnt': 3
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
        'info_A12': {
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
        'info_A12': {
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
        'info_A12': {
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
        'info_A12': {
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
        'info_default': {
            'id': 24,
            'param_cnt': 2
        },
        'info_A12': {
            'id': 24,
            'param_cnt': 1
        },
        'info_PSP1': {
            'id': 24,
            'param_cnt': 1
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
        'info_F2': {
            'id': 98,
            'param_cnt': 1
        },
        'info_X': {
            'id': 98,
            'param_cnt': 1
        }
    },
    {
        'name': 'MAN_CAP',
        'info_FT': {
            'id': 98,
            'param_cnt': 1
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
        'info_default': {
            'id': 4,
            'param_cnt': 2
        },
        'info_A12': {
            'id': 4,
            'param_cnt': 1
        },
        'info_PSP1': {
            'id': 4,
            'param_cnt': 1
        }
    },
    {
        'name': 'MIKU_MOVE',
        'info_default': {
            'id': 2,
            'param_cnt': 4
        },
        'info_A12': {
            'id': 2,
            'param_cnt': 3
        },
        'info_PSP1': {
            'id': 2,
            'param_cnt': 3
        }
    },
    {
        'name': 'MIKU_ROT',
        'info_default': {
            'id': 3,
            'param_cnt': 2
        },
        'info_A12': {
            'id': 3,
            'param_cnt': 1
        },
        'info_PSP1': {
            'id': 3,
            'param_cnt': 1
        }
    },
    {
        'name': 'MIKU_SHADOW',
        'info_default': {
            'id': 5,
            'param_cnt': 2
        },
        'info_A12': {
            'id': 5,
            'param_cnt': 1
        },
        'info_PSP1': {
            'id': 5,
            'param_cnt': 1
        }
    },
    {
        'name': 'MODE_SELECT',
        'info_default': {
            'id': 26,
            'param_cnt': 2
        },
        'info_A12': {
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
        'info_default': {
            'id': 19,
            'param_cnt': 5
        },
        'info_A12': {
            'id': 19,
            'param_cnt': 3
        },
        'info_PSP1': {
            'id': 19,
            'param_cnt': 3
        }
    },
    {
        'name': 'MOVE_CAMERA',
        'info_default': {
            'id': 31,
            'param_cnt': 21
        },
        'info_A12': {
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
        'info_F2': {
            'id': 68,
            'param_cnt': 1
        },
        'info_FT': {
            'id': 68,
            'param_cnt': 1
        },
        'info_X': {
            'id': 68,
            'param_cnt': 1
        },
        'info_f': {
            'id': 68,
            'param_cnt': 1
        }
    },
    {
        'name': 'MOVIE_PLAY',
        'info_F2': {
            'id': 67,
            'param_cnt': 1
        },
        'info_FT': {
            'id': 67,
            'param_cnt': 1
        },
        'info_X': {
            'id': 67,
            'param_cnt': 1
        },
        'info_f': {
            'id': 67,
            'param_cnt': 1
        }
    },
    {
        'name': 'MUSIC_PLAY',
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
        'info_A12': {
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
        'info_f': {
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
        'info_f': {
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
        'info_A12': {
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
        'info_F2': {
            'id': 65,
            'param_cnt': 1
        },
        'info_FT': {
            'id': 65,
            'param_cnt': 1
        },
        'info_X': {
            'id': 65,
            'param_cnt': 1
        },
        'info_f': {
            'id': 65,
            'param_cnt': 1
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
        'desc': 'Ends PV playback.',
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
        'info_f': {
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
        'info_A12': {
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
        'info_A12': {
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
        'info_A12': {
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
        'info_A12': {
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
        'info_default': {
            'id': 7,
            'param_cnt': 4
        },
        'info_A12': {
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
        'info_A12': {
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
        'info_f': {
            'id': 73,
            'param_cnt': 1
        }
    },
    {
        'name': 'SHADOWHEIGHT',
        'info_default': {
            'id': 29,
            'param_cnt': 2
        },
        'info_A12': {
            'id': 29,
            'param_cnt': 1
        },
        'info_PSP1': {
            'id': 29,
            'param_cnt': 1
        }
    },
    {
        'name': 'SHADOWPOS',
        'info_default': {
            'id': 33,
            'param_cnt': 3
        },
        'info_A12': {
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
        'info_default': {
            'id': 6,
            'param_cnt': 7
        },
        'info_F2': {
            'id': 6,
            'param_cnt': 12
        },
        'info_X': {
            'id': 6,
            'param_cnt': 12
        },
        'info_f': {
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
        'info_default': {
            'id': 58,
            'param_cnt': 1
        },
        'info_A12': {
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
            'params_info': [{'desc': 'time to wait until', 'type': 'int'}]
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
        'info_A12': {
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
        'info_f': {
            'id': 69,
            'param_cnt': 3
        }
    }
]