pyfmh3 Documentation
====================

pyfmh3 supports FMH3 files from FT series games (AFT/FT/M39) and FMH3 in FONM container for F2nd (BE only) and X games.

## Usage
### Dictionary Representation
The main API makes use of nested python dictionaries and lists to represent data:
```
{
    'fmh3_type': 'FMH3',             # format-specific signature (FMH3/FONM/FONM_F2)
    'fonts': [                       # list of fonts in the fontmap
        {                            # each font is a dictionary
            'id': 0,
            'advance_width': 36,
            'line_height': 36,
            'box_width': 35,
            'box_height': 46,
            'layout_param_1': 3,
            'layout_param_2_numerator': 1,
            'layout_param_2_denominator': 2,
            'other_params?': 0,
            'tex_size_chars': 117,
            'chars': [               # chars is another list of dictionaries
                {
                    'codepoint': 32,
                    'halfwidth': True,
                    'tex_col': 0,
                    'tex_row': 0,
                    'glyph_x': 3,
                    'glyph_width': 12
                }
            ]
        }
    ]
}
```

### Reading Data
Use `pyfmh3.from_stream` or `pyfmh3.from_bytes` to convert raw data to the dictionary representation.  
Example:
```
with open('test.bin', 'rb') as f:
    fmh_from_stream = pyfmh3.from_stream(f)
    
    f.seek(0)
    fmh_from_bytes = pyfmh3.from_bytes(f.read())
```

`pyfmh3.UnsupportedFmh3TypeException` will be raised if the supplied file is not a known FMH3 fontmap type.


### Writing Data
Use `pyfmh3.to_stream` or `pyfmh3.to_bytes` to convert the dictionary representation to raw data.  
Example:
```
fmhdata = {'fmh3_type': 'FMH3', 'fonts': [...]}
with open('test.bin', 'wb') as f:
    pyfmh3.to_stream(fmhdata, f)
fmh_to_bytes = pyfmh3.to_bytes(fmhdata, no_copy=True)
```

Setting `no_copy` provides a speedup and memory usage reduction, but the input will be contaminated with internal data
created during processing. Only enable this if you won't reuse the dictionary.

`pyfmh3.UnsupportedFmh3TypeException` will be raised if the fmh3_type is unknown.

　

## Development Info
FMH3 format for FT series games is described in `docs/fmh3_format.txt`, but the Struct in `pydiva/pyfmh3_formats.py` is
probably just as easy to understand.
X is similar but some fields become 64 bits long and it's encapsulated in an F2nd/X style file with FONM magic.  
F2nd (BE) is also similar, but the FMH3 data is big endian.
MikuMikuModel serves as a good reference for how the sectioned F2nd/X files work.