from ...codegen.environment import Environment
from ...codegen.code_node import CodeNode

class ASTNode:
    def to_code(self, env: Environment) -> CodeNode:
        raise NotImplementedError()

    def to_lcode(self, env: Environment) -> CodeNode:
        raise ValueError('{} is not a valid L-Value expression'.format(self.__class__.__name__))


class Identifier(ASTNode):
    def __init__(self, name: str) -> None:
        self.name = name