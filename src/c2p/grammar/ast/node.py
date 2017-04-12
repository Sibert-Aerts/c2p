from typing import Any, List, Optional, Union, Tuple
from ..ctypes import CArray, CConst, CInt, CPointer, CType, CVoid
from ...codegen.environment import Environment
from ...codegen.code_node import CodeNode
from ...ptypes import PAddress
from ... import instructions
# from ..ptypes import PType, PAddress, PBoolean, PCharacter, PInteger, PReal

### AST nodes
class ASTNode:
    def to_code(self, env: Environment) -> CodeNode:
        raise NotImplementedError()

    def to_lcode(self, env: Environment) -> CodeNode:
        raise ValueError('{} is not a valid L-Value expression'.format(self.__class__.__name__))


class Identifier(ASTNode):
    def __init__(self, name: str) -> None:
        self.name = name

    def to_code(self, env: Environment) -> CodeNode:
        raise NotImplementedError('TODO')


# Expressions
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

class LogicalOr(ASTNode):
    def __init__(self, left: Expression, right: Expression) -> None:
        self.left = left
        self.right = right

    def to_code(self, env: Environment) -> CodeNode:
        raise NotImplementedError('TODO')

class LogicalAnd(ASTNode):
    def __init__(self, left: Expression, right: Expression) -> None:
        self.left = left
        self.right = right

    def to_code(self, env: Environment) -> CodeNode:
        raise NotImplementedError('TODO')

class Equals(ASTNode):
    def __init__(self, left: Expression, right: Expression) -> None:
        self.left = left
        self.right = right

    def to_code(self, env: Environment) -> CodeNode:
        raise NotImplementedError('TODO')

class NotEquals(ASTNode):
    def __init__(self, left: Expression, right: Expression) -> None:
        self.left = left
        self.right = right

    def to_code(self, env: Environment) -> CodeNode:
        raise NotImplementedError('TODO')

class LessThan(ASTNode):
    def __init__(self, left: Expression, right: Expression) -> None:
        self.left = left
        self.right = right

    def to_code(self, env: Environment) -> CodeNode:
        raise NotImplementedError('TODO')

class GreaterThan(ASTNode):
    def __init__(self, left: Expression, right: Expression) -> None:
        self.left = left
        self.right = right

    def to_code(self, env: Environment) -> CodeNode:
        raise NotImplementedError('TODO')

class LessThanEquals(ASTNode):
    def __init__(self, left: Expression, right: Expression) -> None:
        self.left = left
        self.right = right

    def to_code(self, env: Environment) -> CodeNode:
        raise NotImplementedError('TODO')

class GreaterThanEquals(ASTNode):
    def __init__(self, left: Expression, right: Expression) -> None:
        self.left = left
        self.right = right

    def to_code(self, env: Environment) -> CodeNode:
        raise NotImplementedError('TODO')

class Add(ASTNode):
    def __init__(self, left: Expression, right: Expression) -> None:
        self.left = left
        self.right = right

    def to_code(self, env: Environment) -> CodeNode:
        raise NotImplementedError('TODO')

class Subtract(ASTNode):
    def __init__(self, left: Expression, right: Expression) -> None:
        self.left = left
        self.right = right

    def to_code(self, env: Environment) -> CodeNode:
        raise NotImplementedError('TODO')

class Multiply(ASTNode):
    def __init__(self, left: Expression, right: Expression) -> None:
        self.left = left
        self.right = right

    def to_code(self, env: Environment) -> CodeNode:
        raise NotImplementedError('TODO')

class Divide(ASTNode):
    def __init__(self, left: Expression, right: Expression) -> None:
        self.left = left
        self.right = right

    def to_code(self, env: Environment) -> CodeNode:
        raise NotImplementedError('TODO')

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
        raise NotImplementedError('TODO')

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

class LogicalNot(ASTNode):
    def __init__(self, inner: Expression) -> None:
        self.inner = inner

    def to_code(self, env: Environment) -> CodeNode:
        raise NotImplementedError('TODO')

class Negate(ASTNode):
    def __init__(self, inner: Expression) -> None:
        self.inner = inner

    def to_code(self, env: Environment) -> CodeNode:
        raise NotImplementedError('TODO')

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

        # TODO: finish this

        return code

class Call(ASTNode):
    def __init__(self, name: Expression, arguments: List[Expression]) -> None:
        self.name = name
        self.arguments = arguments

    def to_code(self, env: Environment) -> CodeNode:
        raise NotImplementedError('TODO')

class Constant(ASTNode):
    def __init__(self, type: CConst, value: Any) -> None:
        self.type = type
        self.value = value

    def to_code(self, env: Environment) -> CodeNode:
        code = CodeNode()

        code.type = self.type
        val = self.value

        # TODO: Do we need to convert val to something here?
        code.add(instructions.Ldc(code.type.ptype(), val))

        code.maxStackSpace = 1

        return code

