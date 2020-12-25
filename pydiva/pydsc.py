"""
pydsc reader and writer for Project Diva DSC files
"""

from pydiva.pydsc_op_db import dsc_op_db, dsc_db_games, dsc_lookup_ids, dsc_lookup_names

class UnsupportedDscGameException(Exception):
    pass

class UnknownDscOpException(Exception):
    pass

def _fix_param_types(param_values, param_info, enum_dir='to_str'):
    """
    Corrects parameter types and resolves enums to strings for easier handling
    """
    
    param_values = param_values.copy()
    
    for i in range(len(param_values)):
        if param_values[i] == '':
            param_values[i] = 0
        
        if param_info[i]:
            t = param_info[i]['type']
        else:
            t = int
        
        if t == 'enum':
            if enum_dir == 'to_str':
                v = int(param_values[i])
                if v < 0 or v >= len(param_info[i]['enum_choices']):
                    raise KeyError('Invalid enum value {} for param {}'.format(v, param_info[i]['name']))
                else:
                    param_values[i] = param_info[i]['enum_choices'][v]
            elif enum_dir == 'from_str':
                v = str(param_values[i])
                try:
                    param_values[i] = int(param_info[i]['enum_choices'].index(v))
                except ValueError:
                    raise KeyError('Invalid enum value {} for param {}'.format(v, param_info[i]['name']))
            elif enum_dir != 'none':
                raise ValueError('Invalid enum_dir: {}'.format(enum_dir))
        else:
            param_values[i] = t(param_values[i])
    
    return param_values

def _reorder_named_args(param_list, param_info):
    """
    Converts a split param string with named args into the positional args.
    This is not a strictly robust conversion, but instead non-named arguments from anywhere in the list
    will be moved around to fit in the named ones where they belong.
    """
    
    nparam_move_map = []
    seen_target_pos = []
    
    # build a mapping of parameters that need to be moved and remove the name from them
    for i, p in enumerate(param_list):
        if '=' in p:
            pname, pval = p.split('=', 1)
            pname = pname.strip()
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
                raise KeyError('Unknown parameter name: {}'.format(pname))
            
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
    

