from .base import PInstruction
from ..ptypes import PType


class Equ(PInstruction):
    """Pops (b: T), then (a: T), then pushes (a = b)."""

    def __init__(self, t: PType) -> None:
        self.t = t

    def emit(self) -> str:
        return 'equ %s' % self.t.letter


class Geq(PInstruction):
    """Pops (b: T), then (a: T), then pushes (a ≥ b)."""

    def __init__(self, t: PType) -> None:
        self.t = t

    def emit(self) -> str:
        return 'geq %s' % self.t.letter


class Leq(PInstruction):
    """Pops (b: T), then (a: T), then pushes (a ≤ b)."""

    def __init__(self, t: PType) -> None:
        self.t = t

    def emit(self) -> str:
        return 'leq %s' % self.t.letter


class Les(PInstruction):
    """Pops (b: T), then (a: T), then pushes (a < b)."""

    def __init__(self, t: PType) -> None:
        self.t = t

    def emit(self) -> str:
        return 'les %s' % self.t.letter


class Grt(PInstruction):
    """Pops (b: T), then (a: T), then pushes (a > b)."""

    def __init__(self, t: PType) -> None:
        self.t = t

    def emit(self) -> str:
        return 'grt %s' % self.t.letter


class Neq(PInstruction):
    """Pops (b: T), then (a: T), then pushes (a ≠ b)."""

    def __init__(self, t: PType) -> None:
        self.t = t

    def emit(self) -> str:
        return 'neq %s' % self.t.letter
