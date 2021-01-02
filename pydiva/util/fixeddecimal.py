class FixedDecimal(int):
    """
    Works like a regular int, but string conversions have decimal places
    that will be converted (eg. int 2000 <-> str '20.00')
    
    Just initialise a new instance rather than trying to change value after
    creation.
    Integer arithmetic (add, sub, mul, div) works on the internal int.
    For other stuff or floating point arithmetic just rely on type conversion.
    
    Don't modify dec_places if you can avoid it.
    It's are not per-instance.
    
    Don't directly use this class, but instead derive it:
    `type('my_fixed_decimal', (FixedDecimal,), {'dec_places': 2})`.
    
    The n lowest base 10 digits of the internal int will be the decimal protion.
    
    Use `issubclass(my_fixed_decimal, FixedDecimal)` to check if a class is a
    FixedDecimal.
    """
    
    dec_places = 0
    
    @classmethod
    def _check_dec_places_valid(cls):
        """Check that dec_places is valid and won't lead to issues."""
        
        if type(cls.dec_places) != int:
            raise TypeError('FixedDecimal dec_places is wrong type (must be int)')
    
    @classmethod
    def __new__(cls, type, value):
        """Initialise an instance (eg. from another instance, an integer, or a string)."""
        
        cls._check_dec_places_valid()        
        return cls._new_int_value(value)
    
    @classmethod
    def _new_int_value(cls, value):
        """Set the current value (eg. from another instance, an integer, or a string)."""
        
        if type(value) == str:
            value = value.strip()
            point_idx = value.find('.')
            
            # values with no point get one
            if point_idx < 0:
                value += '.'
                point_idx = len(value) - 1
            
            # pad zeroes
            while len(value) < point_idx + 1 + cls.dec_places:
                value += '0'
            
            # use slices to get the wanted parts
            value = value[:point_idx] + value[point_idx+1:point_idx+1+cls.dec_places]
        
        return super().__new__(cls, value)
    
    @classmethod
    def from_bytes(cls, bytes, byteorder, signed=False):
        """Set the current value from integer bytes."""
        
        value_int = int.from_bytes(bytes, byteorder=byteorder, signed=signed)
        return cls(value_int)
    
    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, super().__repr__())
    
    def __str__(self):
        value = super().__repr__() # get the representation of the internal int
        
        # lpad zeroes
        while len(value) <= self.__class__.dec_places:
            value = '0' + value
        
        value = value[:-self.__class__.dec_places] + '.' + value[-self.__class__.dec_places:] # insert point
        return value
    
    
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