"""
pydsc reader and writer for Project Diva DSC files
"""

from pydiva.pydsc_op_db import dsc_op_db, dsc_db_games, dsc_lookup_ids, dsc_lookup_names
from pydiva.pydsc_formats import _dsc_types
from pydiva.pydsc_util import fix_param_types, fix_param_cnt, reorder_named_args
#from pydiva.util.stringenum import StringEnum
from io import BytesIO

class UnsupportedDscGameException(Exception):
    pass

class UnknownDscOpException(Exception):
    pass    

class DscOp:
    """
    Class to represent an operation.
    I usually avoid unnecessary classes, but just using dictionaries for such
    long lists seems like too much of a hassle, so here we are
    """
    
    # instance vars
    # game = 'FT'
    # op_name = 'END'
    # op_id = 0
    # param_values = [] # length of param_values will be set correctly when using from_id, from_name, or from_string
    # param_info = None
    
    def __eq__(x, y):
        if type(y) != DscOp:
            return NotImplemented
        
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
        self.op_name = op_name.upper()
        self.op_id = op_id
        self.param_values = param_values
        self.param_info = param_info
    
    @classmethod
    def from_id(cls, game, op_id, param_values):
        """
        Returns a DscOp from opcode id, with ordered parameter values set.
        param_values equal to None will generate dummy data (NOT default values).
        """
        
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
        
        pvalues = fix_param_cnt(param_values, op_game_info['param_cnt'])
        
        if 'param_info' in op_game_info:
            pvalues = fix_param_types(pvalues, op_game_info['param_info'])
        else:
            pvalues = fix_param_types(pvalues, [None for i in range(0, op_game_info['param_cnt'])])
        
        return cls(game, op_info['name'], op_id, pvalues, op_game_info.get('param_info'))
    
    @classmethod
    def from_name(cls, game, op_name, param_values):
        """
        Returns a DscOp from opcode name, with ordered parameter values set.
        param_values equal to None will generate dummy data (NOT default values).
        """
        
        op_name = op_name.upper()
        
        if not game in dsc_db_games:
            raise UnsupportedDscGameException('Unsupported game name: {}'.format(game))
        if not op_name in dsc_lookup_names:
            raise UnknownDscOpException('Unknown opcode name: {}'.format(op_name))
        
        op_info = dsc_op_db[dsc_lookup_names[op_name]]
        op_game_info = op_info.get('info_{}'.format(game), op_info.get('info_default'))
        if not op_game_info or op_game_info['id'] == None:
            raise UnknownDscOpException('Unknown opcode name for game {}: {}'.format(game, op_name))
        
        pvalues = fix_param_cnt(param_values, op_game_info['param_cnt'])
        
        if 'param_info' in op_game_info:
            pvalues = fix_param_types(pvalues, op_game_info['param_info'])
        else:
            pvalues = fix_param_types(pvalues, [None for i in range(0, op_game_info['param_cnt'])])
        
        return cls(game, op_name, op_game_info['id'], pvalues, op_game_info.get('param_info'))
    
    @classmethod
    def from_string(cls, game, op_str):
        """
        Returns a DscOp from a string (as returned by get_str).
        """
        
        if not game in dsc_db_games:
            raise UnsupportedDscGameException('Unsupported game name: {}'.format(game))
        
        op_str = op_str.strip()
        if op_str.endswith(';'):
            op_str = op_str[:-1]
        if op_str.count('(') != 1 or op_str.count(')') != 1 or op_str.startswith('(') or not op_str.endswith(')'):
            raise Exception('Invalid input string')
        
        op_name = op_str.split('(', 1)[0].strip().upper()
        if not op_name in dsc_lookup_names:
            raise UnknownDscOpException('Unknown opcode name: {}'.format(op_name))
        
        op_info = dsc_op_db[dsc_lookup_names[op_name]]
        op_game_info = op_info.get('info_{}'.format(game), op_info.get('info_default'))
        if not op_game_info or op_game_info['id'] == None:
            raise UnknownDscOpException('Unknown opcode name for game {}: {}'.format(game, op_name))
        
        param_values = op_str.split('(', 1)[1].split(')')[0]
        param_values = [p.strip() for p in param_values.split(',')]
        
        param_cnt = op_game_info['param_cnt']
        
        if len(param_values) > param_cnt:
            pvalues = param_values[:param_cnt]
        else:
            pvalues = param_values
            while len(param_values) < param_cnt:
                pvalues += ['']
        
        if 'param_info' in op_game_info:
            pvalues = reorder_named_args(pvalues, op_game_info['param_info'])
        else:
            pvalues = reorder_named_args(pvalues, [None for i in range(0, op_game_info['param_cnt'])])
        
        pvalues = fix_param_cnt(pvalues, op_game_info['param_cnt'])
        
        if 'param_info' in op_game_info:
            pvalues = fix_param_types(pvalues, op_game_info['param_info'])
        else:
            pvalues = fix_param_types(pvalues, [None for i in range(0, op_game_info['param_cnt'])])
        
        return cls(game, op_name, op_game_info['id'], pvalues, op_game_info.get('param_info'))
    
    @classmethod
    def read_from_stream(cls, game, s, endian='little'):
        """
        Returns a DscOp by reading it from a binary stream.
        """
        
        # no need to check read length because end of stream will generate b'' and turn into id 0
        self = cls.from_id(game, int.from_bytes(s.read(4), byteorder=endian, signed=True), param_values=None)
        
        for i in range(0, len(self.param_values)):
            if self.param_info and self.param_info[i]:
                t = self.param_info[i]['type']
            else:
                t = int
            
            if t == bool and not self.param_info[i].get('ignore_bool_warning'): # use to catch false assumptions about type
                v = int.from_bytes(s.read(4), byteorder=endian, signed=False)
                if v > 1:
                    raise TypeError('{}\'s parameter {} is not a bool!'.format(self.op_name, self.param_info[i]['name']))
                v = bool(v)
            else:
                v = t.from_bytes(s.read(4), byteorder=endian, signed=True)
            
            self.param_values[i] = v
        
        return self
    
    
    def write_to_stream(self, s, endian='little'):
        """
        Writes the DscOp to a binary stream.
        """
        
        if self.param_info:
            pvalues = fix_param_types(self.param_values, self.param_info)
        else:
            pvalues = self.param_values
        
        s.write(self.op_id.to_bytes(4, byteorder=endian, signed=True))
        
        for p in pvalues:
            s.write(p.to_bytes(4, byteorder=endian, signed=True))
    
    
    def get_annotated_str(self, show_names=True, int_vars=False, hide_default=True):
        """
        Returns a nicely formatted string representing this Op with annotated tags for syntax.
        Output is a tuple of string and a list of dicts: ('END()', [{'start': 0, 'end': 5, 'name': 'op'},...]).
        
        list of tag names:
        'op': from the DscOp's op_name until the op parameters' closing parenthesis
        'op_name': just the op's name, excluding values and parenthesis
        'param_name': param's name, including = sign, if present
        'param_value': param's value
        
        param tags will also contain 'param_index', which is the index into
        param_info for its details
        """
        
        if hide_default and not show_names:
            raise Exception('Hiding default values without showing names on parameters may make unparseable results')
        
        out = self.op_name
        tags = [
            {'start': 0, 'end': 0, 'name': 'op'}, # placeholder
            {'start': 0, 'end': len(self.op_name), 'name': 'op_name'}
        ]
        
        out += '('
        cur_pos = len(out)
        
        out_param_cnt = 0
        for i, v in enumerate(self.param_values):
            if self.param_info and self.param_info[i]:
                if hide_default and 'default' in self.param_info[i] and v == self.param_info[i]['default']:
                    if not None in self.param_info[i:]: # check this because it can create false ordering when there are unused parameters
                        continue                        # (None arg detected as previously ommited arg positionally)
                
                if self.param_info[i] and show_names and len(self.param_values) > 1:
                    namestr = '{}='.format(self.param_info[i]['name'])
                    out += namestr
                    tags += [{'start': cur_pos, 'end': cur_pos + len(namestr), 'name': 'param_name', 'param_index': i}]
                    cur_pos += len(namestr)
            
            if int_vars:
                valuestr = 'i'
                valuestr += str(int(v))
            else:
                valuestr = str(v)
            out += valuestr
            tags += [{'start': cur_pos, 'end': cur_pos + len(valuestr), 'name': 'param_value', 'param_index': i}]
            cur_pos += len(valuestr)
            
            out += ', '
            cur_pos += 2
            out_param_cnt += 1
        
        if out_param_cnt > 0:
            out = out[:-2]
            cur_pos -= 2
        out += ')'
        cur_pos += 1
        
        tags[0]['end'] = cur_pos
        
        return (out, tags)
        
    def get_str(self, show_names=True, int_vars=False, hide_default=True):
        """Returns a nicely formatted string representing this Op"""
        
        return self.get_annotated_str(show_names, int_vars, hide_default)[0]
    
    def __str__(self):
        return 'DscOp({}, {})'.format(self.game, self.get_str(True))
    
    def __repr__(self):
        return '<DscOp object ({}, {})>'.format(self.game, self.get_str(True))


