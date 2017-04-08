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
    labels = []
    count = {}

    def __init__(self, label: str) -> None:
        if label not in labels:
            labels.append(label)
            count[label] = 0
            self.label = label
        else:
            while(label + str(count[label]) in labels):
                count[label] += 1
            labels.append(label + str(count[label]))
            self.label = newLabel

    def emit(self) -> str:
        return '%s:' % self.label
