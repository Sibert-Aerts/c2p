from typing import Any, List, Optional, Union, Tuple, Callable
from ..ctypes import CArray, CConst, CChar, CInt, CFloat, CPointer, CType, CVoid, CBool
from ...codegen.environment import Environment
from ...codegen.code_node import CodeNode
from ...codegen.error import SemanticError
from ...ptypes import PAddress
from ... import instructions
from c2p.source_interval import SourceInterval
from c2p.codegen.error import warn

from .node_base import *
from .node_expression import *

Declarator = Any  # of the following:

class DeclaratorASTNode(ASTNode):  # abstract
    def __init__(self, where: SourceInterval) -> None:
        super().__init__(where)

    def to_var(self, declarationType: CType) -> Tuple[CType, str]:
        '''
        CType (and name) synthesis from declarator 'types' and a given base type:
        int *x, y[]   →   (CPointer(CInt), "x") and (CArray(CInt), "y")
        '''
        raise NotImplementedError()

class IdentifierDeclarator(DeclaratorASTNode):
    def __init__(self, where: SourceInterval, identifier: Identifier) -> None:
        super().__init__(where)
        self.identifier = identifier

    def to_var(self, innerType: CType) -> Tuple[CType, str]:
        return (innerType, self.identifier.name)


class PointerDeclarator(DeclaratorASTNode):
    def __init__(self, where: SourceInterval, inner: 'Declarator') -> None:
        super().__init__(where)
        self.inner = inner

    def to_var(self, innerType: CType) -> Tuple[CType, str]:
        return self.inner.to_var(CPointer(innerType))



class ConstantDeclarator(DeclaratorASTNode):
    def __init__(self, where: SourceInterval, inner: 'Declarator') -> None:
        super().__init__(where)
        self.inner = inner

    def to_var(self, innerType: CType) -> Tuple[CType, str]:
        return self.inner.to_var(CConst(innerType))


class ArrayDeclarator(DeclaratorASTNode):
    def __init__(self, where: SourceInterval, inner: 'Declarator', size: Expression) -> None:
        super().__init__(where)
        self.inner = inner
        self.size = size

    def to_var(self, innerType: CType) -> Tuple[CType, str]:
        return self.inner.to_var(CArray(innerType, self.size))



# Declarations
class InitDeclarator(ASTNode):
    def __init__(self, where: SourceInterval, declarator: Declarator, init: Optional[Expression]) -> None:
        super().__init__(where)
        self.declarator = declarator
        self.init = init

# I pulled this out of the Declaration.to_code function because it's easier that way
# Essentially a simpler version of assignment.
def init_to_code(env : Environment, name : str, init : Expression, where: SourceInterval) -> CodeNode:
    code = CodeNode()

    # Load the variable's address onto the stack
    var = env.get_variable(name, where)
    code.add(instructions.Lda(0, var.address))

    # Evaluate the right expression and put it on the stack
    cinit = init.to_code(env)

    if not cinit.type.promotes_to(var.ctype):
        if cinit.type.demotes_to(var.ctype):
            warn('Possible loss of information in initialisation of {} as {}.'.format(var.ctype, cinit.type), where)
        else:
            raise SemanticError('Incompatible initialisation of {} as {}.'.format(var.ctype, cinit.type), where)
    code.add(cinit, var.ctype)

    # Store the value
    code.add(instructions.Sto(var.ptype))

    code.maxStackSpace = cinit.maxStackSpace + 1

    return code

class Declaration(ASTNode):
    def __init__(self, where: SourceInterval, type: CType, initDeclarators: List[InitDeclarator]) -> None:
        super().__init__(where)
        self.type = type
        self.initDeclarators = initDeclarators

    def to_code(self, env: Environment) -> CodeNode:
        code = CodeNode()

        for decl in self.initDeclarators:
            declType, name = decl.declarator.to_var(self.type)
            env.register_variable(name, declType, self.where)

            init = None
            if decl.init is not None:
                if isinstance(declType.ignoreConst(), CArray):
                    raise SemanticError('Cannot initialise arrays.', self.where)
                init = decl.init
            else:
                # Initialise as zero: init is a Constant
                init = Constant(self.where, CConst(declType), declType.default())

            if not isinstance(declType.ignoreConst(), CArray):
                c = init_to_code(env, name, init, self.where)
                code.add(c)
                # max stack space depends entirely on the max. required by any of the init assignments
                code.maxStackSpace = max(code.maxStackSpace, c.maxStackSpace)

        return code