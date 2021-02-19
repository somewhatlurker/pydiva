"""
FMH3 format information for pyfmh3
"""

_construct_version = None
try:
    from construct import __version__ as _construct_version
    _construct_version = [int(v) for v in _construct_version.split('.')]
except Exception:
    # I'd rather just continue than throw an error if this fails for some reason, like versioning changes,
    # so just let _construct_version be None
    # Users following instructions should never have a low version anyway
    pass

if _construct_version:
    if (_construct_version[0] < 2) or ((_construct_version[0] == 2) and (_construct_version[1] < 9)):
        raise Exception('Construct version too low, please install version 2.9+')

from construct import Struct, Computed, Tell, Const, Padding, Padded, Pointer, RepeatUntil, Byte, Int16ul, Flag, Rebuild, If, Int32ub, Seek, Int32ul, Int64ul
from pydiva.util.cs3_file_utils import RelocationPointerAdapter, gen_relocation_struct, relocation_data_len, gen_eofc_struct, gen_cs3_file

def _gen_fmh3_struct(int_type, pointer_type, addr_mode='rel'):
    return Struct(
        "pointer_offset" / (Computed(0) if addr_mode == 'abs' else Tell),
        "signature" / Const(b'FMH3'),
        Padding(4),
        "fonts_count" / Padded(pointer_type.sizeof(), int_type),
        "fonts_pointers_offset" / pointer_type,
        "fonts" / Pointer(lambda this: this.fonts_pointers_offset + this.pointer_offset, RepeatUntil(lambda obj,lst,ctx: ctx._index >= ctx.fonts_count - 1, Struct(
            "pointer" / pointer_type,
            "data" / Pointer(lambda this: this.pointer + this._.pointer_offset, Struct(
                "id" / int_type,
                "advance_width" / Byte,
                "line_height" / Byte,
                "box_width" / Byte,
                "box_height" / Byte,
                "layout_param_1" / Byte, 
                "layout_param_2_numerator" / Byte,
                "layout_param_2_denominator" / Byte,
                Padding(1),
                "other_params?" / int_type,
                "tex_size_chars" / int_type,
                "chars_count" / int_type,
                "chars_pointer" / pointer_type,
                "chars" / Pointer(lambda this: this.chars_pointer + this._._.pointer_offset, RepeatUntil(lambda obj,lst,ctx: ctx._index >= ctx.chars_count - 1, Struct(
                    "codepoint" / Int16ul,
                    "halfwidth" / Flag,
                    Padding(1),
                    "tex_col" / Byte,
                    "tex_row" / Byte,
                    "glyph_x" / Byte,
                    "glyph_width" / Byte,
                ))),
            )),
        ))),
    )

_fmh3_types = {
    'FMH3': {
        'remarks': 'unencapsulated FT fontmap',
        'struct': _gen_fmh3_struct(Int32ul, Int32ul),
        'address_size': 4,
        'fonts_pointers_min_offset': 32,
        'nest_fmh3_data': False,
    },
    'FONM': {
        'remarks': 'X fontmap in FONM container',
        'struct': gen_cs3_file(Int32ul, Int64ul, [{
            'signature': 'FONM',
            'data_size': lambda this: this.data_size,
            'data_subcon': _gen_fmh3_struct(Int32ul, RelocationPointerAdapter(Int64ul)),
            'enrs': True,
            'relocation': True
        }]),
        'address_size': 8,
        'fonts_pointers_min_offset': 32,
        'nest_fmh3_data': 'FONM',
        'alternate_type_checks': [{'type': 'FONM_F2', 'checks': [{'offset': 15, 'mask': 0x08}]}]
    },
    'FONM_F2': {
        'remarks': 'F2nd fontmap in FONM container',
        'struct': gen_cs3_file(Int32ub, Int32ub, [{
            'signature': 'FONM',
            'data_size': lambda this: this.data_size,
            'data_subcon': _gen_fmh3_struct(Int32ub, RelocationPointerAdapter(Int32ub), addr_mode='abs'),
            'enrs': False,
            'relocation': True
        }]),
        'address_size': 4,
        'fonts_pointers_min_offset': 32 + 64, # because FONM headers are within the same address space :/
        'nest_fmh3_data': 'FONM',
    },
}