class DscOp:
    """
    Class to represent an operation.
    I usually avoid unnecessary classes, but just using dictionaries for such
    long lists seems like too much of a hassle, so here we are
    """
    
    game = 'FT'
    op_name = 'END'
    op_id = 0
    param_values = [] # length of param_values will be set correctly when using from_id, from_name, or from_string
    param_info = None
    
    def __eq__(x, y):
        if not x.game == y.game:
            return False
        if not x.op_name == y.op_name:
            return False
        if not x.op_id == y.op_id:
            return False
        if not x.param_values == y.param_values:
            return False
        if not x.param_info == y.param_info:
            return False
        
        return True
    
    def __init__(self, game, op_name, op_id, param_values, param_info):
        """Base init method for DscOp. Recommended to use from_id, from_name, or from_string instead."""
        
        if not game in dsc_db_games:
            raise UnsupportedDscGameException('Unsupported game name: {}'.format(game))
        self.game = game
        self.op_name = op_name
        self.op_id = op_id
        self.param_values = param_values
        self.param_info = param_info
    
    @classmethod
    def from_id(self, game, op_id, param_values=None):
        if not game in dsc_db_games:
            raise UnsupportedDscGameException('Unsupported game name: {}'.format(game))
        if not op_id in dsc_lookup_ids:
            raise UnknownDscOpException('Unknown opcode id: {}'.format(op_id))
        if not game in dsc_lookup_ids[op_id]:
            raise UnknownDscOpException('Unknown opcode id for game {}: {}'.format(game, op_id))
        
        op_info = dsc_op_db[dsc_lookup_ids[op_id][game]]
        op_game_info = op_info.get('info_{}'.format(game), op_info.get('info_default'))
        if not op_game_info:
            raise Exception('Unexpected error accessing opcode info (op {}, game {})'.format(op_id, game))
        
        param_cnt = op_game_info['param_cnt']
        if param_values == None:
            pvalues = [0 for i in range(0, param_cnt)]
        elif len(param_values) > param_cnt:
            pvalues = param_values[:param_cnt]
        else:
            pvalues = param_values
            while len(param_values) < param_cnt:
                pvalues += [0]
        
        if 'param_info' in op_game_info:
            pvalues = _fix_param_types(pvalues, op_game_info['param_info'])
        else:
            pvalues = _fix_param_types(pvalues, [None for i in range(0, param_cnt)])
        
        return self(game, op_info['name'], op_id, pvalues, op_game_info.get('param_info'))
    
    @classmethod
    def from_name(self, game, op_name, param_values=None):
        if not game in dsc_db_games:
            raise UnsupportedDscGameException('Unsupported game name: {}'.format(game))
        if not op_name in dsc_lookup_names:
            raise UnknownDscOpException('Unknown opcode name: {}'.format(op_name))
        
        op_info = dsc_op_db[dsc_lookup_names[op_name]]
        op_game_info = op_info.get('info_{}'.format(game), op_info.get('info_default'))
        if not op_game_info:
            raise UnknownDscOpException('Unknown opcode name for game {}: {}'.format(game, op_name))
        
        param_cnt = op_game_info['param_cnt']
        if param_values == None:
            pvalues = [0 for i in range(0, param_cnt)]
        elif len(param_values) > param_cnt:
            pvalues = param_values[:param_cnt]
        else:
            pvalues = param_values
            while len(param_values) < param_cnt:
                pvalues += [0]
        
        if 'param_info' in op_game_info:
            pvalues = _fix_param_types(pvalues, op_game_info['param_info'])
        else:
            pvalues = _fix_param_types(pvalues, [None for i in range(0, param_cnt)])
        
        return self(game, op_name, op_game_info['id'], pvalues, op_game_info.get('param_info'))
    
    @classmethod
    def from_string(self, game, op_str):
        if not game in dsc_db_games:
            raise UnsupportedDscGameException('Unsupported game name: {}'.format(game))
        
        op_str = op_str.strip()
        if op_str.endswith(';'):
            op_str = op_str[:-1]
        if not '(' in op_str or op_str.startswith('(') or not op_str.endswith(')'):
            raise Exception('Invalid input string')
        
        op_name = op_str.split('(', 1)[0].strip()
        if not op_name in dsc_lookup_names:
            raise UnknownDscOpException('Unknown opcode name: {}'.format(op_name))
        
        op_info = dsc_op_db[dsc_lookup_names[op_name]]
        op_game_info = op_info.get('info_{}'.format(game), op_info.get('info_default'))
        if not op_game_info:
            raise UnknownDscOpException('Unknown opcode name for game {}: {}'.format(game, op_name))
        
        param_values = op_str.split('(', 1)[1].split(')')[0]
        param_values = [p.strip() for p in param_values.split(',')]
        
        param_cnt = op_game_info['param_cnt']
        
        if 'param_info' in op_game_info:
            param_values = _reorder_named_args(param_values, op_game_info['param_info'])
        else:
            param_values = _reorder_named_args(param_values, [None for i in range(0, param_cnt)])
        
        if param_values == None:
            pvalues = [0 for i in range(0, param_cnt)]
        elif len(param_values) > param_cnt:
            pvalues = param_values[:param_cnt]
        else:
            pvalues = param_values
            while len(param_values) < param_cnt:
                pvalues += [0]
        
        if 'param_info' in op_game_info:
            pvalues = _fix_param_types(pvalues, op_game_info['param_info'], enum_dir='none')
        else:
            pvalues = _fix_param_types(pvalues, [None for i in range(0, param_cnt)], enum_dir='none')
        
        return self(game, op_name, op_game_info['id'], pvalues, op_game_info.get('param_info'))
    
    @classmethod
    def read_from_stream(self, game, s, endian='little'):
        self = self.from_id(game, int.from_bytes(s.read(4), byteorder=endian, signed=True))
        
        for i in range(0, len(self.param_values)):
            if self.param_info and self.param_info[i]:
                t = self.param_info[i]['type']
                if t == 'enum': # read enums as ints and fix them later
                    t = int
            else:
                t = int
            
            if t == bool: # use to catch false assumptions about type
                v = int.from_bytes(s.read(4), byteorder=endian, signed=False)
                if v > 1:
                    raise TypeError('{}\'s parameter {} is not a bool!'.format(self.name, self.param_info[i]['name']))
                v = bool(v)
            else:
                v = t.from_bytes(s.read(4), byteorder=endian, signed=True)
            
            self.param_values[i] = v
        
        if self.param_info: # use _fix_param_types to resolve enums
            self.param_values = _fix_param_types(self.param_values, self.param_info)
        
        return self
    
    
    def write_to_stream(self, s, endian='little'):
        if self.param_info:
            pvalues = _fix_param_types(self.param_values, self.param_info, enum_dir='from_str')
        else:
            pvalues = self.param_values
        
        s.write(self.op_id.to_bytes(4, byteorder=endian, signed=True))
        
        for p in pvalues:
            s.write(p.to_bytes(4, byteorder=endian, signed=True))
    
    
    def get_str(self, show_names=True):
        """Returns a nicely formatted string representing this OP"""
        
        param_str = '('
        for i, v in enumerate(self.param_values):
            if show_names and self.param_info and i < len(self.param_info) and self.param_info[i]:
                param_str += '{}={}'.format(self.param_info[i]['name'], v)
            else:
                param_str += str(v)
            
            if i < len(self.param_values) - 1:
                param_str += ', '
        
        param_str += ')'
        
        return '{}{}'.format(self.op_name, param_str)
    
    def __str__(self):
        return 'DscOp({}, {})'.format(self.game, self.get_str(True))
    
    def __repr__(self):
        return '<DscOp object ({}, {})>'.format(self.game, self.get_str(True))


def from_stream(s):
    """AFT-only"""
    
    s.seek(s.tell() + 12) # skip junk
    
    out = []
    
    while True:
        op = DscOp.read_from_stream('FT', s, 'little')
        out += [op]
        
        if op.op_id == 0: # END
            break
    
    return out


def to_stream(dsc, s):
    """AFT-only"""
    
    s.write(b'\x21\x09\x05\x14\x41\x00\x00\x00\x00\x00\x00\x00') # header junk
    
    for op in dsc:
        op.write_to_stream(s)

def dsc_to_string(dsc):
    """Get a nice string representation of an entire DSC"""
    
    out = ''
    for i, op in enumerate(dsc):
        out += op.get_str(True) + ';'
        if i < len(dsc) - 1:
            out += '\n'
    
    return out