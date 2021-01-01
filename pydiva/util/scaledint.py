class ScaledInt(int):
    """
    Works like a regular int, but string conversions can use a
    percentage value instead. (eg. '60%', '55.2%')
    
    Just initialise a rather than trying to change value after creation.
    
    Don't modify value_min and value_max if you can avoid it.
    They are not per-instance.
    
    Don't directly use this class, but instead derive it:
    `type('my_scaled_int', (ScaledInt,), {'value_min': 0, 'value_max': 100})`.
    
    Use `issubclass(my_scaled_int, ScaledInt)` to check if a class is a
    ScaledInt.
    """
    
    value_min = 0
    value_max = 100
    
    @classmethod
    def _check_value_limits_valid(cls):
        """Check that value_min and value_max are valid and won't lead to issues."""
        
        if type(cls.value_min) != int:
            raise TypeError('ScaledInt value_min is wrong type (must be int)')
            
        if type(cls.value_max) != int:
            raise TypeError('ScaledInt value_max is wrong type (must be int)')
    
    @classmethod
    def __new__(cls, type, value):
        """Initialise an instance (eg. from another instance, an integer, or a string)."""
        
        cls._check_value_limits_valid()        
        return cls._new_int_value(value)
    
    @classmethod
    def _new_int_value(cls, value):
        """Set the current value (eg. from another instance, an integer, or a string)."""
        
        if type(value) == str:
            pct_idx = value.find('%')
            if pct_idx >= 0:
                value = float(value[:pct_idx])
                value = cls.value_min + value * (cls.value_max - cls.value_min) / 100
        
        return super().__new__(cls, value)
    
    @classmethod
    def from_bytes(cls, bytes, byteorder, signed=False):
        """Set the current value from integer bytes."""
        
        value_int = int.from_bytes(bytes, byteorder=byteorder, signed=signed)
        return cls(value_int)
    
    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, super().__repr__())
    
    def __str__(self):
        value = float((self - self.__class__.value_min) / (self.__class__.value_max - self.__class__.value_min)) * 100
        return '{:.2f}%'.format(value)