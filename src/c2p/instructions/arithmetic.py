from .base import PInstruction
from ..ptypes import PNumericType

class Add(PInstruction):
    def __init__(self, ptype: PNumericType) -> None:
        self.ptype = ptype

    def emit(self) -> str:
        return 'add %s' % self.ptype.letter

class Sub(PInstruction):
    def __init__(self, ptype: PNumericType) -> None:
        self.ptype = ptype

    def emit(self) -> str:
        return 'sub %s' % self.ptype.letter

class Mul(PInstruction):
    def __init__(self, ptype: PNumericType) -> None:
        self.ptype = ptype

    def emit(self) -> str:
        return 'mul %s' % self.ptype.letter

class Div(PInstruction):
    def __init__(self, ptype: PNumericType) -> None:
        self.ptype = ptype

    def emit(self) -> str:
        return 'div %s' % self.ptype.letter

class Neg(PInstruction):
    def __init__(self, ptype: PNumericType) -> None:
        self.ptype = ptype

    def emit(self) -> str:
        return 'neg %s' % self.ptype.letter
