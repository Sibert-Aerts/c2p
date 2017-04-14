from typing import Any, List, Optional, Union, Tuple, Callable
from ..ctypes import CArray, CConst, CChar, CInt, CFloat, CPointer, CType, CVoid, CBool
from ...codegen.environment import Environment
from ...codegen.code_node import CodeNode
from ...ptypes import PAddress
from ... import instructions

from .node_base import *

Expression = Any  # of the following:
class Comma(ASTNode):
    def __init__(self, left: Expression, right: Expression) -> None:
        self.left = left
        self.right = right

    def to_code(self, env: Environment) -> CodeNode:
        code = CodeNode()

        # Just treat the left hand side as an individual expression and move on.
        cl = ExprStatement(self.left).to_code(env)
        code.add(cl)
        cr = self.right.to_code(env)
        code.add(cr)
        code.type = cr.type

        code.maxStackSpace = max(cl.maxStackSpace, cr.maxStackSpace)

        return code

    def to_lcode(self, env: Environment) -> CodeNode:
        code = CodeNode()

        # the left hand side of a comma expression is basically just an independent statement right?
        cl = ExprStatement(self.left).to_code(env)
        code.add(cl)
        # Notice that this will cause an error unless the right instance is a valid L-value expression
        cr = self.right.to_lcode(env)
        code.add(cr)

        code.type = cr.type
        code.maxStackSpace = max(cl.maxStackSpace, cr.maxStackSpace)

        return code

class Assignment(ASTNode):
    def __init__(self, left: Expression, right: Expression) -> None:
        self.left = left
        self.right = right

    def to_code(self, env: Environment) -> CodeNode:
        code = CodeNode()

        # Load the left hand side as an L-Value, right hand side as an R-Value, and write R to L
        cl = self.left.to_lcode(env)
        code.add(cl)
        cr = self.right.to_code(env)
        code.add(cr)

        # TODO: type compatibility & implicit casting logic!
        if(cl.type != cr.type.ignoreConst()):
            raise ValueError('Incompatible assignment of {} to {}.'.format(cr.type, cl.type))

        code.add(instructions.Sto(cl.type.ptype()))

        code.type = cl.type
        code.maxStackSpace = max(cl.maxStackSpace, cr.maxStackSpace + 1)

        return code

class AddAssignment(ASTNode):
    def __init__(self, left: Expression, right: Expression) -> None:
        self.left = left
        self.right = right

    def to_code(self, env: Environment) -> CodeNode:
        raise NotImplementedError('TODO')

class SubAssignment(ASTNode):
    def __init__(self, left: Expression, right: Expression) -> None:
        self.left = left
        self.right = right

    def to_code(self, env: Environment) -> CodeNode:
        raise NotImplementedError('TODO')

class MulAssignment(ASTNode):
    def __init__(self, left: Expression, right: Expression) -> None:
        self.left = left
        self.right = right

    def to_code(self, env: Environment) -> CodeNode:
        raise NotImplementedError('TODO')

class DivAssignment(ASTNode):
    def __init__(self, left: Expression, right: Expression) -> None:
        self.left = left
        self.right = right

    def to_code(self, env: Environment) -> CodeNode:
        raise NotImplementedError('TODO')

class TernaryIf(ASTNode):
    def __init__(self, condition: Expression, left: Expression, right: Expression) -> None:
        self.condition = condition
        self.left = left
        self.right = right

    def to_code(self, env: Environment) -> CodeNode:
        raise NotImplementedError('TODO')


class BinaryBooleanOperationNode(ASTNode):
    '''A Node representing a binary expression between two binary expressions.'''
    def __init__(self, left: Expression, right: Expression, operation : Any) -> None:
        self.left = left
        self.right = right
        self.operation = operation

    def to_code(self, env: Environment) -> CodeNode:
        code = CodeNode()

        # Load the left hand side as an L-Value, right hand side as an R-Value
        cl = self.left.to_code(env)
        code.add(cl)
        cr = self.right.to_code(env)
        code.add(cr)

        # TODO: boolean conversions.
        for c in (cl, cr):
            if(c.type.ignoreConst() != CBool()):
                raise ValueError('Attempted to use variable of type {} as a boolean.'.format(cl.type))

        code.add(self.operation())

        code.type = CBool()
        code.maxStackSpace = max(cl.maxStackSpace, cr.maxStackSpace + 1)

        return code

class LogicalOr(BinaryBooleanOperationNode):
    def __init__(self, left: Expression, right: Expression) -> None:
        BinaryBooleanOperationNode.__init__(self, left, right, instructions.Or)

class LogicalAnd(BinaryBooleanOperationNode):
    def __init__(self, left: Expression, right: Expression) -> None:
        BinaryBooleanOperationNode.__init__(self, left, right, instructions.And)


