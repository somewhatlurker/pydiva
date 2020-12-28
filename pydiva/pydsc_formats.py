from re import compile as re_compile

_dsc_types = {
    'FT': {
        'header_regex': re_compile(b'....\x41\x00\x00\x00\x00\x00\x00\x00'),
        'header_output': b'\x21\x09\x05\x14\x41\x00\x00\x00\x00\x00\x00\x00',
        'endian': 'little'
    }
}