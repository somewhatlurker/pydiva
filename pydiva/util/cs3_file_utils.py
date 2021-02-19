"""
Stuff for dealing with sectioned from CS3 engine games. (F2nd, X)

Only single-section binary files (eg. FONM, DSC) + relocation are tested, so
other stuff is probably wrong, but the intent is that is can be expanded in the
future.
"""

from construct import Adapter, Struct, Tell, Const, Rebuild, Int32ub, Int32ul, Padding, Bytes, Default, If, Seek, Probe

def gen_relocation_data(offsets):
    """
    Given a list of offsets (offsets are in multiples of pointer length),
    output bytes to put in the relocation section's data.
    """
    
    last_offset = 0
    out = b''
    for o in offsets:
        distance = o - last_offset
        
        if distance > 0x3ff:
            b = distance.to_bytes(4, byteorder='big')
            b = bytes([b[0] | 0xc0]) + b[1:]
        elif distance > 0x3f:
            b = distance.to_bytes(2, byteorder='big')
            b = bytes([b[0] | 0x80]) + b[1:]
        else:
            b = distance.to_bytes(1, byteorder='big')
            b = bytes([b[0] | 0x40]) + b[1:]
        
        out += b
        last_offset = o
    
    out_size = len(out) + 4
    out = out_size.to_bytes(4, byteorder='little', signed=False) + out # prepend length
    
    # pad to 16 bytes
    while len(out) % 16:
        out += b'\x00'
    
    return out

def relocation_data_len(offsets):
    """
    Get the length of relocation data.
    (implemnted by calling len on gen_relocation_data result)
    """
    
    return len(gen_relocation_data(offsets))

class RelocationPointerAdapter(Adapter):
    """
    Wraps the pointer type, and generates relocation data during building.
    
    Relocation data will be put in root context's extra_sections['pof1']['data']
    (root context is up one level from level that contains pointer_offset)
    """
    
    def _decode(self, obj, context, path):
        # called at parsing time to return a modified version of obj
        
        return obj

    def _encode(self, obj, context, path):
        # called at building time to return a modified version of obj
        
        io_offset = context._io.tell()
        
        # try to find the current context's pointer offset by recursing up
        pointer_offset_ctx = context
        while hasattr(pointer_offset_ctx, '_') and not hasattr(pointer_offset_ctx, 'pointer_offset'):
            pointer_offset_ctx = pointer_offset_ctx._
        pointer_offset = getattr(pointer_offset_ctx, 'pointer_offset', 0)
        
        offset = io_offset - pointer_offset
        pointer_size = self.subcon.sizeof()
        if offset % pointer_size != 0:
            raise Exception('Pointer at bad offset -- can\'t generate relocation data')
        offset = offset // pointer_size
        
        # set offset to pointer_relocation_offsets in the parent context of pointer_offset
        # -- directly in the POF section's data (DIRTY SOLUTION!)
        # (doesn't make sense to not have this when using relocation tho)
        if not 'extra_sections' in pointer_offset_ctx._:
            pointer_offset_ctx._['extra_sections'] = {}
        if not 'POF' in pointer_offset_ctx._['extra_sections']:
            pointer_offset_ctx._['extra_sections']['POF'] = {}
        if not 'data' in pointer_offset_ctx._['extra_sections']['POF']:
            pointer_offset_ctx._['extra_sections']['POF']['data'] = []
        
        pointer_offset_ctx._['extra_sections']['POF']['data'] += [offset]
        
        pointer_offset_ctx._['extra_sections']['POF']['data'].sort()
        
        return obj

class RelocationDataAdapter(Adapter):
    """Converts a list of pointer offsets into relocation section data."""
    
    def _decode(self, obj, context, path):
        # called at parsing time to return a modified version of obj
        
        return obj

    def _encode(self, obj, context, path):
        # called at building time to return a modified version of obj
        
        return gen_relocation_data(obj)

def gen_relocation_struct(pointer_type, depth):
    """
    Generates a Construct struct for a POFx (relocation) section.
    
    Required context layout for data is:
    ```
    data=relocation_offsets
    ```
    """
    
    int_type = Int32ul # seems to use little endian in F2nd fontmap
    
    return Struct(
        "pointer_offset" / Tell,
        "signature" / Const(b'POF0' if pointer_type.sizeof() == 4 else b'POF1'),
        "section_size" / Rebuild(Int32ul, lambda this: relocation_data_len(this.data)),
        "data_pointer" / Default(Int32ul, 32),
        "flags" / Const(0x00000018 if int_type == Int32ub else 0x10000000, int_type),
        "depth" / Rebuild(Int32ul, depth),
        "data_size" / Rebuild(Int32ul, lambda this: this.section_size),
        Padding(lambda this: this.data_pointer - 24),
        Seek(lambda this: this.data_pointer + this.pointer_offset),
        "data" / RelocationDataAdapter(Bytes(lambda this: this.data_size))
    )

def gen_eofc_struct(depth, fix_parent_size=None):
    """Generates a Construct struct for an EOFC (end of file) section."""
    
    int_type = Int32ul # seems to use little endian in F2nd fontmap
    
    return Struct(
        "pointer_offset" / Tell,
        "signature" / Const(b'EOFC'),
        "section_size" / Rebuild(Int32ul, 0),
        "data_pointer" / Rebuild(Int32ul, 32),
        "flags" / Const(0x00000018 if int_type == Int32ub else 0x10000000, int_type),
        "depth" / Rebuild(Int32ul, depth),
        "data_size" / Rebuild(Int32ul, 0),
        Padding(lambda this: this.data_pointer - 24),
        Seek(lambda this: this.data_pointer + this.pointer_offset),
        Rebuild(Bytes(lambda this: this.data_size), b''),
        "parent_size_fix" / If(fix_parent_size, Struct(
            "end_offset" / Tell,
            Seek(lambda this: this._._.section_outer.section.section_size_offset),
            Rebuild(int_type, lambda this: this.end_offset - (this._._.section_outer.section.data_pointer + this._._.section_outer.section.pointer_offset)),
            Seek(lambda this: this.end_offset)
        ))
    )

