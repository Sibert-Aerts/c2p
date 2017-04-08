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

if __name__ == '__main__':
    unittest.main()