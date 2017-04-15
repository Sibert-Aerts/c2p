from typing import Any, List
from .environment import Environment
from .code_node import CodeNode
from ..grammar.ctypes import *
from ..instructions import *

Expression = Any
def to_code(arguments: List[Expression], env: Environment):
    print(arguments[0])
    # HACK for circular dependency :(((
    fmt = arguments[0]
    assert fmt.__class__.__name__ == 'Constant'
    assert fmt.type == CConst(CArray(CConst(CChar())))
    # TODO: what is this address and why is it wrong
    address = env.add_string_literal(fmt.value)

    loop_label = Label('printf_loop')
    done_label = Label('printf_done')

    code = CodeNode()

    ################################### Stack after this opcode: #
    ##############################################################
    code.add(Ldc(PAddress, address))  # q
    code.add(loop_label)              # q
    # Get the character.
    code.add(Dpl(PAddress))           # q, q
    code.add(Ind(PCharacter))         # q, STORE[q]

    # If it's zero, jump to done.
    code.add(Dpl(PCharacter))         # q, STORE[q], STORE[q]
    code.add(Ldc(PCharacter, "'0'"))  # q, STORE[q], STORE[q], 0
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
