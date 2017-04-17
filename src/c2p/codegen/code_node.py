from c2p.instructions import PInstruction
from typing import Union

class CodeNode:
    '''A class that holds generated code, and meta-data about this code.'''
    def __init__(self, code=None, type=None):
        self.code = code or []
        # Data useful to higher-up nodes
        self.type = type            # By and for Expressions
        self.maxStackSpace = 0      # By expressions and declarations, for functions
        self.foundMain = False      # By function defs, for Program

    def add(self, other : Union['CodeNode', PInstruction]) -> None:
        '''Add a new instruction, or append all instructions from another node.'''
        if isinstance(other, CodeNode):
            self.code += other.code
        else:
            self.code.append(other)
