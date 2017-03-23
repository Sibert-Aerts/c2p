from .base import PInstruction
from ..ptypes import PType

class Equ(PInstruction):
    def __init__(self, ptype: PType) -> None:
        self.ptype = ptype

    def emit(self) -> str:
        return 'equ %s' % self.ptype.letter

class Geq(PInstruction):
    def __init__(self, ptype: PType) -> None:
        self.ptype = ptype

    def emit(self) -> str:
        return 'geq %s' % self.ptype.letter

class Leq(PInstruction):
    def __init__(self, ptype: PType) -> None:
        self.ptype = ptype

    def emit(self) -> str:
        return 'leq %s' % self.ptype.letter

class Les(PInstruction):
    def __init__(self, ptype: PType) -> None:
        self.ptype = ptype

    def emit(self) -> str:
        return 'les %s' % self.ptype.letter

class Grt(PInstruction):
    def __init__(self, ptype: PType) -> None:
        self.ptype = ptype

    def emit(self) -> str:
        return 'grt %s' % self.ptype.letter

class Neq(PInstruction):
    def __init__(self, ptype: PType) -> None:
        self.ptype = ptype

    def emit(self) -> str:
        return 'neq %s' % self.ptype.letter
