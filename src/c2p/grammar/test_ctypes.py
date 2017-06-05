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



        self.assertTrue(CArray(CInt(), 10).common_promote(CPointer(CInt())) == CPointer(CInt()))
        self.assertTrue(CArray(CInt(), 10).common_promote(CArray(CInt(), 20)) == CArray(CInt(), 30))
        self.assertTrue(CArray(CInt(), 10).common_promote(CArray(CConst(CInt()), 20)) == CArray(CInt(), 30))
        self.assertTrue(CArray(CConst(CInt()), 10).common_promote(CArray(CInt(), 20)) == CArray(CInt(), 30))
        self.assertTrue(CArray(CConst(CInt()), 10).common_promote(CArray(CConst(CInt()), 20)) == CArray(CInt(), 30))

    def test_equivalence(self):
        self.assertTrue(CVoid().equivalent(CVoid()))
        self.assertTrue(CInt().equivalent(CInt()))
        self.assertTrue(CInt().equivalent(CConst(CInt())))
        self.assertFalse(CInt().equivalent(CFloat()))
        self.assertFalse(CInt().equivalent(CConst(CFloat())))
        
        self.assertTrue(CPointer(CInt()).equivalent(CConst(CPointer(CConst(CInt())))))
        self.assertTrue(CArray(CInt(), 10).equivalent(CConst(CArray(CConst(CInt()), 10))))
        self.assertTrue(CArray(CInt(), 10).equivalent(CConst(CArray(CConst(CInt()), 20))))
        self.assertTrue(CArray(CInt(), 10).equivalent(CArray(CConst(CInt()), 20)))
        self.assertTrue(CArray(CInt(), 10).equivalent(CArray(CInt(), 20)))
        self.assertTrue(CConst(CArray(CConst(CInt()), 10)).equivalent(CConst(CArray(CConst(CInt()), 20))))

if __name__ == '__main__':
    unittest.main()