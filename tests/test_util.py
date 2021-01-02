import unittest
from pydiva.util.stringenum import StringEnum
from pydiva.util.scaledint import ScaledInt
from pydiva.util.fixeddecimal import FixedDecimal
from pydiva.util.divatime import DivaTime


string_enum_fruits = type('string_enum_fruits', (StringEnum,), {'choices': ['apple', 'banana', 'pear', 'cantaloupe', 'watermelon', 'kiwi', 'mango']})

class TestStringEnum(unittest.TestCase):
    
    def test_int(self):
        i = string_enum_fruits(0)
        self.assertEqual(i, 0)
        i = string_enum_fruits(2)
        self.assertEqual(i, 2)
        
        # integer string
        i = string_enum_fruits('6')
        self.assertEqual(i, 6)
        
        try: # exception for bad index
            i = string_enum_fruits(7)
            self.assertTrue(False) # should never reach here
        except Exception as e:
            self.assertEqual(type(e), ValueError)
    
    def test_str(self):
        i = string_enum_fruits('apple')
        self.assertEqual(i, 0)
        self.assertEqual(repr(i), 'string_enum_fruits(apple)')
        self.assertEqual(str(i), 'apple')
        i = string_enum_fruits('pear')
        self.assertEqual(i, 2)
        self.assertEqual(repr(i), 'string_enum_fruits(pear)')
        self.assertEqual(str(i), 'pear')
        i = string_enum_fruits('mango')
        self.assertEqual(i, 6)
        self.assertEqual(repr(i), 'string_enum_fruits(mango)')
        self.assertEqual(str(i), 'mango')
        
        try: # exception for bad choice
            i = string_enum_fruits('lemon')
            self.assertTrue(False) # should never reach here
        except Exception as e:
            self.assertEqual(type(e), ValueError)
    
    def test_eq(self):
        i = string_enum_fruits('apple')
        j = string_enum_fruits(0)
        self.assertEqual(i, j)
        
        j = string_enum_fruits(1)
        self.assertNotEqual(i, j)

scaled_int_0_1000 = type('scaled_int_0_1000', (ScaledInt,), {'value_min': 0, 'value_max': 1000})
scaled_int_100_200 = type('scaled_int_100_200', (ScaledInt,), {'value_min': 100, 'value_max': 200})

class TestScaledInt(unittest.TestCase):
    
    def test_int(self):
        # should directly set the internal int
        i = scaled_int_0_1000(150)
        self.assertEqual(i, 150)
        i = scaled_int_100_200(150)
        self.assertEqual(i, 150)
        i = scaled_int_0_1000(-150)
        self.assertEqual(i, -150)
    
    def test_int_str(self):
        # should directly set the internal int
        i = scaled_int_0_1000('150')
        self.assertEqual(i, 150)
        self.assertEqual(repr(i), 'scaled_int_0_1000(150)')
        i = scaled_int_100_200('150')
        self.assertEqual(i, 150)
        self.assertEqual(repr(i), 'scaled_int_100_200(150)')
        i = scaled_int_0_1000('-150')
        self.assertEqual(i, -150)
        self.assertEqual(repr(i), 'scaled_int_0_1000(-150)')
    
    def test_pct_str(self):
        # should set as a percentage
        i = scaled_int_0_1000('15%')
        self.assertEqual(i, 150)
        self.assertEqual(str(i), '15%')
        i = scaled_int_100_200('50%')
        self.assertEqual(i, 150)
        self.assertEqual(str(i), '50%')
        i = scaled_int_0_1000('-15%')
        self.assertEqual(i, -150)
        self.assertEqual(str(i), '-15%')
    
    def test_arithmetic(self):
        i = scaled_int_0_1000(150)
        
        j = i + 100
        self.assertEqual(type(j), scaled_int_0_1000)
        self.assertEqual(j, 250)
        
        j = i - 100
        self.assertEqual(type(j), scaled_int_0_1000)
        self.assertEqual(j, 50)
        
        j = i * 10
        self.assertEqual(type(j), scaled_int_0_1000)
        self.assertEqual(j, 1500)
        
        j = i // 10
        self.assertEqual(type(j), scaled_int_0_1000)
        self.assertEqual(j, 15)
        
        # check float div is fine (doesn't preserve type
        j = i / 10
        self.assertEqual(type(j), float)
        self.assertEqual(j, 15)


fixed_decimal_2 = type('fixed_decimal_2', (FixedDecimal,), {'dec_places': 2})
fixed_decimal_6 = type('fixed_decimal_6', (FixedDecimal,), {'dec_places': 6})