def from_stream(s, game_hint=None):
    """
    Converts a DSC from a stream to a list of DscOp.
    Use game_hint to force detection as a certain type.
    """
    
    og_pos = s.tell()
    
    if game_hint:
        game = game_hint
    else:
        game = None
        for g, type_info in _dsc_types.items():
            if type_info['header_regex'].match(s.read(len(type_info['header_regex'].pattern))):
                game = g
                break
    
    if not game:
        raise UnsupportedDscGameException('Couldn\'t identify file type')
    
    out = []
    
    while True:
        op = DscOp.read_from_stream('FT', s, 'little')
        out += [op]
        
        if op.op_id == 0: # END
            break
    
    return out

def from_bytes(b, game_hint=None):
    """
    Converts a DSC from bytes to a list of DscOp.
    Use game_hint to force detection as a certain type.
    """
    
    with BytesIO(b) as s:
        return from_stream(s, game_hint)


def to_stream(dsc, s):
    """Writes a DscOp list to a stream."""
    
    game = dsc[0].game
    s.write(_dsc_types[game]['header_output'])
    
    for op in dsc:
        op.write_to_stream(s)

def to_bytes(dsc):
    """Converts a DscOp list to bytes."""
    
    with BytesIO() as s:
        to_stream(dsc, s)
        return s.getvalue()

