from .base import PInstruction
from ..ptypes import PType


# TODO: document all of these.

class Mst(PInstruction):
    def __init__(self, p: int) -> None:
        self.p = p

    def emit(self) -> str:
        return 'mst %d' % self.p


class Cup(PInstruction):
    def __init__(self, p: int, label: str) -> None:
        self.p = p
        self.label = label

    def emit(self) -> str:
        return 'cup %d %s' % (self.p, self.label)


class Ssp(PInstruction):
    def __init__(self, p: int) -> None:
        self.p = p

    def emit(self) -> str:
        return 'ssp %d' % self.p


class Sep(PInstruction):
    def __init__(self, p: int) -> None:
        self.p = p

    def emit(self) -> str:
        return 'sep %d' % self.p


class Ent(PInstruction):
    def __init__(self, p: int, q: int) -> None:
        self.p = p
        self.q = q

    def emit(self) -> str:
        return 'ent %d %d' % (self.p, self.q)


class Retf(PInstruction):
    def emit(self) -> str:
        return 'retf'


class Retp(PInstruction):
    def emit(self) -> str:
        return 'retp'


class Smp(PInstruction):
    def __init__(self, p: int) -> None:
        self.p = p

    def emit(self) -> str:
        return 'smp %d' % self.p


class Cupi(PInstruction):
    def __init__(self, p: int, q: int) -> None:
        self.p = p
        self.q = q

    def emit(self) -> str:
        return 'cupi %d %d' % (self.p, self.q)


class Mstf(PInstruction):
    def __init__(self, p: int, q: int) -> None:
        self.p = p
        self.q = q

    def emit(self) -> str:
        return 'mstf %d %d' % (self.p, self.q)