class ComparisonNode(ASTNode):
    '''A Node representing a boolean comparison between two expressions of any type.'''
    def __init__(self, left: Expression, right: Expression, operation : Any) -> None:
        self.left = left
        self.right = right
        self.operation = operation

    def to_code(self, env: Environment) -> CodeNode:
        code = CodeNode()

        cl = self.left.to_code(env)
        code.add(cl)
        cr = self.right.to_code(env)
        code.add(cr)

        # TODO: type compatibility & implicit casting logic!
        if(cl.type.ignoreConst() != cr.type.ignoreConst()):
            raise ValueError('Invalid comparison {} between values of type of {} and {}.'.format(self.operation.__name__, cr.type, cl.type))

        code.add(self.operation(cl.type.ptype()))

        code.type = CBool()
        code.maxStackSpace = max(cl.maxStackSpace, cr.maxStackSpace + 1)

        return code

class Equals(ComparisonNode):
    def __init__(self, left: Expression, right: Expression) -> None:
        ComparisonNode.__init__(self, left, right, instructions.Equ)

class NotEquals(ComparisonNode):
    def __init__(self, left: Expression, right: Expression) -> None:
        ComparisonNode.__init__(self, left, right, instructions.Neq)

class LessThan(ComparisonNode):
    def __init__(self, left: Expression, right: Expression) -> None:
        ComparisonNode.__init__(self, left, right, instructions.Les)

class GreaterThan(ComparisonNode):
    def __init__(self, left: Expression, right: Expression) -> None:
        ComparisonNode.__init__(self, left, right, instructions.Grt)

class LessThanEquals(ComparisonNode):
    def __init__(self, left: Expression, right: Expression) -> None:
        ComparisonNode.__init__(self, left, right, instructions.Leq)

class GreaterThanEquals(ComparisonNode):
    def __init__(self, left: Expression, right: Expression) -> None:
        ComparisonNode.__init__(self, left, right, instructions.Geq)

        
class BinaryNumericOperationNode(ASTNode):
    '''A Node representing a numeric expression between two numeric expressions.'''
    def __init__(self, left: Expression, right: Expression, operation : Any) -> None:
        self.left = left
        self.right = right
        self.operation = operation

    def to_code(self, env: Environment) -> CodeNode:
        code = CodeNode()

        cl = self.left.to_code(env)
        code.add(cl)
        cr = self.right.to_code(env)
        code.add(cr)

        # TODO: type compatibility & implicit casting logic!
        if(cl.type.ignoreConst() != cr.type.ignoreConst()):
            raise ValueError('Invalid operation {} between values of type of {} to {}.'.format(self.operation.__name__, cr.type, cl.type))

        code.add(self.operation(cl.type.ptype()))

        code.type = cl.type
        code.maxStackSpace = max(cl.maxStackSpace, cr.maxStackSpace + 1)

        return code

class Add(BinaryNumericOperationNode):
    def __init__(self, left: Expression, right: Expression) -> None:
        BinaryNumericOperationNode.__init__(self, left, right, instructions.Add)

class Subtract(BinaryNumericOperationNode):
    def __init__(self, left: Expression, right: Expression) -> None:
        BinaryNumericOperationNode.__init__(self, left, right, instructions.Sub)

class Multiply(BinaryNumericOperationNode):
    def __init__(self, left: Expression, right: Expression) -> None:
        BinaryNumericOperationNode.__init__(self, left, right, instructions.Mul)

class Divide(BinaryNumericOperationNode):
    def __init__(self, left: Expression, right: Expression) -> None:
        BinaryNumericOperationNode.__init__(self, left, right, instructions.Div)


class Cast(ASTNode):
    def __init__(self, type: CType, right: Expression) -> None:
        self.type = type
        self.right = right

    def to_code(self, env: Environment) -> CodeNode:
        raise NotImplementedError('TODO')

class PrefixIncrement(ASTNode):
    def __init__(self, inner: Expression) -> None:
        self.inner = inner

    def to_code(self, env: Environment) -> CodeNode:
        raise NotImplementedError('TODO')

class PostfixIncrement(ASTNode):
    def __init__(self, inner: Expression) -> None:
        self.inner = inner

    def to_code(self, env: Environment) -> CodeNode:
        raise NotImplementedError('TODO')

class PrefixDecrement(ASTNode):
    def __init__(self, inner: Expression) -> None:
        self.inner = inner

    def to_code(self, env: Environment) -> CodeNode:
        raise NotImplementedError('TODO')

class PostfixDecrement(ASTNode):
    def __init__(self, inner: Expression) -> None:
        self.inner = inner

    def to_code(self, env: Environment) -> CodeNode:
        raise NotImplementedError('TODO')

