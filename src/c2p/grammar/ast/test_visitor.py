import unittest
import sys
import c2p
import os
import traceback

from .visitor import *
from antlr4 import * # type: ignore
from c2p.grammar.antlr.SmallCLexer import SmallCLexer
from c2p.grammar.antlr.SmallCParser import SmallCParser
from c2p.grammar.ast.visitor import ASTVisitor

filepath = os.path.dirname(__file__) + "/../examples/"

class TestVisitorSuccess(unittest.TestCase):
    def parse(self, filename):
        parser = SmallCParser(CommonTokenStream(SmallCLexer(FileStream(filename))))
        self.tree = parser.program()

    def _test(self, filename):
        self.parse(filepath + filename)
        AST = ASTVisitor().visit(self.tree)

    def test_etc(self):
        self._test('etc.c')

    def test_for(self):
        self._test('for.c')

    def test_if(self):
        self._test('if.c')

    def test_while(self):
        self._test('while.c')

    def test_function(self):
        self._test('function.c')

    def test_expression(self):
        self._test('expression.c')

    def test_garbage(self):
        self._test('garbage.c')

    def tearDown(self):
        self.tree = None

if __name__ == '__main__':
    unittest.main()