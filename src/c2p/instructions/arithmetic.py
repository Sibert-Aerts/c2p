from .base import PInstruction
from ..ptypes import PType, PNumericType


class Add(PInstruction):
    """Adds the top two elements on the stack (of type N)."""

    def __init__(self, n: PNumericType) -> None:
        self.n = n

    def emit(self) -> str:
        return 'add %s' % self.n.letter


class Sub(PInstruction):
    """Subtracts the top two elements on the stack (of type N)."""

    def __init__(self, n: PNumericType) -> None:
        self.n = n

    def emit(self) -> str:
        return 'sub %s' % self.n.letter


class Mul(PInstruction):
    """Multiplies the top two elements on the stack (of type N)."""

    def __init__(self, n: PNumericType) -> None:
        self.n = n

    def emit(self) -> str:
        return 'mul %s' % self.n.letter


class Div(PInstruction):
    """Divides the top two elements on the stack (of type N)."""

    def __init__(self, n: PNumericType) -> None:
        self.n = n

    def emit(self) -> str:
        return 'div %s' % self.n.letter


class Neg(PInstruction):
    """Negates the top element on the stack (of type N)."""

    def __init__(self, n: PNumericType) -> None:
        self.n = n

    def emit(self) -> str:
        return 'neg %s' % self.n.letter


class Inc(PInstruction):
    """Increment the top-of-stack (of type T) by q (of type int)."""

    def __init__(self, t: PType, q: int) -> None:
        self.t = t
        self.q = q

    def emit(self) -> str:
        return 'inc %s %d' % (self.t, self.q)


class Dec(PInstruction):
    """Decrement the top-of-stack (of type T) by q (of type int)."""

    def __init__(self, t: PType, q: int) -> None:
        self.t = t
        self.q = q

    def emit(self) -> str:
        return 'dec %s %d' % (self.t, self.q)
