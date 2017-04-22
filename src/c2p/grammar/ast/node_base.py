from typing import Optional, Any
from ..ctypes import CVoid
from ...codegen.environment import Environment
from ...codegen.code_node import CodeNode
from ...codegen.semantic_error import SemanticError
from ... import instructions

class ASTNode:
    def to_code(self, env: Environment) -> CodeNode:
        raise NotImplementedError()

    def to_lcode(self, env: Environment) -> CodeNode:
        raise SemanticError('{} is not a valid L-Value expression.'.format(self.__class__.__name__))


class Identifier(ASTNode):
    def __init__(self, name: str) -> None:
        self.name = name

Expression = Any

class ExprStatement(ASTNode):
    def __init__(self, expression: Optional[Expression]) -> None:
        self.expression = expression

    def to_code(self, env: Environment) -> CodeNode:
        code = CodeNode()

        if self.expression is None:
            return code

        c = self.expression.to_code(env)
        code.add(c)

        if c.type is None:
            raise NotImplementedError('Forgot to set the type when compiling {}!'.format(self.expression.__class__.__name__))
        if c.maxStackSpace == 0:
            raise NotImplementedError('Forgot to set the maxStackSpace when compiling {}!'.format(self.expression.__class__.__name__))

        # discard the top of stack...
        # there is no instruction that simply does SP := SP - 1...
        # ...so just write the top of the stack to 0?
        # TODO: figure out what better to do with the useless top-of-stack in an ExprStmt
        if c.type != CVoid():
            code.add(instructions.Sro(c.type.ptype(), 0))

        code.maxStackSpace = c.maxStackSpace

        return code