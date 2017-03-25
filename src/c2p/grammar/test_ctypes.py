import unittest
from c2p.grammar.ctypes import *

class TestCTypesEquality(unittest.TestCase):
    def test_equality(self):
        self.assertTrue(CVoid() == CVoid())
        self.assertTrue(CVoid() != CInt())
        self.assertTrue(CPointer(CVoid()) == CPointer(CVoid()))
        self.assertTrue(CPointer(CVoid()) != CPointer(CInt()))
        self.assertTrue(CPointer(CVoid()) != CVoid())

if __name__ == '__main__':
    unittest.main()