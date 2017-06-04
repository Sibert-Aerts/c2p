import unittest
from .ctypes import *

class TestCTypesEquality(unittest.TestCase):
    def test_equality(self):
        self.assertTrue(CVoid() == CVoid())
        self.assertTrue(CVoid() != CInt())
        self.assertTrue(CPointer(CVoid()) == CPointer(CVoid()))
        self.assertTrue(CPointer(CVoid()) != CPointer(CInt()))
        self.assertTrue(CPointer(CVoid()) != CVoid())

    def test_const_equality(self):
        self.assertTrue(CVoid() == CConst(CVoid()).ignoreConst())
        self.assertTrue(CVoid() != CConst(CInt()).ignoreConst())
        self.assertTrue(CConst(CVoid()).ignoreConst() == CConst(CVoid()).ignoreConst())
        self.assertTrue(CConst(CPointer(CVoid())).ignoreConst() == CPointer(CConst(CVoid())).ignoreConst())
        self.assertTrue(CConst(CPointer(CConst(CVoid()))).ignoreConst() == CPointer(CConst(CVoid())).ignoreConst())

    def test_promotion(self):
        self.assertTrue(CFloat().promotes_to(CFloat()))
        self.assertTrue(CInt().promotes_to(CFloat()))
        self.assertTrue(CChar().promotes_to(CFloat()))
        self.assertTrue(CBool().promotes_to(CFloat()))

        self.assertFalse(CFloat().promotes_to(CInt()))
        self.assertTrue(CInt().promotes_to(CInt()))
        self.assertTrue(CChar().promotes_to(CInt()))
        self.assertTrue(CBool().promotes_to(CInt()))

        self.assertFalse(CFloat().promotes_to(CChar()))
        self.assertFalse(CInt().promotes_to(CChar()))
        self.assertTrue(CChar().promotes_to(CChar()))
        self.assertTrue(CBool().promotes_to(CChar()))

        self.assertFalse(CFloat().promotes_to(CBool()))
        self.assertFalse(CInt().promotes_to(CBool()))
        self.assertFalse(CChar().promotes_to(CBool()))
        self.assertTrue(CBool().promotes_to(CBool()))

        self.assertFalse(CInt().promotes_to(CVoid()))
        self.assertFalse(CVoid().promotes_to(CInt()))
        
    def test_promotion_2(self):
        self.assertTrue(CFloat() == CInt().common_promote(CFloat()))
        self.assertTrue(CFloat() == CBool().common_promote(CFloat()))
        self.assertTrue(CInt() == CInt().common_promote(CChar()))
        self.assertTrue(CInt() == CInt().common_promote(CBool()))
        self.assertTrue(CInt() == CBool().common_promote(CInt()))

        self.assertTrue(CInt().common_promote(CVoid()) is None)
        self.assertTrue(CVoid().common_promote(CInt()) is None)

if __name__ == '__main__':
    unittest.main()