def dsc_to_annotated_string(dsc, compat_mode=False, indent=2):
    """
    Get a nice string representation of an entire DSC, complete with tags like DscOp.get_annotated_str.
    Returns a tuple of (text, tags)
    Use compat_mode if output should be readable in future versions.
    """
    
    time_ops = ['TIME']
    branch_ops = ['PV_BRANCH_MODE']
    branch_param_values = ['normal', 'success']
    indent_level = 1
    
    out = ''
    out_len = 0
    tags = []
    for i, op in enumerate(dsc):
        if op.op_name in branch_ops:
            if op.param_values[0] in branch_param_values:
                indent_level = 2
            else:
                indent_level = 1
        
        if not op.op_name in time_ops + branch_ops:
            s = ''.join([' ' for i in range(0, indent_level * indent)])
            out += s
            out_len += len(s)
        
        s, optags = op.get_annotated_str(not compat_mode, compat_mode, not compat_mode)
        s += ';'
        for t in optags:
            t['start'] += out_len
            t['end'] += out_len
        out += s
        out_len += len(s)
        tags += optags
        
        if i < len(dsc) - 1:
            out += '\n'
            out_len += 1
    
    return (out, tags)

def dsc_to_string(dsc, compat_mode=False, indent=2):
    """
    Get a nice string representation of an entire DSC.
    Use compat_mode if output should be readable in future versions.
    """
    
    return dsc_to_annotated_string(dsc, compat_mode, indent)[0]