class IdentifierExpression(ASTNode):
    def __init__(self, identifier: Identifier) -> None:
        self.identifier = identifier

    def to_code(self, env: Environment) -> CodeNode:
        code = CodeNode()

        var = env.get_var(self.identifier.name)

        code.add(instructions.Ldo(var.ptype, var.address))
        code.type = var.ctype

        code.maxStackSpace = 1

        return code

    def to_lcode(self, env: Environment) -> CodeNode:
        code = CodeNode()

        var = env.get_var(self.identifier.name)

        code.add(instructions.Lda(0, var.address))

        # TODO: Something about checking whether or not the variable is (at some level) const?
        code.type = var.ctype
        code.maxStackSpace = 1

        return code

# Declarators
Declarator = Any  # of the following:

class DeclaratorASTNode(ASTNode):  # abstract
    def to_var(self, declarationType: CType) -> Tuple[CType, str]:
        '''
        CType (and name) synthesis from declarator 'types' and a given base type:
        int *x, y[]   →   (CPointer(CInt), "x") and (CArray(CInt), "y")
        '''
        raise NotImplementedError()

class IdentifierDeclarator(DeclaratorASTNode):
    def __init__(self, identifier: Identifier) -> None:
        self.identifier = identifier

    def to_code(self, env: Environment) -> CodeNode:
        raise NotImplementedError('TODO')

    def to_var(self, declarationType: CType) -> Tuple[CType, str]:
        return (declarationType, self.identifier.name)


class PointerDeclarator(DeclaratorASTNode):
    def __init__(self, inner: 'Declarator') -> None:
        self.inner = inner

    def to_code(self, env: Environment) -> CodeNode:
        raise NotImplementedError('TODO')

    def to_var(self, declarationType: CType) -> Tuple[CType, str]:
        innerType, name = self.inner.to_var(declarationType)
        return (CPointer(innerType), name)



class ConstantDeclarator(DeclaratorASTNode):
    def __init__(self, inner: 'Declarator') -> None:
        self.inner = inner

    def to_code(self, env: Environment) -> CodeNode:
        raise NotImplementedError('TODO')

    def to_var(self, declarationType: CType) -> Tuple[CType, str]:
        innerType, name = self.inner.to_var(declarationType)
        return (CConst(innerType), name)


class ArrayDeclarator(DeclaratorASTNode):
    def __init__(self, inner: 'Declarator', size: Expression) -> None:
        self.inner = inner
        self.size = size

    def to_code(self, env: Environment) -> CodeNode:
        raise NotImplementedError('TODO')

    def to_var(self, declarationType: CType) -> Tuple[CType, str]:
        innerType, name = self.inner.to_var(declarationType)
        return (CArray(innerType), name)



# Declarations
class InitDeclarator(ASTNode):
    def __init__(self, declarator: Declarator, init: Optional[Expression]) -> None:
        self.declarator = declarator
        self.init = init

    def to_code(self, env: Environment) -> CodeNode:
        raise NotImplementedError('TODO')

class Declaration(ASTNode):
    def __init__(self, type: CType, initDeclarators: List[InitDeclarator]) -> None:
        self.type = type
        self.initDeclarators = initDeclarators

    def to_code(self, env: Environment) -> CodeNode:
        code = CodeNode()

        for decl in self.initDeclarators:
            declarationType, name = decl.declarator.to_var(self.type)
            env.register_variable(name, declarationType)

            if decl.init != None:
                # An initialiser is just an assignment, except it can also assign to const variables...
                # TODO: Initialisation of const variables
                init = Assignment(left=IdentifierExpression(Identifier(name)), right=decl.init)
                c = init.to_code(env)
                code.add(c)

                # max stack space depends entirely on the max. required by any of the init assignments
                code.maxStackSpace = max(code.maxStackSpace, c.maxStackSpace)
            else:
                # TODO: default initialisation?
                pass

        return code

# Statements
Statement = Any  # of the following:
class CondStatement(ASTNode):
    def __init__(self, condition: Expression, trueBody: Statement, falseBody: Optional[Statement]) -> None:
        self.condition = condition
        self.trueBody = trueBody
        self.falseBody = falseBody

    def to_code(self, env: Environment) -> CodeNode:
        raise NotImplementedError('TODO')

class WhileStatement(ASTNode):
    def __init__(self, condition: Expression, body: Statement) -> None:
        self.condition = condition
        self.body = body

    def to_code(self, env: Environment) -> CodeNode:
        raise NotImplementedError('TODO')

class ForStatement(ASTNode):
    def __init__(self, left: Optional[Union[Declaration, Expression]], center: Optional[Expression], right: Optional[Expression], body: Statement) -> None:
        self.left = left
        self.center = center
        self.right = right
        self.body = body

    def to_code(self, env: Environment) -> CodeNode:
        raise NotImplementedError('TODO')

