from .base import PInstruction


class And(PInstruction):
    """Logically ANDs the top two booleans on the stack."""

    def emit(self) -> str:
        return 'and'


class Or(PInstruction):
    """Logically ORs the top two booleans on the stack."""

    def emit(self) -> str:
        return 'or'


class Not(PInstruction):
    """Logically NOTs the top boolean on the stack."""

    def emit(self) -> str:
        return 'not'
