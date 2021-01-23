"""
Utils for processing dsc-related stuff.
"""

from pydiva.pydsc_op_db import dsc_op_db, dsc_db_games, dsc_lookup_ids, dsc_lookup_names

def fix_param_types(param_values, param_info):
    """
    Corrects parameter types
    """
    
    param_values = param_values.copy()
    
    for i in range(len(param_values)):
        if type(param_values[i]) == str and param_values[i].startswith('i'):
            try:
                param_values[i] = int(param_values[i][1:])
                continue
            except Exception:
                pass # maybe it's still legit for an enum
        
        if param_values[i] == '':
            param_values[i] = None
        
        if param_info[i]:
            # resolve None types to correct initial type
            if param_values[i] == None:
                if param_info[i]['required']:
                    raise Exception('Missing required parameter {}'.format(param_info[i]['name']))
                else:
                    param_values[i] = param_info[i]['default']
            
            t = param_info[i]['type']
        else:
            if param_values[i] == None:
                param_values[i] = 0
            t = int
        
        if t == bool and type(param_values[i]) == str:
            param_values[i] = param_values[i].lower() in ['t', 'true', '1']
        else:
            param_values[i] = t(param_values[i])
    
    return param_values

def fix_param_cnt(param_values, param_cnt):
    """
    Add placeholder parameters for missing params.
    If param_values is None, generate dummy data instead.
    """
    
    if param_values == None:
        pvalues = [0 for i in range(0, param_cnt)]
    elif len(param_values) > param_cnt:
        raise Exception('Too many values (expected {})'.format(param_cnt))
    else:
        pvalues = param_values
        while len(param_values) < param_cnt:
            pvalues += [None]
    
    return pvalues

def reorder_named_args(param_list, param_info):
    """
    Converts a split param string list with named args into positional args.
    This is not a strictly robust conversion, but instead non-named arguments from anywhere in the list
    will be moved around to fit in the named ones where they belong.
    """
    
    nparam_move_map = []
    seen_target_pos = []
    
    # build a mapping of parameters that need to be moved and remove the name from them
    for i, p in enumerate(param_list):
        if '=' in p:
            pname, pval = p.split('=', 1)
            pname = pname.strip().lower()
            pval = pval.strip()
            found_target = False
            for j, q in enumerate(param_info):
                if q and q['name'] == pname:
                    if j in seen_target_pos:
                        raise Exception('Duplicate parameter: {}'.format(pname))
                    nparam_move_map += [(i, j)]
                    seen_target_pos += [j]
                    found_target = True
            
            if not found_target:
                raise ValueError('Unknown parameter name: {}'.format(pname))
            
            param_list[i] = pval
    
    
    captured_args = []
    
    # sort the move map by reverse source position
    nparam_move_map.sort(key=lambda p: p[0], reverse=True)
    # remove and store the desired args, update nparam_move_map to be based on captured_args
    for i, p in enumerate(nparam_move_map):
        captured_args += [param_list.pop(p[0])]
        nparam_move_map[i] = (i, p[1])
    
    # sort the move map by insertion position
    nparam_move_map.sort(key=lambda p: p[1])
    # insert the args
    for i, j in nparam_move_map:
        param_list.insert(j, captured_args[i])
    
    return param_list

def find_param_order(param_list, param_info, flag_invalids=False):
    """
    Takes a split param string with named args and returns a list of ordered parameter indices for inputs.
    This is not a strictly robust conversion, but instead non-named arguments from anywhere in the list
    will be moved around to fit in the named ones where they belong.
    
    flag_invalids will make invalid args correspond to an error string instead of throwing Exceptions.
    """
    
    nparam_move_map = {}
    invalid_inputs = []
    
    # build a mapping of parameters that need to be moved
    for i, p in enumerate(param_list):
        if '=' in p:
            pname = p.split('=', 1)[0]
            pname = pname.strip().lower()
            found_target = False
            for j, q in enumerate(param_info):
                if q and q['name'] == pname:
                    if j in nparam_move_map.values():
                        if flag_invalids:
                            invalid_inputs += [i]
                            j = 'duplicate parameter'
                        else:
                            raise Exception('Duplicate parameter: {}'.format(pname))
                    nparam_move_map[i] = j
                    found_target = True
            
            if not found_target:
                if flag_invalids:
                    invalid_inputs += [i]
                    nparam_move_map[i] = 'unknown parameter name'
                else:
                    raise ValueError('Unknown parameter name: {}'.format(pname))
        else:
            nparam_move_map[i] = None
    
    
    # now nparam_move_map contains {input_pos: ordered_pos} for named args,
    # it can have the unnamed input params filled in where ordered_pos is None
    for i, p in nparam_move_map.items():
        if p == None and not i in invalid_inputs:
            # find first unused ordered_pos -- slow loop, but there are never
            # enough params for it to really matter
            for j in range(0, len(nparam_move_map)):
                if not j in nparam_move_map.values():
                    p = j
                    break
            
            if p == None:
                raise Exception('Unknown error reordering parameters (pos {})'.format(i))
            
            if p >= len(param_info):
                p = 'too many parameters'
            
            nparam_move_map[i] = p
    
    return [p[1] for p in sorted(nparam_move_map.items(), key=lambda x: x[0])]


