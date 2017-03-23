from .base import PInstruction
from ..ptypes import PType


class In(PInstruction):
    """Read a value of type T from STDIN and push it."""

    def __init__(self, t: PType) -> None:
        self.t = t

    def emit(self) -> str:
        return 'in %s' % self.t.letter


class Out1(PInstruction):
    """Pop a value of type T and write it to STDOUT."""

    def __init__(self, t: PType) -> None:
        self.t = t

    def emit(self) -> str:
        return 'out %s' % self.t.letter


class Out2(PInstruction):
    """Pop a precision and a real value, and write it to STDOUT."""

    def emit(self) -> str:
        return 'out r i'
