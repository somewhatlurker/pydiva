"""
pydsc reader and writer for Project Diva DSC files
"""

from pydiva.pydsc_op_db import dsc_op_db, dsc_db_games, dsc_lookup_ids, dsc_lookup_names

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
    
    game = 'FT'
    op_name = 'END'
    op_id = 0
    param_values = [] # length of param_values will be set correctly when using from_id or from_name
    param_info = None
    
    def __init__(self, game, op_name, op_id, param_values, param_info):
        """Base init method for DscOp. Recommended to use DscOp.from_id or DscOp.from_name instead."""
        
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
        
        return self(game, op_name, op_info['id'], pvalues, op_game_info.get('param_info'))
    
    def get_str(self, show_names=False):
        """Returns a nicely formatted string representing this OP"""
        
        param_str = '('
        for i, v in enumerate(self.param_values):
            if show_names and self.param_info and i < len(self.param_info) and self.param_info[i]:
                param_str += '{}={}'.format(self.param_info[i]['name'], v)
            else:
                param_str += str(v)
            
            if i < len(self.param_values) - 1:
                param_str += ', '
            else:
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
        op_id = int.from_bytes(s.read(4), byteorder='little', signed=True)
        op = DscOp.from_id('FT', op_id)
        for i in range(0, len(op.param_values)):
            if op.param_info and op.param_info[i]:
                t = op.param_info[i]['type']
            else:
                t = int
            
            op.param_values[i] = t.from_bytes(s.read(4), byteorder='little', signed=True)
        
        out += [op]
        
        if op_id == 0: # END
            break
    
    return out