def annotate_string(game, s):
    """
    Annotates a string as returned by DscOp.get_str and returns the generated tags.
    Output is a list of dicts: [{'start': 0, 'end': 5, 'name': 'op'},...].
    
    list of tag names:
    'op': from the DscOp's op_name until the op parameters' closing parenthesis
    'op_name': just the op's name, excluding values and parenthesis
    'param_name': param's name, including = sign, if present
    'param_value': param's value
    'invalid': for when something doesn't seem right
    
    param tags will also contain 'param_index', which is the index into
    param_info for its details
    
    invalid tags will also contain 'reason', which is an error message
    """
    
    ws_chars = ' 　\r\n'
    tags = []
    
    # strip whitespace from end because we don't care about it
    # and it won't affect indices
    # also makes the end of the op itself be at len(op_str), which is nice
    op_str = s.rstrip()
    
    # awkward pattern to get string's start offset (first non-whitespace
    # character) in a relatively efficient manner
    op_str_offset = 0
    while op_str_offset < len(op_str) and op_str[op_str_offset] in ws_chars:
        op_str_offset += 1
    
    # couldn't find any content
    if op_str_offset == len(op_str):
        return tags
    
    # remove semicolon if present and re-strip
    if op_str.endswith(';'):
        op_str = op_str[:-1]
        op_str = op_str.rstrip()
     
    # basic formatting check, can't continue if it fails
    # (should have some text, then parenthesis, and nested parenthesis are disallowed)
    if op_str.count('(') != 1 or op_str.count(')') != 1 or op_str[op_str_offset] == '(' or not op_str.endswith(')'):
        tags += [{'start': op_str_offset, 'end': len(op_str), 'name': 'invalid', 'reason': 'bad format'}]
        return tags
    
    tags += [{'start': op_str_offset, 'end': len(op_str), 'name': 'op'}]
    
    # op_name is whatever comes before parenthesis open
    op_name_offset = op_str_offset
    op_name = op_str[op_name_offset:].split('(', 1)[0].rstrip().upper()
    
    # don't bother continuing onto params if the op name isn't even correct
    tags += [{'start': op_name_offset, 'end': op_name_offset + len(op_name), 'name': 'op_name'}]
    if not op_name in dsc_lookup_names:
        tags += [{'start': op_name_offset, 'end': op_name_offset + len(op_name), 'name': 'invalid', 'reason': 'unknown op name'}]
        return tags
    
    op_info = dsc_op_db[dsc_lookup_names[op_name]]
    op_game_info = op_info.get('info_{}'.format(game), op_info.get('info_default'))
    if not op_game_info or op_game_info['id'] == None:
        tags += [{'start': op_name_offset, 'end': op_name_offset + len(op_name), 'name': 'invalid', 'reason': 'op not valid for game {}'.format(game)}]
        return tags
    
    # do regular splitting stuff to resolve order easily, even though we'll
    # iterate to preserve index when applying tags
    param_values = op_str.split('(', 1)[1].split(')')[0]
    param_values = [p.strip() for p in param_values.split(',')]
    if op_game_info['param_cnt'] == 0 and param_values == ['']: # remove empty str for zero parameters
        param_values = []
    
    param_info = op_game_info.get('param_info')
    
    if param_info:
        param_ordered_indices = find_param_order(param_values, param_info, flag_invalids=True)
        
        for i, p in enumerate(param_info):
            if not p:
                continue
            
            if p['required']:
                if i in param_ordered_indices:
                    param_value_idx = param_ordered_indices.index(i)
                    if param_value_idx >= 0 and param_value_idx < len(param_values):
                        param_text = param_values[param_value_idx]
                        param_text = param_text.split('=', 1)[-1]
                        if param_text.strip():
                            continue # param is good
                
                tags += [{'start': op_str.find('('), 'end': len(op_str), 'name': 'invalid', 'reason': 'missing required parameter {}'.format(p['name'])}]
    else:
        param_ordered_indices = list(range(0, op_game_info['param_cnt']))
        while len(param_ordered_indices) < len(param_values):
            param_ordered_indices += ['too many parameters']
    
    
    # parse and tag all params (fun!)
    op_param_cur_pos = op_str.find('(') + 1
    op_param_cur_num = 0
    while op_param_cur_num < len(param_values):
        # find start of actual text instead of just being in the right syntax area
        while op_str[op_param_cur_pos] in ws_chars:
            op_param_cur_pos += 1
        
        # find end of the syntax area
        op_param_cur_end = op_str.find(',', op_param_cur_pos)
        if op_param_cur_end == -1:
            op_param_cur_end = op_str.find(')', op_param_cur_pos)
        
        # and find the actual end of the token
        op_param_cur_end_stripped = op_param_cur_end # keep stripped ver separate so can get og index later
        while op_param_cur_end_stripped > op_param_cur_pos and op_str[op_param_cur_end_stripped - 1] in ws_chars:
            op_param_cur_end_stripped -= 1
        
        ordered_pos = param_ordered_indices[op_param_cur_num]
        
        # ordered_pos not int indicates an invalid param, ordered_pos contains the reason
        if type(ordered_pos) != int:
            tags += [{'start': op_param_cur_pos, 'end': op_param_cur_end_stripped, 'name': 'invalid', 'reason': str(ordered_pos)}]
        else:
            eq_pos = op_str.find('=', op_param_cur_pos, op_param_cur_end_stripped)        
            if eq_pos == -1:
                value_start_pos = op_param_cur_pos
                value_end_pos = op_param_cur_end_stripped
                
                tags += [{'start': value_start_pos, 'end': value_end_pos, 'name': 'param_value', 'param_index': ordered_pos}]
            else:
                value_pos = eq_pos + 1
                while op_str[value_pos] in ws_chars:
                    value_pos += 1
                
                name_end_pos = eq_pos
                # below commented code is for if it doesn't include equal sign in name
                #while op_str[name_end_pos - 1] in ws_chars:
                #    name_end_pos -= 1
                
                value_start_pos = value_pos
                value_end_pos = op_param_cur_end_stripped
                
                # if param_info doesn't exist, we shouldn't have a name so output an error instead of the normal tag
                if not param_info:
                    tags += [{'start': op_param_cur_pos, 'end': value_end_pos, 'name': 'invalid', 'reason': 'unknown parameter name'}]
                else:
                    tags += [{'start': op_param_cur_pos, 'end': name_end_pos+1, 'name': 'param_name', 'param_index': ordered_pos}]
                    tags += [{'start': value_start_pos, 'end': value_end_pos, 'name': 'param_value', 'param_index': ordered_pos}]
            
            # get and check type of arg
            forced_int = False
            if op_str[value_start_pos] == 'i':
                try:
                    int(op_str[value_start_pos+1:value_end_pos])
                    forced_int = True
                except Exception:
                    pass # maybe it's still legit for an enum
            
            if not forced_int:
                if param_info and param_info[ordered_pos]:
                    t = param_info[ordered_pos]['type']
                else:
                    t = int
                
                try:
                    if t == bool:
                        op_str[value_start_pos:value_end_pos].lower() in ['t', 'true', '1']
                    else:
                        t(op_str[value_start_pos:value_end_pos])
                except Exception as e:
                    tags += [{'start': value_start_pos, 'end': value_end_pos, 'name': 'invalid', 'reason': 'cannot convert to correct type ({})'.format(e)}]
        
        op_param_cur_pos = op_param_cur_end + 1
        op_param_cur_num += 1
    
    return tags