class TestFixedDecimal(unittest.TestCase):
    
    def test_int(self):
        # should directly set the internal int
        i = fixed_decimal_2(100)
        self.assertEqual(i, 100)
        i = fixed_decimal_6(2000000)
        self.assertEqual(i, 2000000)
        i = fixed_decimal_2(-100)
        self.assertEqual(i, -100)
    
    def test_str(self):
        # should directly set with decimal places resolved
        i = fixed_decimal_2('100')
        self.assertEqual(i, 10000)
        self.assertEqual(repr(i), 'fixed_decimal_2(10000)')
        self.assertEqual(str(i), '100.00')
        i = fixed_decimal_6('20')
        self.assertEqual(i, 20000000)
        self.assertEqual(repr(i), 'fixed_decimal_6(20000000)')
        self.assertEqual(str(i), '20.000000')
        i = fixed_decimal_2('-100')
        self.assertEqual(i, -10000)
        self.assertEqual(repr(i), 'fixed_decimal_2(-10000)')
        self.assertEqual(str(i), '-100.00')
        
        i = fixed_decimal_2('1.51')
        self.assertEqual(i, 151)
        self.assertEqual(repr(i), 'fixed_decimal_2(151)')
        self.assertEqual(str(i), '1.51')
        i = fixed_decimal_6('20.23')
        self.assertEqual(i, 20230000)
        self.assertEqual(repr(i), 'fixed_decimal_6(20230000)')
        self.assertEqual(str(i), '20.230000')
        i = fixed_decimal_2('-1.51')
        self.assertEqual(i, -151)
        self.assertEqual(repr(i), 'fixed_decimal_2(-151)')
        self.assertEqual(str(i), '-1.51')
    
    def test_arithmetic(self):
        i = fixed_decimal_2(150)
        
        j = i + 100
        self.assertEqual(type(j), fixed_decimal_2)
        self.assertEqual(j, 250)
        
        j = i - 100
        self.assertEqual(type(j), fixed_decimal_2)
        self.assertEqual(j, 50)
        
        j = i * 10
        self.assertEqual(type(j), fixed_decimal_2)
        self.assertEqual(j, 1500)
        
        j = i // 10
        self.assertEqual(type(j), fixed_decimal_2)
        self.assertEqual(j, 15)
        
        # check float div is fine (doesn't preserve type
        j = i / 10
        self.assertEqual(type(j), float)
        self.assertEqual(j, 15)


class TestDivaTome(unittest.TestCase):
    
    def test_int(self):
        # should directly set the internal int
        i = DivaTime(100)
        self.assertEqual(i, 100)
        i = DivaTime(-100)
        self.assertEqual(i, -100)
    
    def test_str(self):
        # should set from timecode
        i = DivaTime('10') # 10s
        self.assertEqual(i, 10000000)
        i = DivaTime('-10')
        self.assertEqual(i, -10000000)
        
        i = DivaTime('100') # 100s
        self.assertEqual(i, 100000000)
        i = DivaTime('-100')
        self.assertEqual(i, -100000000)
        
        i = DivaTime('1:07') # 1m 7s
        self.assertEqual(i, 67000000)
        i = DivaTime('-1:7')
        self.assertEqual(i, -67000000)
        
        i = DivaTime('1:00:10') # 1h 10s
        self.assertEqual(i, 3610000000)
        i = DivaTime('-1:00:10')
        self.assertEqual(i, -3610000000)
        
        i = DivaTime('0:00:2.4') # 2.4s
        self.assertEqual(i, 2400000)
        i = DivaTime('-2.4')
        self.assertEqual(i, -2400000)
        
        # exceptions for bad input
        try:
            i = DivaTime('12:-2.3') # unexpected negative sign
            self.assertTrue(False) # should never reach here
        except Exception as e:
            self.assertEqual(type(e), ValueError)
        try:
            i = DivaTime('12:11:32:02.3') # too many sections
            self.assertTrue(False) # should never reach here
        except Exception as e:
            self.assertEqual(type(e), ValueError)
    
    def test_arithmetic(self):
        i = DivaTime(150)
        
        j = i + 100
        self.assertEqual(type(j), DivaTime)
        self.assertEqual(j, 250)
        
        j = i - 100
        self.assertEqual(type(j), DivaTime)
        self.assertEqual(j, 50)
        
        j = i * 10
        self.assertEqual(type(j), DivaTime)
        self.assertEqual(j, 1500)
        
        j = i // 10
        self.assertEqual(type(j), DivaTime)
        self.assertEqual(j, 15)
        
        # check float div is fine (doesn't preserve type
        j = i / 10
        self.assertEqual(type(j), float)
        self.assertEqual(j, 15)