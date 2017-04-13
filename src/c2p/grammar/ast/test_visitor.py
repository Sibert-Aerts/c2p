import unittest
import sys
import c2p
import os
import traceback
import cProfile
from pstats import Stats

from .visitor import *
from antlr4 import * # type: ignore
from c2p.grammar.antlr.SmallCLexer import SmallCLexer
from c2p.grammar.antlr.SmallCParser import SmallCParser
from c2p.grammar.ast.visitor import ASTError, ASTVisitor

filepath = os.path.dirname(__file__) + "/test/"

class TestVisitorSuccess(unittest.TestCase):
    def parse(self, filename):
        parser = SmallCParser(CommonTokenStream(SmallCLexer(FileStream(filename))))
        self.tree = parser.program()

    def _test_acceptance(self, filename):
        try:
            self.parse(filepath + filename)
            ASTVisitor().visit(self.tree)
        except ASTError:
            self.fail("Failed to visit '{0}'!".format(filename))

    def _test_failure(self, filename):
        try:
            self.parse(filepath + filename)
            ASTVisitor().visit(self.tree)
        except ASTError:
            return
        self.fail("Succeeded at visiting incorrect file '{0}'!".format(filename))

    def test_etc(self):
        self._test_acceptance('visitable/etc.c')

    def test_for(self):
        self._test_acceptance('visitable/for.c')

    def test_if(self):
        self._test_acceptance('visitable/if.c')

    def test_while(self):
        self._test_acceptance('visitable/while.c')

    def test_function(self):
        self._test_acceptance('visitable/function.c')

    def test_expression(self):
        self._test_acceptance('visitable/expression.c')

    def test_garbage(self):
        self._test_acceptance('visitable/garbage.c')

    def test_qualifiers(self):
        self._test_failure('unvisitable/qualifiers.c')

    def setUp(self):
        self.profile = cProfile.Profile()
        self.profile.enable()

    def tearDown(self):
        p = Stats (self.profile)
        p.strip_dirs()
        p.sort_stats('cumtime')
        p.print_stats()
        self.tree = None
