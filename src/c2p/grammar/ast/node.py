from typing import Any, List, Optional, Union, Tuple, Callable
from ..ctypes import CArray, CConst, CChar, CInt, CPointer, CType, CVoid, CBool
from ...codegen.environment import Environment, FunctionRecord
from ...codegen.code_node import CodeNode
from ...ptypes import PAddress
from ... import instructions
from c2p.source_interval import SourceInterval
# from ..ptypes import PType, PAddress, PBoolean, PCharacter, PInteger, PReal

# Code is split up over these files:
from .node_base import *
from .node_expression import *
from .node_decl import *
from .node_statement import *

# this is still a bit funky, because the declarator and type go together
class ParameterDeclaration(ASTNode):
    def __init__(self, where: SourceInterval, type: CType, declarator: Declarator) -> None:
        super().__init__(where)
        self.type = type
        self.declarator = declarator

    def to_code(self, env: Environment) -> CodeNode:
        raise NotImplementedError('TODO')

    def to_var(self) -> Tuple[CType, str]:
        return self.declarator.to_var(self.type)


class FunctionDeclaration(ASTNode):
    def __init__(self, where: SourceInterval, name: str, returnType: CType, parameters: List[ParameterDeclaration]) -> None:
        super().__init__(where)
        self.name = name
        self.returnType = returnType
        self.parameters = parameters

    def to_code(self, env: Environment) -> CodeNode:
        # `signature` is a list of CTypes
        signature = [p.to_var()[0] for p in self.parameters]
        env.declare_function(self.name, self.returnType, signature, self.where)
        return CodeNode()


class FunctionDefinition(ASTNode):
    def __init__(self, where: SourceInterval, name: str, returnType: CType, parameters: List[ParameterDeclaration], body: CompoundStatement) -> None:
        super().__init__(where)
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

        label = env.declare_function(name, returnType, signature, self.where, isDefinition=True).label

        # Append the label pointing to this function
        code.add(label)


        # Deepen the environment into a new scope, and tell the returnType
        env.deepen()
        env.returnType = returnType

        # Register all the function arguments to the new scope
        for p in parameters:
            env.register_variable(p[1], p[0], self.where)

        # Generate the body's code in the new scope
        bodyc = blockstmt_to_code(self.body, env)

        # Get the amount of space the variables take up (needs to happen before leaving scope)
        maxVarSpace = env.scope.maxVarSpace

        # Leave the new scope, remove the returnType
        env.undeepen()
        env.returnType = None

        # maxVarSpace + 5 because we need to keep the frame header in mind
        code.add(instructions.Ent(bodyc.maxStackSpace, maxVarSpace + 5))
        code.add(bodyc)

        # Add the implicit return in case of a void function
        if returnType == CVoid():
            code.add(instructions.Retp())

        # Safety halt in case execution flow continues past the function boundary...?
        code.add(instructions.Hlt())

        return code

class Program(ASTNode):
    def __init__(self, where: SourceInterval, declarations: List[Union[FunctionDefinition, Declaration]]) -> None:
        super().__init__(where)
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

        for k, v in env.scope.symbols.items():
            if isinstance(v, FunctionRecord) and not v.defined:
                raise self.semanticError('%s was declared but not defined.' % k)
        # the amount of space global variables take up is just the amount of space all vars in level 0 take up
        varSpace = env.scope.varSpace
        # make space for the global variables + frame header (5) + files! (4)
        varSpace += 5 + 4
        code.add(instructions.Ent(varSpace, varSpace))

        # First: initialise global variables
        code.add(env.string_literal_code())
        code.add(declarationCode)
        # Second: call the main function
        code.add(instructions.Mst(0))
        code.add(instructions.Cup(0, 'f_main'))
        code.add(instructions.Hlt())

        # Finally: Big block of function code.
        code.add(functionCode)

        if not code.foundMain:
            raise self.semanticError('No \'main\' function found.')

        return code