class BreakStatement(ASTNode):
    def __init__(self) -> None:
        pass

    def to_code(self, env: Environment) -> CodeNode:
        raise NotImplementedError('TODO')

class ContinueStatement(ASTNode):
    def __init__(self) -> None:
        pass

    def to_code(self, env: Environment) -> CodeNode:
        raise NotImplementedError('TODO')

class ReturnStatement(ASTNode):
    def __init__(self, expression: Optional[Expression]) -> None:
        self.expression = expression

    def to_code(self, env: Environment) -> CodeNode:
        raise NotImplementedError('TODO')

class ExprStatement(ASTNode):
    def __init__(self, expression: Optional[Expression]) -> None:
        self.expression = expression

    def to_code(self, env: Environment) -> CodeNode:
        code = CodeNode()

        if self.expression is None:
            return code

        c = self.expression.to_code(env)
        code.add(c)

        # discard the top of stack...
        # there is no instruction that simply does SP := SP - 1...
        # ...so just write the top of the stack to 0?
        # TODO: figure out what better to do with the useless top-of-stack in an ExprStmt
        code.add(instructions.Sro(PAddress, 0))

        code.maxStackSpace = c.maxStackSpace

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
    def __init__(self, statements: List[Union[Declaration, Statement]]) -> None:
        self.statements = statements

    def to_code(self, env: Environment) -> CodeNode:
        env.deepen()
        code = blockstmt_to_code(self, env)
        env.undeepen()

        return code

# Top-level stuff
# this is still a bit funky, because the declarator and type go together
class ParameterDeclaration(ASTNode):
    def __init__(self, type: CType, declarator: Declarator) -> None:
        self.type = type
        self.declarator = declarator

    def to_code(self, env: Environment) -> CodeNode:
        raise NotImplementedError('TODO')

    def to_var(self) -> Tuple[CType, str]:
        return self.declarator.to_var(self.type)


class FunctionDefinition(ASTNode):
    def __init__(self, name: str, returnType: CType, parameters: List[ParameterDeclaration], body: CompoundStatement) -> None:
        self.name = name
        self.returnType = returnType
        self.parameters = parameters
        self.body = body

    def to_code(self, env: Environment) -> CodeNode:
        code = CodeNode()

        name = self.name
        code.foundMain = (name == 'main')

        returnType = self.returnType
        # `parameters` is a list of tuples Tuple[CType, str]
        parameters = [p.to_var() for p in self.parameters]
        # `signature` is a list of CTypes
        signature = [p[0] for p in parameters]

        # Calculate the amount of space on the stack the parameters take up
        paramSpace = 0
        for t in signature:
            paramSpace += t.ptype().size()

        label = env.register_function(name, returnType, signature)

        # Append the label pointing to this function
        code.add(label)


        # Deepen the environment into a new scope
        env.deepen()

        # Register all the function arguments to the new scope
        for p in parameters:
            env.register_variable(p[1], p[0])
        # Generate the body's code in the new scope
        bodyc = blockstmt_to_code(self.body, env)

        # Leave the new scope.
        env.undeepen()


        # Before entering the body we must make space
        maxVarSpace = env.symbols.max_var_space()
        code.add(instructions.Ent(bodyc.maxStackSpace, maxVarSpace))
        code.add(bodyc)

        # Add the implicit return in case of a void function
        if returnType == CVoid:
            code.add(instructions.Retp())

        # Safety halt in case execution flow continues past the function boundary...?
        code.add(instructions.Hlt())

        return code

class Program(ASTNode):
    def __init__(self, declarations: List[Union[FunctionDefinition, Declaration]]) -> None:
        self.declarations = declarations

    def to_code(self, env: Environment) -> CodeNode:
        code = CodeNode()

        declarationCode = CodeNode()
        functionCode = CodeNode()

        for child in self.declarations:
            c = child.to_code(env)

            if isinstance(child, Declaration):
                # TODO: global variable space / binding?
                declarationCode.add(c)
            else:
                functionCode.add(c)

            code.foundMain = code.foundMain or c.foundMain

        # the amount of space global variables take up is just the amount of space all vars in level 0 take up
        varSpace = env.symbols.varSpace

        # TODO: Find an instruction that makes space for (uninitialised) variables.
        for i in range(5 + varSpace):
            code.add(instructions.Ldc(PAddress, 0))

        # First: initialise global variables
        code.add(declarationCode)
        # Second: jump to the main function
        # TODO: replace by a function call to main?
        code.add(instructions.Ujp('f_main'))
        # Finally: Big block of function code.
        code.add(functionCode)

        if not code.foundMain:
            raise ValueError('No \'main\' function found.')

        return code
