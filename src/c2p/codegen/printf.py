from typing import Any, List
from .environment import Environment
from .code_node import CodeNode
from .error import SemanticError
from ..grammar.ctypes import *
from ..instructions import *
from c2p.source_interval import SourceInterval

Expression = Any
def to_code(arguments: List[Expression], env: Environment, where: SourceInterval):
    # TODO: actually make this thing print more than strings
    # important: this has to happen in C code? unsure.

    string = arguments[0]

    cs = string.to_code(env)
    if cs.type.ignoreConst() != CArray(CChar()):
        raise SemanticError('Invalid call to "printf" with argument of type {}, expected {}.'.format(cs.type, CArray(CChar())), where)

    # Load the string's address onto the stack

    loop_label = Label('printf_loop')
    done_label = Label('printf_done')

    code = CodeNode()

    ################################### Stack after this opcode: #
    ##############################################################
    code.add(cs)
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
