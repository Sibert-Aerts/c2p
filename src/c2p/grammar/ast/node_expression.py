from typing import Any, List, Optional, Union, Tuple, Callable
from ..ctypes import CArray, CConst, CChar, CInt, CFloat, CPointer, CType, CVoid, CBool
from ...codegen.environment import Environment
from ...codegen.code_node import CodeNode
from ...codegen import printf
from ...ptypes import *
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


class OperationAssignment(ASTNode):
    def __init__(self, left: Expression, right: Expression, operation : Optional[Any]) -> None:
        self.left = left
        self.right = right
        self.operation = operation

    def to_code(self, env: Environment) -> CodeNode:
        code = CodeNode()

        # Load the left hand side as an L-Value, right hand side as an R-Value, and write R to L
        cl = self.left.to_lcode(env)
        lType = cl.type.ptype()
        code.add(cl)
        # Duplicate the value produced by the left expression
        code.add(instructions.Dpl(PAddress))

        if self.operation:
            # Get the current value of the l-side object (if we need it)
            code.add(instructions.Dpl(PAddress))
            code.add(instructions.Ind(lType))

        cr = self.right.to_code(env)
        code.add(cr)

        # TODO: type compatibility & implicit casting logic!
        if(cl.type != cr.type.ignoreConst()):
            raise ValueError('Incompatible assignment of {} to {}.'.format(cr.type, cl.type))

        # Apply the operation (if any)
        if self.operation:
            code.add(self.operation(lType))

        # Store the value from the right expression into the addres from the left expression
        code.add(instructions.Sto(lType))

        # Finally, load the value from the left expression back onto the stack for further use in expressions
        code.add(instructions.Ind(lType))

        code.type = cl.type
        code.maxStackSpace = max(cl.maxStackSpace, cr.maxStackSpace + 2)

        return code

class Assignment(OperationAssignment):
    def __init__(self, left: Expression, right: Expression) -> None:
        OperationAssignment.__init__(self, left, right, None)

class AddAssignment(OperationAssignment):
    def __init__(self, left: Expression, right: Expression) -> None:
        OperationAssignment.__init__(self, left, right, instructions.Add)

class SubAssignment(OperationAssignment):
    def __init__(self, left: Expression, right: Expression) -> None:
        OperationAssignment.__init__(self, left, right, instructions.Sub)

class MulAssignment(OperationAssignment):
    def __init__(self, left: Expression, right: Expression) -> None:
        OperationAssignment.__init__(self, left, right, instructions.Mul)

class DivAssignment(OperationAssignment):
    def __init__(self, left: Expression, right: Expression) -> None:
        OperationAssignment.__init__(self, left, right, instructions.Div)

class TernaryIf(ASTNode):
    def __init__(self, condition: Expression, left: Expression, right: Expression) -> None:
        self.condition = condition
        self.left = left
        self.right = right

    def to_code(self, env: Environment) -> CodeNode:
        code = CodeNode()

        cc = self.condition.to_code(env)
        cl = self.left.to_code(env)
        cr = self.right.to_code(env)

        # TODO: type equivalence
        if cl.type.ignoreConst() != cr.type.ignoreConst():
            raise ValueError('Incompatible ternary expression of both types {} and {}'.format(cl.type, cr.type))

        code.type = cl.type.ignoreConst()

        if cc.type.ignoreConst() != CBool():
            # TODO: boolean conversion
            raise ValueError('Invalid boolean expression of type {}'.format(cc.type))

        # Make labels (the Label class ensures the labels are unique)
        falseLabel = instructions.Label('ternfalse')
        endLabel = instructions.Label('ternend')

        # Verify condition
        code.add(cc)
        code.add(instructions.Fjp(falseLabel.label))
        # If true: evaluate left expression
        code.add(cl)
        code.add(instructions.Ujp(endLabel.label))
        # If false: evaluate right expression
        code.add(falseLabel)
        code.add(cr)
        # End up at the end in either case
        code.add(endLabel)

        # None of the expressions are ever simultaneously loaded onto the stack
        code.maxStackSpace = max(cc.maxStackSpace, cl.maxStackSpace, cr.maxStackSpace)

        return code


class BinaryBooleanOperationNode(ASTNode):
    '''A Node representing a binary operation between two boolean expressions.'''
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

class PrefixNode(ASTNode):
    '''Node representing a prefix increment/decrement.'''
    def __init__(self, inner: Expression, operation : Any) -> None:
        self.inner = inner
        self.operation = operation

    def to_code(self, env: Environment) -> CodeNode:
        code = CodeNode()

        c = self.inner.to_lcode(env)
        t = c.type.ptype()

        # Put the expression's address on the stack thrice
        code.add(c)
        code.add(instructions.Dpl(PAddress))
        code.add(instructions.Dpl(PAddress))

        # Put the expression's actual value on the stack
        code.add(instructions.Ind(t))
        # crement it
        code.add(self.operation(t, 1))
        # Store it
        code.add(instructions.Sto(t))

        # Indirect: Load the newly cremented value on the stack
        code.add(instructions.Ind(t))

        code.type = c.type
        code.maxStackSpace = max(c.maxStackSpace, 3)

        return code

class PrefixIncrement(PrefixNode):
    def __init__(self, inner: Expression) -> None:
        PrefixNode.__init__(self, inner, instructions.Inc)

class PrefixDecrement(PrefixNode):
    def __init__(self, inner: Expression) -> None:
        PrefixNode.__init__(self, inner, instructions.Dec)


