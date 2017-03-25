import unittest
from . import *
from ..ptypes import *

class TestInstructionEmit(unittest.TestCase):
    def test_emit(self):
        self.assertEqual(Add(PReal).emit(), 'add r')
        self.assertEqual(Lod(PAddress, 5, 7).emit(), 'lod a 5 7')
        self.assertEqual(Label('foo').emit(), 'foo:')
        self.assertEqual(Out1(PCharacter).emit(), 'out c')
        self.assertEqual(Out2().emit(), 'out r i')

if __name__ == '__main__':
    unittest.main()
