from typing import Optional, Any
from ..ctypes import CVoid
from ...codegen.environment import Environment
from ...codegen.code_node import CodeNode
from ...codegen.error import SemanticError
from ... import instructions
from ...codegen.error import ASTError
from c2p.source_interval import SourceInterval

class ASTNode:
    def __init__(self, where: SourceInterval) -> None:
        self.where = where

    def to_code(self, env: Environment) -> CodeNode:
        raise NotImplementedError()

    def to_lcode(self, env: Environment) -> CodeNode:
        raise self.semanticError('{} is not a valid L-Value expression.'.format(self.__class__.__name__))

    def semanticError(self, message: Any) -> SemanticError:
        return SemanticError(message, self.where)

# A list of all invalid identifiers
keywords = ["void", "int", "void", "bool", "float", "if", "else", "where", "for", "break", "continue", "return", "const"]

class Identifier(ASTNode):
    def __init__(self, where: SourceInterval, name: str) -> None:
        super().__init__(where)
        if name in keywords:
            raise ASTError("Can't use keyword {} as an identifier.".format(name), self.where)
        self.name = name

Expression = Any

class ExprStatement(ASTNode):
    def __init__(self, where: SourceInterval, expression: Optional[Expression]) -> None:
        super().__init__(where)
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