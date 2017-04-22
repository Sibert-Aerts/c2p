import sys
import os
import traceback
import unittest

from antlr4 import * # type: ignore
from c2p.grammar.antlr.SmallCLexer import SmallCLexer
from c2p.grammar.antlr.SmallCParser import SmallCParser
from c2p.grammar.ast.visitor import ASTVisitor
from c2p.grammar.ast.visualize import Visualizer
from .environment import Environment
from .semantic_error import SemanticError

filepath = os.path.dirname(__file__) + "/../../test/wrong/"

def _test(filename, expectedString):
    parser = SmallCParser(CommonTokenStream(SmallCLexer(FileStream(filepath + filename))))
    tree = parser.program()
    try:
        ast = ASTVisitor().visit(tree)
        code = ast.to_code(Environment()).code
        return False
    except SemanticError as e:
        if expectedString == str(e):
            return True
        else:
            print('Unexpected SemanticError "{}" for file "{}"'.format(str(e), filename))
            return False
    except:
        print('Unexpected {} "{}" for file "{}".'.format(e.__class__.__name__, str(e), filename))
        return False


class TestSemanticErrors(unittest.TestCase):

    def test_no_main(self):
        self.assertTrue(_test('no_main.c', 'No \'main\' function found.'))

    def test_float_as_int(self):
        self.assertTrue(_test('float_as_int.c', 'Incompatible assignment of const float to int.'))

    def test_int_as_float(self):
        self.assertTrue(_test('int_as_float.c', 'Incompatible assignment of const int to float.'))

    def test_int_as_char(self):
        self.assertTrue(_test('int_as_char.c', 'Incompatible assignment of const int to char.'))

    def test_func_as_var(self):
        self.assertTrue(_test('func_as_var.c', 'Attempted to use symbol "func" as a variable when it is a function.'))

    def test_var_as_func(self):
        self.assertTrue(_test('var_as_func.c', 'Attempted to use symbol "x" as a function when it is a variable.'))

    def test_repeat_func(self):
        self.assertTrue(_test('repeat_func.c', 'Repeated declaration of symbol "main"'))

    def test_repeat_var(self):
        self.assertTrue(_test('repeat_var.c', 'Repeated declaration of symbol "i"'))

    def test_undefined_func(self):
        self.assertTrue(_test('undefined_func.c', 'Use of undefined function "x"'))

    def test_undefined_var(self):
        self.assertTrue(_test('undefined_var.c', 'Use of undefined variable "x"'))

    def test_missing_args(self):
        self.assertTrue(_test('missing_args.c', 'Invalid call to "func": Expected 1 arguments, got 0.'))

    def test_too_many_args(self):
        self.assertTrue(_test('too_many_args.c', 'Invalid call to "func": Expected 0 arguments, got 1.'))

    def test_wrong_args(self):
        self.assertTrue(_test('wrong_args.c', 'Invalid call to "func": Expected expression of type int, got const float.'))

if __name__ == '__main__':
    unittest.main()