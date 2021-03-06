from typing import Any, List
from .environment import Environment
from .code_node import CodeNode
from .error import SemanticError
from ..grammar.ctypes import *
from ..grammar.ast.node_expression import Constant
from ..instructions import *
from c2p.source_interval import SourceInterval
import re

Expression = Any

def string_print_loop(node: CodeNode):
    loop_label = Label('printf_loop')
    done_label = Label('printf_done')

    code = CodeNode()
    ################################### Stack after this opcode: #
    ##############################################################
    code.add(node)
    code.add(loop_label)              # q
    # Get the character.
    code.add(Dpl(PAddress))           # q, q
    code.add(Ind(PCharacter))         # q, STORE[q]

    # If it's zero, jump to done.
    code.add(Dpl(PCharacter))         # q, STORE[q], STORE[q]
    code.add(Ldc(PCharacter, 0))      # q, STORE[q], STORE[q], 0
    code.add(Neq(PCharacter))         # q, STORE[q], STORE[q] != 0
    code.add(Fjp(done_label.label))   # q, STORE[q]

    # Print it and loop.
    code.add(Out1(PCharacter))        # q
    code.add(Inc(PAddress, 1))        # q+1
    code.add(Ujp(loop_label.label))
    code.add(done_label)              # q, STORE[q]

    # Discard two values (HACK).
    code.add(Dpl(PCharacter))
    code.add(Equ(PCharacter))
    code.add(Fjp(done_label.label))
    code.add(Dpl(PAddress))
    code.add(Equ(PAddress))
    code.add(Fjp(done_label.label))

    code.type = CVoid()
    code.maxStackSpace = 5
    return code

def to_code(arguments: List[Expression], env: Environment, where: SourceInterval):
    # Get the format string.
    fmt = arguments[0]
    if not (isinstance(fmt, Constant) and fmt.type.equivalent(CArray(CChar(), 1))):
        raise SemanticError('First argument to "printf" should be a string literal.'
            ' (Hint: try `printf("%s", foo)` to print a non-literal string.)', where)
    fmt = fmt.value
    assert isinstance(fmt, str)

    # Tokenize format string.
    tokens = re.findall('%%|%s|%d|%\d*f|%c|.', fmt, flags=re.DOTALL)

    # Check argument count.
    expected = 1 + len(re.findall('%s|%d|%\d*f|%c', fmt, flags=re.DOTALL))
    given = len(arguments)
    if expected != given:
        raise SemanticError('printf expects {} argument{} here; given {}.'.format(expected, '' if expected == 1 else 's', given), where)

    # Start codegen.
    code = CodeNode()
    code.type = CVoid()
    code.maxStackSpace = 5
    i = 1
    for token in tokens:
        if token == '%s':
            node = arguments[i].to_code(env)
            t = node.type.ignoreConst()
            if not (isinstance(t, CArray) and t.t == CChar() or node.type.ignoreConst() == CPointer(CChar())):
                raise SemanticError('%s matched up with {} in printf.'.format(node.type), where)
            code.add(string_print_loop(node))
            i += 1
        elif token == '%d':
            node = arguments[i].to_code(env)
            if node.type.ignoreConst() != CInt():
                raise SemanticError('%d matched up with {} in printf.'.format(node.type), where)
            code.add(node)
            code.add(Out1(PInteger))
            i += 1
        elif token[0] == '%' and token[-1] == 'f':
            node = arguments[i].to_code(env)
            if node.type.ignoreConst() != CFloat():
                raise SemanticError('%f matched up with {} in printf.'.format(node.type), where)
            code.add(node)
            if len(token) > 2:
                code.add(Ldc(PInteger, token[1:-1]))
                code.add(Out2())
            else:
                code.add(Out1(PReal))
            i += 1
        elif token == '%c':
            node = arguments[i].to_code(env)
            if node.type.ignoreConst() != CChar():
                raise SemanticError('%c matched up with {} in printf.'.format(node.type), where)
            code.add(node)
            code.add(Out1(PCharacter))
            i += 1
        else:
            code.add(Ldc(PCharacter, ord(token[:1])))
            code.add(Out1(PCharacter))

    return code
