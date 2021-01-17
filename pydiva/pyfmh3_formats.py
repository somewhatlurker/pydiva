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

from construct import Struct, Tell, Const, Padding, Padded, Pointer, RepeatUntil, Byte, Int16ul, Flag, Rebuild, If, Int32ub, Seek, Int32ul, Int64ul
from pydiva.util.cs3_file_utils import RelocationPointerAdapter, gen_relocation_struct, relocation_data_len, gen_eofc_struct, gen_cs3_file

def _gen_fmh3_struct(int_type, pointer_type):
    return Struct(
        "pointer_offset" / Tell,
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

def _gen_fonm_struct(int_type, pointer_type):
    return Struct(
        "pointer_offset" / Tell,
        "signature" / Const(b'FONM'),
        "section_size_offset" / Tell,
        "section_size" / Rebuild(int_type, lambda this: 0), # this is written later when building
        "data_pointer" / int_type,
        "flags" / Const(0x18000000 if int_type == Int32ub else 0x10000000, int_type),
        "depth" / Const(0, int_type),
        "data_size" / int_type,
        "data" / Pointer(lambda this: this.data_pointer + this.pointer_offset, _gen_fmh3_struct(int_type, RelocationPointerAdapter(pointer_type))),
        # Seek(lambda this: this.data_pointer + this.data_size),
        # ENRS (endian reversal) ignored
        "extra_sections" / If(lambda this: this._building, Struct(
            "POF" / Pointer(lambda this: this._.data_pointer + this._.data_size + this._.pointer_offset, gen_relocation_struct(int_type, pointer_type)),
            # dirty hack to rewrite section_size (POF data size is unavailable during initial build)
            "build_pos" / Tell,
            Seek(lambda this: this._.section_size_offset),
            "section_size_proper" / Rebuild(int_type, lambda this: this._.data_size + relocation_data_len(this.POF.data) + 32 + 32),
            Seek(lambda this: this.build_pos),
            
            Pointer(lambda this: this._.data_pointer + this._.data_size + this._.pointer_offset + relocation_data_len(this.POF.data) + 32, gen_eofc_struct(int_type)),
            Pointer(lambda this: this._.data_pointer + this.section_size_proper + this._.pointer_offset, gen_eofc_struct(int_type)),
        )),
    )

_fmh3_types = {
    'FMH3': {
        'remarks': 'unencapsulated FT fontmap',
        'struct': _gen_fmh3_struct(Int32ul, Int32ul),
        'address_size': 4,
        'nest_fmh3_data': False,
    },
    'FONM': {
        'remarks': 'X fontmap in FONM container',
        #'struct': _gen_fonm_struct(Int32ul, Int64ul),
        'struct': gen_cs3_file(Int32ul, Int64ul, [{
            'signature': 'FONM',
            'data_size': lambda this: this.data_size,
            'data_subcon': _gen_fmh3_struct(Int32ul, RelocationPointerAdapter(Int64ul)),
            'enrs': True,
            'relocation': True
        }]),
        'address_size': 8,
        'nest_fmh3_data': 'FONM',
    },
}