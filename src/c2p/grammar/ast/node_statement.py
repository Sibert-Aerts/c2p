from typing import Any, List, Optional, Union, Tuple, Callable
from ..ctypes import CArray, CConst, CChar, CInt, CFloat, CPointer, CType, CVoid, CBool
from ...codegen.environment import Environment
from ...codegen.code_node import CodeNode
from ...ptypes import PAddress
from ... import instructions

from .node_base import *
from .node_expression import *
from .node_decl import *

# Statements
Statement = Any  # of the following:
class CondStatement(ASTNode):
    def __init__(self, condition: Expression, trueBody: Statement, falseBody: Optional[Statement]) -> None:
        self.condition = condition
        self.trueBody = trueBody
        self.falseBody = falseBody

    def to_code(self, env: Environment) -> CodeNode:
        code = CodeNode()

        # The Label class ensures that these are unique
        falseLabel = instructions.Label('ifFalse')
        endLabel = instructions.Label('ifEnd')

        ccond = self.condition.to_code(env)
        code.add(ccond)
        code.add(instructions.Fjp(falseLabel.label))

        ctrue = self.trueBody.to_code(env)
        code.add(ctrue)

        if self.falseBody:
            code.add(instructions.Ujp(endLabel.label))
            code.add(falseLabel)
            cf = self.falseBody.to_code(env)
            code.maxStackSpace = cf.maxStackSpace
            code.add(cf)
            code.add(endLabel)
        else:
            code.add(falseLabel)

        code.maxStackSpace = max(code.maxStackSpace, ccond.maxStackSpace, ctrue.maxStackSpace)

        return code

class WhileStatement(ASTNode):
    def __init__(self, condition: Expression, body: Statement) -> None:
        self.condition = condition
        self.body = body

    def to_code(self, env: Environment) -> CodeNode:
        code = CodeNode()

        # The Label class ensures that these are unique
        startLabel = instructions.Label('whileStart')
        endLabel = instructions.Label('whileEnd')

        # Define this scope as a loop, and tell the code where to jump to
        # in case of a break (end) or continue (start)
        env.set_as_loop(endLabel, startLabel)

        ccond = self.condition.to_code(env)
        cbody = self.body.to_code(env)

        code.add(startLabel)
        code.add(ccond)
        code.add(instructions.Fjp(endLabel.label))
        code.add(cbody)
        code.add(instructions.Ujp(startLabel.label))
        code.add(endLabel)

        code.maxStackSpace = max(ccond.maxStackSpace, cbody.maxStackSpace)

        return code

class ForStatement(ASTNode):
    def __init__(self, left: Optional[Union['Declaration', Expression]], center: Optional[Expression], right: Optional[Expression], body: Statement) -> None:
        self.left = left
        self.center = center
        self.right = right
        self.body = body

    def to_code(self, env: Environment) -> CodeNode:
        code = CodeNode()

        # The Label class ensures that these are unique
        startLabel = instructions.Label('whileStart')
        endLabel = instructions.Label('whileEnd')

        # Define this scope as a loop, and tell the code where to jump to
        # in case of a break (end) or continue (start)
        env.set_as_loop(endLabel, startLabel)

        # Manually deepen.
        env.deepen()

        # Compile the different parts of the statement, if they exist
        cleft = None
        if self.left:
            if isinstance(self.left, Declaration):
                cleft = self.left.to_code(env)
            else: # cleft is an Expression
                cleft = ExprStatement(self.left).to_code(env)
            code.maxStackSpace = max(code.maxStackSpace, cleft.maxStackSpace)
        
        ccond = None
        if self.center:
            ccond = self.center.to_code(env)
            code.maxStackSpace = max(code.maxStackSpace, ccond.maxStackSpace)

        cright = None
        if self.right:
            cright = ExprStatement(self.right).to_code(env)
            code.maxStackSpace = max(code.maxStackSpace, cright.maxStackSpace)

        cbody = None
        if isinstance(self.body, CompoundStatement):
            cbody = blockstmt_to_code(self.body, env)
        else:
            cbody = self.body.to_code(env)
        code.maxStackSpace = max(code.maxStackSpace, cbody.maxStackSpace)

        if self.left:
            code.add(cleft)
        code.add(startLabel)
        if self.center:
            code.add(ccond)
            code.add(instructions.Fjp(endLabel.label))
        code.add(cbody)
        if self.right:
            code.add(cright)
        code.add(instructions.Ujp(startLabel.label))
        code.add(endLabel)

        env.undeepen()

        return code

class BreakStatement(ASTNode):
    def __init__(self) -> None:
        pass

    def to_code(self, env: Environment) -> CodeNode:
        code = CodeNode()

        loopScope = env.find_loop()

        # Check if we're inside a loop or not
        if loopScope is None:
            ValueError('Attempted to "break" outside a loop.')

        code.add(instructions.Ujp(loopScope.breakLabel))

        return code

class ContinueStatement(ASTNode):
    def __init__(self) -> None:
        pass

    def to_code(self, env: Environment) -> CodeNode:
        code = CodeNode()

        loopScope = env.find_loop()

        # Check if we're inside a loop or not
        if loopScope is None:
            ValueError('Attempted to "continue" outside a loop.')

        code.add(instructions.Ujp(loopScope.continueLabel))

        return code

class ReturnStatement(ASTNode):
    def __init__(self, expression: Optional[Expression]) -> None:
        self.expression = expression

    def to_code(self, env: Environment) -> CodeNode:
        if self.expression:
            code = CodeNode()
            c = self.expression.to_code(env)
            code.add(c)

            # TODO: type compatibility
            # Ensure we're returning the right thing
            if c.type.ignoreConst() != env.returnType.ignoreConst():
                raise ValueError('Attempted to return expression of type {}, expected {}.'.format(c.type, env.returnType))

            # Put the return value where we can find it later: On top of the previous stack, where MP points to
            code.add(instructions.Str(c.type.ptype(), 0, 0))
            # Return with value
            code.add(instructions.Retf())
            return code
        else:
            if env.returnType != CVoid():
                raise ValueError('Cannot return an expression in a function that returns void.')

            code = CodeNode()
            # Return without value
            code.add(instructions.Retp())
            return code

def blockstmt_to_code(compStmt: 'CompoundStatement', env: Environment) -> CodeNode:
    # Special case of CompoundStatement.to_code needed by FunctionDefinition
    # Does not first deepen / undeepen at the end, so that FuncDef can insert the arguments first
    code = CodeNode()

    declCount = 0
    for stmt in compStmt.statements:
        c = stmt.to_code(env)
        code.add(c)
        # max stack space is the max space any statement uses.
        code.maxStackSpace = max(code.maxStackSpace, c.maxStackSpace)

    return code

class CompoundStatement(ASTNode):
    def __init__(self, statements: List[Union['Declaration', Statement]]) -> None:
        self.statements = statements

    def to_code(self, env: Environment) -> CodeNode:
        env.deepen()
        code = blockstmt_to_code(self, env)
        env.undeepen()

        return code