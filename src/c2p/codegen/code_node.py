from c2p.instructions import PInstruction, Conv
from c2p.grammar.ctypes import CType
from typing import Union, Optional

class CodeNode:
    '''A class that holds generated code, and meta-data about this code.'''
    def __init__(self, code=None, type=None):
        self.code = code or []
        # Data useful to higher-up nodes
        self.type = type            # By and for Expressions
        self.maxStackSpace = 0      # By expressions and declarations, for functions
        self.foundMain = False      # By function defs, for Program

    def add(self, other : Union['CodeNode', PInstruction], desiredType : Optional[CType] = None) -> None:
        '''Add a new instruction, or append all instructions from another node.'''
        if isinstance(other, CodeNode):
            self.code += other.code
            if desiredType is not None and not other.type.equivalent(desiredType):
                self.code.append(Conv(other.type.ptype(), desiredType.ptype()))
        else:
            self.code.append(other)
