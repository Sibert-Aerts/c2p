from typing import Any, List, Optional, Union, Tuple, Callable
from ..ctypes import CArray, CConst, CChar, CInt, CFloat, CPointer, CType, CVoid, CBool
from ...codegen.environment import Environment
from ...codegen.code_node import CodeNode
from ...ptypes import PAddress
from ... import instructions

from .node_base import *
from .node_expression import *

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

    def to_var(self, declarationType: CType) -> Tuple[CType, str]:
        return (declarationType, self.identifier.name)


class PointerDeclarator(DeclaratorASTNode):
    def __init__(self, inner: 'Declarator') -> None:
        self.inner = inner

    def to_var(self, declarationType: CType) -> Tuple[CType, str]:
        innerType, name = self.inner.to_var(declarationType)
        return (CPointer(innerType), name)



class ConstantDeclarator(DeclaratorASTNode):
    def __init__(self, inner: 'Declarator') -> None:
        self.inner = inner

    def to_var(self, declarationType: CType) -> Tuple[CType, str]:
        innerType, name = self.inner.to_var(declarationType)
        return (CConst(innerType), name)


class ArrayDeclarator(DeclaratorASTNode):
    def __init__(self, inner: 'Declarator', size: Expression) -> None:
        self.inner = inner
        self.size = size

    def to_var(self, declarationType: CType) -> Tuple[CType, str]:
        innerType, name = self.inner.to_var(declarationType)
        return (CArray(innerType), name)



# Declarations
class InitDeclarator(ASTNode):
    def __init__(self, declarator: Declarator, init: Optional[Expression]) -> None:
        self.declarator = declarator
        self.init = init

# I pulled this out of the Declaration.to_code function because it's easier that way
# Essentially a simpler version of assignment.
def init_to_code(env : Environment, name : str, decl : InitDeclarator) -> CodeNode:
    code = CodeNode()

    # Load the variable's address onto the stack
    var = env.get_variable(name)
    code.add(instructions.Lda(0, var.address))

    # Evaluate the right expression and put it on the stack
    cinit = decl.init.to_code(env)
    code.add(cinit)

    # TODO: type compatibility & implicit casting logic!
    if(var.ctype.ignoreConst() != cinit.type.ignoreConst()):
        raise ValueError('Incompatible initialisation of {} as {}.'.format(var.ctype, cinit.type))

    # Store the value
    code.add(instructions.Sto(var.ptype))

    code.maxStackSpace = cinit.maxStackSpace + 1

    return code

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
                c = init_to_code(env, name, decl)
                code.add(c)

                # max stack space depends entirely on the max. required by any of the init assignments
                code.maxStackSpace = max(code.maxStackSpace, c.maxStackSpace)
            else:
                # TODO: default initialisation?
                pass

        return code