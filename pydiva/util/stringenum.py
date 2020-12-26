class StringEnum:
    """
    Basically a helper for treating enums in streams like strings in code.
    Implements the standard to_bytes/from_bytes stuff from other types.
    
    Use set_value to change value after initialisation, or just initialise a
    new instance using the new value.
    
    Don't directly use this class, but instead derive it:
    `type('my_enum', (StringEnum,), {'_choices': ['choice_1', 'choice_2']})`.
    
    Use `issubclass(my_enum, StringEnum)` to check if a class is a StringEnum.
    """
    
    _choices = None
    @property
    @classmethod
    def choices(cls):
        return cls._choices
    
    # instance vars
    # value_int = None
    
    @classmethod
    def _check_choices_valid(cls):
        if type(cls.choices) not in (list, tuple):
            raise TypeError('StringEnum choices is wrong type (must be list or tuple)')
    
    def __init__(self, value):
        """
        Initialise an instance
        
        """
        
        self.__class__._check_choices_valid()        
        self.set_value(value)
    
    def set_value(self, value):
        if type(value) == type(self):
            value = value.value_int
        
        if type(value) == int:
            if value < len(self.__class__.choices):
                self.value_int = value
            else:
                raise KeyError('Invalid enum value {}'.format(value))
        elif type(value) == str:
            try:
                self.value_int = self.__class__.choices.index(value)
            except ValueError:
                raise KeyError('Invalid enum value {}'.format(value))
        else:
            raise TypeError('value is wrong type (must be {} instance, str, or int)'.format(self.__class__.__name__))
    
    def to_bytes(self, length, byteorder, signed=False):
        return self.value_int.to_bytes(length=length, byteorder=byteorder, signed=signed)
    
    @classmethod
    def from_bytes(cls, bytes, byteorder, signed=False):
        value_int = int.from_bytes(bytes, byteorder=byteorder, signed=signed)
        return cls(value_int)
    
    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.__class__.choices[self.value_int])
    
    def __str__(self):
        return self.__class__.choices[self.value_int]
    
    def __eq__(x, y):
        cls = type(x)
        if type(y) == cls:
            return x.value_int == y.value_int
        else:
            try:
                y_cls = cls(y)
            except KeyError:
                return False
            except Exception:
                return NotImplemented
            return x.value_int == y_cls.value_int