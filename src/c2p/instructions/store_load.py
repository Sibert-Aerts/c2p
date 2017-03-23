from typing import Any

from .base import PInstruction
from ..ptypes import PType


class Ldo(PInstruction):
    """Pushes STORE[q], which has type T."""

    def __init__(self, t: PType, q: int) -> None:
        self.t = t
        self.q = q

    def emit(self) -> str:
        return 'ldo %s %d' % (self.t.letter, self.q)


class Ldc(PInstruction):
    """Pushes a constant q, which has type T."""

    def __init__(self, t: PType, q: Any) -> None:
        self.t = t
        self.q = q

    def emit(self) -> str:
        return 'ldc %s %s' % (self.t.letter, self.q)


class Ind(PInstruction):
    """Pushes STORE[pop()], which has type T."""

    def __init__(self, t: PType) -> None:
        self.t = t

    def emit(self) -> str:
        return 'ind %s' % self.t.letter


class Sro(PInstruction):
    """Sets STORE[q] to pop(), which has type T."""

    def __init__(self, t: PType, q: int) -> None:
        self.t = t
        self.q = q

    def emit(self) -> str:
        return 'sro %s %d' % (self.t.letter, self.q)


class Sto(PInstruction):
    """Pops (x:T), then pops (j:addr), then sets STORE[j] to x."""

    def __init__(self, t: PType) -> None:
        self.t = t

    def emit(self) -> str:
        return 'sto %s' % self.t.letter
