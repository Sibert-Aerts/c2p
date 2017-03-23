from typing import Any

from .base import PInstruction
from ..ptypes import PType

class Ldo(PInstruction):
    def __init__(self, ptype: PType, q: int) -> None:
        self.ptype = ptype
        self.q = q

    def emit(self) -> str:
        return 'ldo %s %d' % (self.ptype.letter, self.q)

class Ldc(PInstruction):
    def __init__(self, ptype: PType, q: Any) -> None:
        self.ptype = ptype
        self.q = q

    def emit(self) -> str:
        return 'ldc %s %s' % (self.ptype.letter, self.q)

class Ind(PInstruction):
    def __init__(self, ptype: PType) -> None:
        self.ptype = ptype

    def emit(self) -> str:
        return 'ind %s' % self.ptype.letter

class Sro(PInstruction):
    def __init__(self, ptype: PType, q: int) -> None:
        self.ptype = ptype
        self.q = q

    def emit(self) -> str:
        return 'sro %s %d' % (self.ptype.letter, self.q)

class Sto(PInstruction):
    def __init__(self, ptype: PType) -> None:
        self.ptype = ptype

    def emit(self) -> str:
        return 'sto %s' % self.ptype.letter
