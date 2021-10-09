_dsc_types = {
    'FT': {
        # Besides the different signatures, all Arcade dscs have the same opcode length afaik
        # Just new opcodes in newer dscs
        'signatures': [b'\x17\x25\x12\x15', b'\x21\x09\x05\x14'],
        # Just setting to 0x15122517 here because the game won't care
        'header_output': b'\x17\x25\x12\x15',
        'endian': 'little'
    },
    'F': {
        'signatures': [b'\x20\x02\x02\x12'],
        'header_output': b'\x20\x02\x02\x12',
        'endian': 'little'
    }
}