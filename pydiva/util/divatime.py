class DivaTime(int):
    """
    Works like a regular int, but string conversions are formatted like
    timecodes.
    (eg. int 6200003 <-> str '1:02.00003')
    
    Just initialise a new instance rather than trying to change value after
    creation.
    Integer arithmetic (add, sub, mul, div) works on the internal int.
    For other stuff or floating point arithmetic just rely on type conversion.
    """
    
    _second_decimals = 5
    _len_second = 1 * 10**_second_decimals
    _len_minute = 60 * _len_second
    _len_hour = 60 * _len_minute
    
    @classmethod
    def __new__(cls, type, value):
        """Initialise an instance (eg. from another instance, an integer, or a string)."""
              
        return cls._new_int_value(value)
    
    @classmethod
    def _new_int_value(cls, value):
        """Set the current value (eg. from another instance, an integer, or a string)."""
        
        if type(value) == str:
            if value.startswith('-'):
                value = value[1:]
                negate = True
            else:
                negate = False
            
            if value.count('-') != 0:
                raise ValueError('Unknown timecode format (unexpected negative signs). \'Use (-)(hh:)(mm:)ss.ssssss\'.')
            
            value_sections = [s.strip() for s in value.split(':')]
            value = 0
            
            if len(value_sections) > 3:
                raise ValueError('Unknown timecode format (too many sections). \'Use (-)(hh:)(mm:)ss.ssssss\'.')
            
            for i, s in enumerate(reversed(value_sections)):
                if i == 0: # seconds
                    point_idx = s.find('.')
                    
                    # values with no point get one
                    if point_idx < 0:
                        s += '.'
                        point_idx = len(s) - 1
                    
                    # pad zeroes to complete fractional part
                    while len(s) < point_idx + 1 + cls._second_decimals:
                        s += '0'
                    
                    # use slices to get the wanted parts
                    s = s[:point_idx] + s[point_idx+1:point_idx+1+cls._second_decimals]
                    value += int(s)
                
                elif i == 1: # minutes
                    value += int(s) * cls._len_minute
        
                elif i == 2: # hours
                    value += int(s) * cls._len_hour
            
            if negate:
                value *= -1
        
        return super().__new__(cls, value)
    
    @classmethod
    def from_bytes(cls, bytes, byteorder, signed=False):
        """Set the current value from integer bytes."""
        
        value_int = int.from_bytes(bytes, byteorder=byteorder, signed=signed)
        return cls(value_int)
    
    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, super().__repr__())
    
    def __str__(self):
        value = int(self) # get int of our value
        out = ''
        
        if value < 0:
            value *= -1
            out += '-'
        
        force_inc_lower = False
        
        if value >= self.__class__._len_hour:
            out += '{:01d}'.format(value // self.__class__._len_hour) + ':'
            value %= self.__class__._len_hour
            force_inc_lower = True
        
        if force_inc_lower or value >= self.__class__._len_minute:
            out += '{:02d}'.format(value // self.__class__._len_minute) + ':'
            value %= self.__class__._len_minute
            force_inc_lower = True
        
        
        value = repr(value) # get the representation of the int
        # (value no-longer needs to be int for seconds and fractional part)
        # lpad zeroes for seconds to fit, and leading 0 for 10s
        while len(value) <= self.__class__._second_decimals + (1 if force_inc_lower else 0):
            value = '0' + value
        
        value = value[:-self.__class__._second_decimals] + '.' + value[-self.__class__._second_decimals:] # insert point
        value = value.rstrip('0').rstrip('.') # remove trailing zeroes and point
        out += value
        
        return out
    
    
    @staticmethod
    def _arith(fn, x, y):
        r = fn(y)
        if r == NotImplemented:
            return r
        else:
            return x.__class__.__new__(x.__class__, r)
    
    def __add__(x, y):
        return x.__class__._arith(super().__add__, x, y)
    
    def __radd__(x, y):
        return x.__class__._arith(super().__radd__, x, y)
    
    def __sub__(x, y):
        return x.__class__._arith(super().__sub__, x, y)
    
    def __rsub__(x, y):
        return x.__class__._arith(super().__rsub__, x, y)
    
    def __mul__(x, y):
        return x.__class__._arith(super().__mul__, x, y)
    
    def __rmul__(x, y):
        return x.__class__._arith(super().__rmul__, x, y)
    
    #def __truediv__(x, y):
    #    return x.__class__._arith(super().__truediv__, x, y)
    
    #def __rtruediv__(x, y):
    #    return x.__class__._arith(super().__rtruediv__, x, y)
    
    def __floordiv__(x, y):
        return x.__class__._arith(super().__floordiv__, x, y)
    
    def __rfloordiv__(x, y):
        return x.__class__._arith(super().__rfloordiv__, x, y)