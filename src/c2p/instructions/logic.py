from .base import PInstruction

class And(PInstruction):
    def emit(self) -> str:
        return 'and'

class Or(PInstruction):
    def emit(self) -> str:
        return 'or'

class Not(PInstruction):
    def emit(self) -> str:
        return 'not'
