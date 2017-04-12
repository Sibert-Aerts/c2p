from typing import Set
from .base import PInstruction


class Ujp(PInstruction):
    """Unconditionally jumps to the given label."""

    def __init__(self, label: str) -> None:
        self.label = label

    def emit(self) -> str:
        return 'ujp %s' % self.label


class Fjp(PInstruction):
    """Jumps to the given label if pop() is false."""

    def __init__(self, label: str) -> None:
        self.label = label

    def emit(self) -> str:
        return 'fjp %s' % self.label


class Ixj(PInstruction):
    """Indexed jump: unconditionally jumps to pop() + label."""

    def __init__(self, label: str) -> None:
        self.label = label

    def emit(self) -> str:
        return 'ixj %s' % self.label


class Label(PInstruction):
    """A P-machine label. (This isn't really an instruction.)"""
    labels = set() # type: Set[str]

    def __init__(self, label: str) -> None:
        while label in self.labels:
            label += '_'
        self.labels.add(label)
        self.label = label

    def emit(self) -> str:
        return '%s:' % self.label
