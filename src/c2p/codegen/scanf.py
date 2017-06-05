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
    code = CodeNode()
    loop_label = Label('scanf_loop')
    done_label = Label('scanf_done')

    ################################### Stack after this opcode: #
    ##############################################################
    # Push address to write to.
    code.add(node)                    # q
    code.add(loop_label)              # q
    # Dpl address and read a character.
    code.add(Dpl(PAddress))           # q, q
    code.add(In(PCharacter))          # q, q, c

    # If it's ESC (ASCII 27), jump to done.
    code.add(Dpl(PCharacter))         # q, q, c, c
    code.add(Ldc(PCharacter, 27))     # q, q, c, c, 27
    code.add(Neq(PCharacter))         # q, q, c, c != 27
    code.add(Fjp(done_label.label))   # q, q, c

    # Write it to the array.
    code.add(Sto(PCharacter))         # q
    code.add(Inc(PAddress, 1))        # q+1
    code.add(Ujp(loop_label.label))

    code.add(done_label)              # q, q, c
    # Write a NULL byte.
    code.add(Ldc(PCharacter, 0))      # q, q, c, 0
    code.add(Sli(PCharacter))         # q, q, 0
    code.add(Sto(PCharacter))         # q

    # Discard a value.
    code.add(Dpl(PAddress))
    code.add(Equ(PAddress))
    code.add(Fjp(done_label.label))

    code.type = CVoid()
    code.maxStackSpace = 6
    return code

def to_code(arguments: List[Expression], env: Environment, where: SourceInterval):
    # Get the format string.
    fmt = arguments[0]
    if not (fmt.__class__.__name__ == 'Constant' and isinstance(fmt.type.ignoreConst(), CArray)):
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