def gen_section_struct(int_type, pointer_type, signature, depth, data_size=0, data_subcon=Bytes(lambda this: this.data_size), enrs=False, relocation=False, optional=False):
    """
    Generates a Construct scruct for an arbitrary section, with user-defined
    signature, data_size (can be lambda), and data subcon.
    enrs and relocation are optional (enrs only so parsing won't fail), and the
    entire section can be made optional.
    
    Optional sections are skipped if not present during parsing, and always
    skipped during building.
    
    To read data_size from section dict when building, you can use
    `lambda this: this.data_size`.
    
    Required context layout for data is:
    ```
    section_outer=dict(
        section=dict(
            data_pointer=32,
            data=b'Sample Data',
            extra_sections=dict() # needed to avoid KeyError during build with relocation
        )
    )
    ```
    """
    
    return "section_outer" / If(lambda this: this._parsing or not optional, Struct(
        "signature_first_pass" / Rebuild(Bytes(4), signature.encode('ascii')),
        Seek(lambda this: this._io.tell() - 4),
        "section" / If(lambda this: this.signature_first_pass == signature.encode('ascii') or not optional, Struct(
            "pointer_offset" / Tell,
            "signature" / Const(signature.encode('ascii')),
            "section_size_offset" / Tell, # for fixing section_size later 
            "section_size" / Default(Int32ul, 0),
            "data_pointer" / Default(Int32ul, 32),
            #Probe(),
            "flags" / Const(0x00000018 if int_type == Int32ub else 0x10000000, int_type),
            "depth" / Rebuild(Int32ul, depth),
            "data_size" / Rebuild(Int32ul, data_size),
            Padding(lambda this: this.data_pointer - 24),
            Seek(lambda this: this.data_pointer + this.pointer_offset),
            "data" / Default(data_subcon, b''),
            Seek(lambda this: this.data_pointer + this.data_size + this.pointer_offset),
            "extra_sections" / Struct(
                # I think enrs may come before or after relocation(?), so just try reading it from both
                gen_section_struct(int_type, pointer_type, 'ENRS', depth, optional=True) if enrs else Tell,
                "POF" / gen_relocation_struct(pointer_type, depth) if relocation else Tell,
                gen_section_struct(int_type, pointer_type, 'ENRS', depth, optional=True) if enrs else Tell,
                "end_offset" / Tell,
                Seek(lambda this: this._.section_size_offset),
                Rebuild(Int32ul, lambda this: this.end_offset - (this._.data_pointer + this._.pointer_offset)),
                Seek(lambda this: this.end_offset)
            ),
        ))
    ))

def gen_cs3_sections(int_type, pointer_type, sections, depth=0):
    """
    Generates a Construct scruct for multiple sections, including children,
    from a list of info dicts.
    
    My understanding is that these should be structured in the file like:
    [
        SECTION_MAIN
        SECTION_ENRS
        SECTION_POF
        SECTION_CHILDREN // may have nested complete sections
        SECTION_EOF
    ]
    but this is based only on skimming some MikuMikuLibrary code and I never checked it lol
    
    Info dicts must have:
    signature
    
    Info dicts may have:
    data_size, data_subcon (by default, will use 0 length and Bytes),
    enrs, relocation (set to enable sections - enrs only so parsing won't fail),
    optional (set to make this section optional to read, and disable building),
    child_sections (info list for this section's children)
    
    To read data_size from section dict when building, you can use
    `lambda this: this.data_size`.
    
    Required context layout for data is:
    (well, intended context...  this isn't very tested yet)
    ```
    '[SIGNATURE]': {
        section_outer=dict(
            section=dict(
                data_pointer=32,
                data=b'Sample Data',
                extra_sections=dict() # needed to avoid KeyError during build with relocation
            )
        ),
        '[CHILD0_SIG]'=dict(
            section_outer=dict(
                section=dict(
                    data_pointer=32,
                    data=b'Sample Data',
                    extra_sections=dict() # needed to avoid KeyError during build
                )
            ),
            '[CH0_CH1_SIG]'=dict(
                ...
            )
        )
        ...
    }
    ```
    """
    
    if len(sections) == 0:
        return Struct()
    
    struct = Struct()
    for s in sections:
        ss = gen_section_struct(int_type, pointer_type, s['signature'], depth, s.get('data_size', 0), s.get('data_subcon', Bytes(lambda this: this.data_size)), s.get('enrs'), s.get('relocation'), s.get('optional'))
        
        cs = gen_cs3_sections(int_type, pointer_type, s.get('child_sections', []), depth + 1)
        ss += cs
        
        ss += "EOFC" / gen_eofc_struct(depth, s['signature'])
        struct += s['signature'] / ss
    
    return struct

def gen_cs3_file(int_type, pointer_type, sections):
    """
    Generates a Construct scruct for a file with multiple sections, including
    children, from a list of info dicts.
    
    Same as gen_cs3_sections but with an end of file section appended.
    """
    
    return gen_cs3_sections(int_type, pointer_type, sections) + gen_eofc_struct(0)