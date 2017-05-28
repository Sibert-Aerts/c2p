from typing import Any, List
from .environment import Environment
from .code_node import CodeNode
from .error import SemanticError
from ..grammar.ctypes import *
from ..instructions import *
from c2p.source_interval import SourceInterval
import re

Expression = Any

def string_scan_loop(node: CodeNode):
    # TODO
    # assert node.type.ignoreConst() == CArray(CChar()) or node.type.ignoreConst() == CPointer(CChar())
    raise NotImplementedError

    code = CodeNode()
    code.type = CVoid()
    code.maxStackSpace = 5
    return code

def to_code(arguments: List[Expression], env: Environment, where: SourceInterval):
    # Get the format string.
    fmt = arguments[0]
    if not (fmt.__class__.__name__ == 'Constant' and fmt.type.ignoreConst() == CArray(CChar())):
        raise SemanticError('First argument to "scanf" should be a string literal.', where)
    fmt = fmt.value
    assert isinstance(fmt, str)

    # Tokenize format string.
    tokens = re.findall('%%|%s|%d|%f|%c|.', fmt, flags=re.DOTALL)

    # Check argument count.
    expected = 1 + tokens.count('%s') + tokens.count('%d') + tokens.count('%f') + tokens.count('%c')
    given = len(arguments)
    if expected != given:
        raise SemanticError('scanf expects {} argument{} here; given {}.'.format(expected, '' if expected == 1 else 's', given), where)

    # Start codegen.
    code = CodeNode()
    code.type = CVoid()
    code.maxStackSpace = 5
    i = 1
    for token in tokens:
        if token == '%s':
            node = arguments[i].to_code(env)
            if node.type != CPointer(CChar()):
                raise SemanticError('%s expects a mutable pointer to char here.', where)
            code.add(string_scan_loop(node))
            i += 1
        elif token == '%d':
            node = arguments[i].to_code(env)
            if node.type != CPointer(CInt()):
                raise SemanticError('%d expects a mutable pointer to int here.', where)
            code.add(node)
            code.add(In(PInteger))
            code.add(Sto(PInteger))
            i += 1
        elif token == '%f':
            node = arguments[i].to_code(env)
            if node.type != CPointer(CFloat()):
                raise SemanticError('%f expects a mutable pointer to float here.', where)
            code.add(node)
            code.add(In(PReal))
            code.add(Sto(PReal))
            i += 1
        elif token == '%c':
            node = arguments[i].to_code(env)
            if node.type != CPointer(CChar()):
                raise SemanticError('%c expects a mutable pointer to char here.', where)
            code.add(node)
            code.add(In(PCharacter))
            code.add(Sto(PCharacter))
            i += 1
        else:
            # Skip whitespace, or something?
            pass

    return code
