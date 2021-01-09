pydsc Documentation
===================

pydsc is designed with the goal of growing into a complete toolset for working with dsc files, including the ability to
obtain human-friendly parameter names and types, built-in string parsing and generation including tagging for syntax
highlighting or similar, and of course direct file and bytes IO like other parts of pydiva.

Most code for the above is already complete with some limitations:
- File/bytes IO has not been expanded to cover games other than Future Tone.
    I've yet to document the signatures used and variations in formats.
    This should be relatively straight-forward to implement.
- The op data used is very much incomplete.
    Thanks to the work done for Open PD Script Editor, structured data was availiable for parsing and outputting data
    already, but it lacks information necessary for parameter names, types, and op descriptions. Such information must
    be manually reverse-engineered and added to the data.

## Usage
### Op Representation
Dsc ops are represented using the pydsc.DscOp class.

DscOp has the following variables:  
`game`: name of the game to use data for (PDA12, F, F2, FT, PSP1, PSP2, X) -- only FT is fully supported currently  
`op_name`: name of the op  
`op_id`: game-specific ID of the op
`param_values`: list of ordered parametere values for the op (will be automatically converted to appropriate types)
`param_info`: information about the parameters available

`param_info` should be None, or a list where elements are dicts or None. If a list, length will be the number of params
the op takes, like param_values.  
Dicts will have `name`, `desc`, `type`, `required`. Non-required params also have `default`.  
`type` will support converting to/from bytes, str, int where applicable, as python built-in types like int do.  
If `type` is derived from `pydiva.util.stringenum.StringEnum` (`issubclass(type, StringEnum)`), use `type.choices` to
get a list of valid strings.

　

Rather than ever using DscOp's __init__, you should prefer to use these, which will setup variables for you:  
`DscOp.from_id(game='FT', op_id=0, param_values=[0])`  
`DscOp.from_name(game='FT', op_name='TIME', param_values=[0])`  
`DscOp.from_string(game='FT', op_str='TIME(0)')  
`DscOp.read_from_stream(game='FT', s=stream, endian='little')`  
param_values equal to None will generate dummy data (NOT default values)

Similarly for the reverse, you can use these for string and stream operations:  
`s = op.get_str(self, show_names=True, int_vars=False, hide_default=True)`  
`s, tags = op.get_annotated_str(self, show_names=True, int_vars=False, hide_default=True)`
`op.write_to_stream(s=stream, endian='little')`  

　

### Tags/Annotations
`tags` are a list of dicts containing `name` (name/type of tag), `start` (index), `end` (index).  
Possible tag names: 'op', 'op_name', 'param_name', 'param_value', 'invalid'.  
'invalid' tags also contain `reason`.  
'param_name' and 'param_value' tags also contain 'param_index', which is the index into param_info for its details.

Use these for operating with syntax on strings.

To generate them for an arbitrary string without converting to DscOp, use `pydiva.pydsc_util.annotate_string`:
`annotate_string(game='FT', s='TIME(0)')`  
For a DscOp, use `get_annotated_str` to obtain text and tags together.

　

### File-level operations
`pydsc.from_stream`, `pydsc.from_bytes`: use to get a list of DscOp:  
`pydsc.from_stream(s)`, `pydsc.from_bytes(b)`  
Currently only FT is supported, but in the future games will be auto-detected and specifying `game_hint` will force a
certain game.

`pydsc.to_stream`, `pydsc.to_bytes`: use to write contents of a DscOp list as binary data:  
`pydsc.to_stream(dsc, s)`, `pydsc.to_bytes(dsc, b)`

`pydsc.dsc_to_string, pydsc.dsc_to_annotated_string`: generate a string for an entire dsc file:  
`pydsc.dsc_to_annotated_string(dsc, compat_mode=False, indent=2)`  
`compat_mode` is equal to setting `show_names=False, int_vars=True, hide_default=False` on `DscOp.get_str`.
Use compat_mode if output should be readable in future versions rather than prioritising human-readability.

　

### Direct op db access
Generally this will only be necessary for resolving tags in strings to rich information.  
The data is stored in `pydiva.pydsc_op_db`.

To access data efficiently use `dsc_lookup_ids` or `dsc_lookup_names`.

`dsc_lookup_ids` is a dictionary keyed by game-specific ids. Each value is another dict where keys are game names.  
The value for a game (if it exists) in the inner dict is an index into `dsc_op_db`.

`dsc_lookup_names` is a dictionary keyed by op names. The value for a name is an index into `dsc_op_db`.

`dsc_op_db` is a list of dictionaries (one dict per opcode name).  
Opcodes have `name`, optional `desc`, and optional game-specific info dicts (`info_FT`, etc).

List of game-specific info dicts:  
  info_PDA12, info_F2, info_FT, info_PSP1, info_PSP2, info_X, info_F  
  (also info_default)

Use `info_default` if no info exists for the game you're using.  
If no game-specific or default info is found, the game doesn't support this op.  
Additionally, an id of None indicates an unsupported opcode.

Info dicts have `id`, `param_cnt`, and optional `param_info`.
`param_info` is described above as part of DscOp.


Example code:
```
op = dsc_op_db[dsc_lookup_names[op_name]]

info_key = 'info_{}'.format(game)
info = op.get(info_key, op.get('info_default', None))

if not info or not info['id']:
    raise Exception('invalid op for this game')

param_cnt = info['param_cnt`]

if 'param_info' in info:
    my_params = ''
    for i, p in enumerate(info['param_info']):
        my_params += '{}: '.format(i+1)
        if not p:
            my_params += 'Unknown/unused param\n'
            continue
        
        my_params += p['name'] + ' - ' + p['desc']
        if not p['required']:
            my_params += ' (optional, default={})'.format(p['default'])
        my_params += '\n'
```