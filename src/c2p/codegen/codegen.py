from .environment import *
from .code_node import CodeNode
from .expression_to_lcode import *
from .expression_to_code import *
from c2p.grammar import *
from c2p import instructions
from c2p.grammar.ast.node_methods import *

def make_code(AST):
    env = Environment()
    code = AST.to_code(env)
    return code.code

def program_to_code(self, env : Environment) -> CodeNode:
    code = CodeNode()

    declCode = CodeNode()
    methCode = CodeNode()

    for child in self.declarations:
        c = child.to_code(env)

        if isinstance(child, Declaration):
            # TODO: global variable space / binding?
            declCode.add(c)
        else:
            methCode.add(c)
        
        code.foundMain = code.foundMain or c.foundMain

    # the amount of space global variables take up is just the amount of space all vars in level 0 take up
    varSpace = env.symbols.varSpace

    # TODO: Find an instruction that makes space for (uninitialised) variables.
    for i in range(5 + varSpace):
        code.add(instructions.Ldc(PAddress, 0))

    # First: initialise global variables
    code.add(declCode)
    # Second: jump to the main function
    # TODO: replace by a function call to main?
    code.add(instructions.Ujp('f_main'))
    # Finally: Big block of method code.
    code.add(methCode)

    if not code.foundMain:
        raise ValueError('No \'main\' method found.')

    return code

Program.to_code = program_to_code

def declaration_to_code(self, env : Environment) -> CodeNode:
    code = CodeNode()

    for decl in self.initDeclarators:
        declType, name = decl.declarator.to_ctype(self.type)
        env.register_variable(name, declType)
        
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

Declaration.to_code = declaration_to_code

def funcdef_to_code(self, env : Environment) -> CodeNode:
    code = CodeNode()

    name = self.name
    code.foundMain = (name == 'main')

    returnType = self.returnType
    # `parameters` is a list of tuples (CType, str)
    parameters = [p.to_ctype() for p in self.parameters]
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

FunctionDefinition.to_code = funcdef_to_code

def blockstmt_to_code(compStmt : CompoundStatement, env : Environment) -> CodeNode:
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

def compstmt_to_code(self, env : Environment) -> CodeNode:
    env.deepen()
    code = blockstmt_to_code(self, env)
    env.undeepen()

    return code

CompoundStatement.to_code = compstmt_to_code

def exprstmt_to_code(self, env : Environment) -> CodeNode:
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

ExprStatement.to_code = exprstmt_to_code