class AddressOf(ASTNode):
    def __init__(self, inner: Expression) -> None:
        self.inner = inner

    def to_code(self, env: Environment) -> CodeNode:
        code = CodeNode()

        # Getting the L-Value of something is the same as getting its address.
        c = self.inner.to_lcode()
        code.add(c)
        code.maxStackSpace = c.maxStackSpace

        return code

class Dereference(ASTNode):
    def __init__(self, inner: Expression) -> None:
        self.inner = inner

    def to_code(self, env: Environment) -> CodeNode:
        raise NotImplementedError('TODO')

    def to_lcode(self, env: Environment) -> CodeNode:
        code = CodeNode()

        c = self.inner.to_code(env)
        code.add(c)

        # make sure the inner code is of type pointer
        if isinstance(c.type, CPointer):
            print('we dereferencin a pointer ova here!')
            # the type of this expression is the type that's being pointed at
            code.type = c.type.t
        else:
            raise ValueError('Expression of type {} cannot be dereferenced into an L-Value.'.format(c.type))

        # We don't need to add any instructions, because of how assignment instructions work.
        code.maxStackSpace = c.maxStackSpace

        return code


class UnaryOperationNode(ASTNode):
    '''A Node representing an operation on an expression.'''
    def __init__(self, inner: Expression, reqType : Any, operation : Any) -> None:
        self.inner = inner
        self.reqType = reqType
        self.operation = operation

    def to_code(self, env: Environment) -> CodeNode:
        code = CodeNode()

        c = self.inner.to_code(env)
        code.add(c)

        if not isinstance(c.type.ignoreConst(), self.reqType):
            raise ValueError('Cannot perform operation {} on expression of type {}.'.format(self.__class__.__name__, c.type))

        code.add(self.operation(c.type.ptype()))

        code.type = c.type
        code.maxStackSpace = c.maxStackSpace

        return code

class LogicalNot(UnaryOperationNode):
    def __init__(self, inner: Expression) -> None:
        UnaryOperationNode.__init__(self, inner, CBool, instructions.Not)

class Negate(UnaryOperationNode):
    def __init__(self, inner: Expression) -> None:
        UnaryOperationNode.__init__(self, inner, (CInt, CFloat), instructions.Neg)

class Index(ASTNode):
    def __init__(self, array: Expression, index: Expression) -> None:
        self.array = array
        self.index = index

    def to_code(self, env: Environment) -> CodeNode:
        raise NotImplementedError('TODO')

    def to_lcode(self, env: Environment) -> CodeNode:
        code = CodeNode()

        # The array
        c = self.array.to_code(env)
        code.add(c)

        # TODO: Something about whether or not a const array or array of consts can be an L-Value?
        if isinstance(c.type, (CPointer, CArray)):
            print('we indexin an array ova here!!!!!')
            code.type = c.type.t
        else:
            raise ValueError('Expression of type {} cannot be indexed into an L-Value.'.format(c.type))

        # The index
        ic = self.index.to_code(env)
        if ic.type.ignoreConst() == CInt():
            # TODO: implement indexing instructions
            raise NotImplementedError()
        else:
            raise ValueError('Cannot use type {} as array index.'.format(ic.type))

        return code

class Call(ASTNode):
    def __init__(self, name: Expression, arguments: List[Expression]) -> None:
        self.name = name
        self.arguments = arguments

    def to_code(self, env: Environment) -> CodeNode:
        if isinstance(self.name, IdentifierExpression) and self.name.identifier.name == 'printf':
            return printf.to_code(self.arguments, env)

        raise NotImplementedError('TODO')

class Constant(ASTNode):
    def __init__(self, type: CConst, value: Any) -> None:
        self.type = type
        self.value = value

    def to_code(self, env: Environment) -> CodeNode:
        code = CodeNode()

        code.type = self.type
        val = self.value

        # Ask the environment to turn string literals into addresses.
        if code.type == CConst(CArray(CConst(CChar()))):
            val = env.add_string_literal(val)

        if self.type == CConst(CChar()):
            code.add(instructions.Ldc(code.type.ptype(), "'{}'".format(val)))
        else:    
            code.add(instructions.Ldc(code.type.ptype(), val))

        code.maxStackSpace = 1

        return code

class IdentifierExpression(ASTNode):
    def __init__(self, identifier: Identifier) -> None:
        self.identifier = identifier

    def to_code(self, env: Environment) -> CodeNode:
        code = CodeNode()

        var = env.get_variable(self.identifier.name)

        code.add(instructions.Lod(var.ptype, 0, var.address))
        code.type = var.ctype

        code.maxStackSpace = 1

        return code

    def to_lcode(self, env: Environment) -> CodeNode:
        code = CodeNode()

        var = env.get_variable(self.identifier.name)

        code.add(instructions.Lda(0, var.address))

        # TODO: Something about checking whether or not the variable is (at some level) const?
        code.type = var.ctype
        code.maxStackSpace = 1

        return code