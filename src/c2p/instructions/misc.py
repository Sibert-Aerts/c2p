from .base import PInstruction
from ..ptypes import PType


class New(PInstruction):
    """Allocate memory from the heap."""

    def emit(self) -> str:
        return 'new'


class Hlt(PInstruction):
    """Halt the P-machine."""

    def emit(self) -> str:
        return 'hlt'


class Conv(PInstruction):
    """Cast the top-of-stack from type T1 to type T2."""

    def __init__(self, t1: PType, t2: PType) -> None:
        self.t1 = t1
        self.t2 = t2

    def emit(self) -> str:
        return 'conv %s %s' % (self.t1.letter, self.t2.letter)


class Movs(PInstruction):
    """Pop an address, and block-copy q elements starting from there to the stack."""

    def __init__(self, q: int) -> None:
        self.q = q

    def emit(self) -> str:
        return 'movs %d' % self.q


class Movd(PInstruction):
    """Like movs, for dynamic arrays...?"""

    def __init__(self, q: int) -> None:
        self.q = q

    def emit(self) -> str:
        return 'movd %d' % self.q
