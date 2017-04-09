from .base import PInstruction
from ..ptypes import PType


class Ixa(PInstruction):
    """Indexed address computation:
            STORE[SP - 1] := STORE[SP - 1] + STORE[SP] * q
            SP := SP - 1
    """

    def __init__(self, q: int) -> None:
        self.q = q

    def emit(self) -> str:
        return 'ixa %d' % self.q


class Chk(PInstruction):
    """Error if the integer on top of the stack isn't in [p, q]."""

    def __init__(self, p: int, q: int) -> None:
        self.p = p
        self.q = q

    def emit(self) -> str:
        return 'chk %d %d' % (self.p, self.q)


class Dpl(PInstruction):
    """Duplicate the top-of-stack."""

    def __init__(self, t: PType) -> None:
        self.t = t

    def emit(self) -> str:
        return 'dpl %s' % self.t.letter


class Ldd(PInstruction):
    """Dynamic array loading helper:
            SP := SP + 1
            STORE[SP] := STORE[STORE[SP - 3] + q]
    """

    def __init__(self, q: int) -> None:
        self.q = q

    def emit(self) -> str:
        return 'ldd %d' % self.q


class Sli(PInstruction):
    """Slide: remove the element *below* the top element on the stack. The type in `sli T`
    should be that of the top element."""

    def __init__(self, t: PType) -> None:
        self.t = t

    def emit(self) -> str:
        return 'sli %s' % self.t.letter