class PostfixNode(ASTNode):
    '''Node representing a postfix increment/decrement.'''
    def __init__(self, inner: Expression, operation : Any) -> None:
        self.inner = inner
        self.operation = operation

    def to_code(self, env: Environment) -> CodeNode:
        code = CodeNode()

        c = self.inner.to_lcode(env)
        t = c.type.ptype()

        # Put the expression's address on the stack thrice
        code.add(c)
        code.add(instructions.Dpl(PAddress))
        code.add(instructions.Dpl(PAddress))

        # Put the expression's actual value on the stack
        code.add(instructions.Ind(t))
        # crement it
        code.add(self.operation(t, 1))
        # Store it
        code.add(instructions.Sto(t))

        # Indirect: Load the newly cremented value on the stack
        code.add(instructions.Ind(t))

        # How do you nicely set the old value as the top of stack without being able to load/assign
        # relative to the top-of-stack? The stack-based instructions are supposed to make it easier...
        # (and don't think about just adding the expression's l-code twice,
        # because that'll cause its code to execute twice!)

        # TODO: HACK: uncrement it again
        if self.operation == instructions.Inc:
            code.add(instructions.Dec(t, 1))
        else:
            code.add(instructions.Inc(t, 1))

        code.type = c.type
        code.maxStackSpace = max(c.maxStackSpace, 3)

        return code

class PostfixIncrement(PostfixNode):
    def __init__(self, inner: Expression) -> None:
        PostfixNode.__init__(self, inner, instructions.Inc)

class PostfixDecrement(PostfixNode):
    def __init__(self, inner: Expression) -> None:
        PostfixNode.__init__(self, inner, instructions.Dec)


class AddressOf(ASTNode):
    def __init__(self, inner: Expression) -> None:
        self.inner = inner

    def to_code(self, env: Environment) -> CodeNode:
        code = CodeNode()

        # Getting the L-Value of something is the same as getting its address.
        c = self.inner.to_lcode(env)
        code.add(c)

        # The expression is now of type pointer to (inner type)
        code.type = CPointer(c.type)
        code.maxStackSpace = c.maxStackSpace

        return code

class Dereference(ASTNode):
    def __init__(self, inner: Expression) -> None:
        self.inner = inner

    def to_code(self, env: Environment) -> CodeNode:
        code = CodeNode()

        c = self.inner.to_code(env)

        # Ensure it's a pointer
        if isinstance(c.type.ignoreConst(), CPointer):
            # the type of this expression is the type that's being pointed at (CPointer.t)
            code.type = c.type.t
        else:
            raise ValueError('Expression of type {} cannot be dereferenced.'.format(c.type))

        code.add(c)
        code.add(instructions.Ind(c.type.t.ptype()))

        code.maxStackSpace = c.maxStackSpace

        return  code

    def to_lcode(self, env: Environment) -> CodeNode:
        code = CodeNode()

        c = self.inner.to_code(env)
        code.add(c)

        # Ensure it's a const-free pointer
        if isinstance(c.type, CPointer) and c.type == c.type.ignoreConst():
            # the type of this expression is the type that's being pointed at (CPointer.t)
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
        ca = self.array.to_code(env)

        # Ensure the array is indexable and is also const-free
        if isinstance(ca.type, (CPointer, CArray)) and ca.type.ignoreConst() == ca.type:
            code.type = ca.type.t
        else:
            raise ValueError('Expression of type {} cannot be indexed into an L-Value.'.format(ca.type))

        # The index
        ci = self.index.to_code(env)
        if ci.type.ignoreConst() == CInt():
            # Load array and index onto stack
            code.add(ca)
            code.add(ci)
            # Get the length of one item (perhaps another array) from the array we're indexing
            length = self.array.t.size()
            code.add(instructions.Ixa(length))
        else:
            raise ValueError('Cannot use expression of type {} as index.'.format(ci.type))

        return code

class Call(ASTNode):
    def __init__(self, name: Expression, arguments: List[Expression]) -> None:
        self.name = name
        self.arguments = arguments

    def to_code(self, env: Environment) -> CodeNode:
        if isinstance(self.name, IdentifierExpression) and self.name.identifier.name == 'printf':
            return printf.to_code(self.arguments, env)
        
        code = CodeNode()

        # Mark the new frame
        code.add(instructions.Mst(0))

        # Identify the called function (if it exists)
        if not isinstance(self.name, IdentifierExpression):
            raise ValueError('Call to non-identifier.')

        name = self.name.identifier.name
        returnType, signature, label = env.get_function(name)

        # Verify the number of arguments
        if len(signature) != len (self.arguments):
            raise ValueError('Invalid call to "{}": Expected {} arguments, got {}.' \
                .format(name, len(signature), len(self.arguments)))

        # Load the arguments onto the stack and verify their types
        for sig, arg in zip(signature, self.arguments):    # sig:CType, arg:Expression
            # Add the code to load the argument onto the stack
            c = arg.to_code(env)
            code.add(c)

            # TODO: Type compatibility
            if c.type.ignoreConst() != sig.ignoreConst():
                raise ValueError('Invalid call to "{}": Expected expression of type {}, got {}.' \
                    .format(name, arg, c.type))
        
        argSize = sum([s.ptype().size() for s in signature])

        # Make the call
        code.add(instructions.Cup(argSize, label))

        # If the function returns, this should consume everything we put on the stack and
        # put a single value of type returnType on the stack.
        code.type = returnType

        return code

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