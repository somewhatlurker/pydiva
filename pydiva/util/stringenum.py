class StringEnum:
    """
    Basically a helper for treating enums in streams like strings in code.
    Implements the standard to_bytes/from_bytes stuff from other types, but
    from_bytes will return a string that can be used to reinitialise the class
    instead of a StringEnum object.
    
    Don't directly use this class, but instead use
    `type('my_enum', (StringEnum,), {'choices': ['choice_1', 'choice_2', ...]})`.
    
    Use `issubclass(my_enum, StringEnum)` to check type.
    """
    
    choices = None
    
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
        if type(value) == type(self):
            value = value.value_int
        
        if type(value) == int:
            if value < len(self.__class__.choices):
                self.value_int = value
            else:
                raise KeyError('Invalid enum value {}'.format(value))
        elif type(value) == str:
            self.set_value_str(value)
        else:
            raise TypeError('value is wrong type (must be {} instance, str, or int)'.format(self.__class__.__name__))
    
    def set_value_str(self, v_str):
        if not v_str:
            self.value_int = 0
        else:
            v_str = str(v_str)
            try:
                self.value_int = self.__class__.choices.index(v_str)
            except ValueError:
                raise KeyError('Invalid enum value {}'.format(v_str))
    
    def to_bytes(self, length, byteorder, signed=False):
        return self.value_int.to_bytes(length=length, byteorder=byteorder, signed=signed)
    
    @classmethod
    def from_bytes(cls, bytes, byteorder, signed=False):
        """
        This actually returns a string that can be used to reinitilise the type.
        Check the class docstring for details on how this works
        """
        
        cls._check_choices_valid()
        value_int = int.from_bytes(bytes, byteorder=byteorder, signed=signed)
        
        if value_int >= len(cls.choices):
            raise KeyError('Invalid enum value {}'.format(value_int))
        
        return cls.choices[value_int]