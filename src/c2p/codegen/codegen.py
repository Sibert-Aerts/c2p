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

    for child in self.declarations:
        c = child.to_code(env)
        code.add(c)
        code.maxVarSpace += c.maxVarSpace

    return code

Program.to_code = program_to_code

def declaration_to_code(self, env : Environment) -> CodeNode:
    code = CodeNode()

    for decl in self.initDeclarators:
        declType, name = decl.declarator.to_ctype(self.type)
        env.register_variable(name, declType)
        # Increase the size of the variable space
        code.maxVarSpace += declType.ptype().size()
        
        if decl.init != None:
            # An initialiser is just an assignment
            node = Assignment(left=IdentifierExpression(Identifier(name)), right=decl.init)
            c = node.to_code(env)
            code.add(c)

            # max stack space depends entirely on the max. required by any of the init assignments
            code.maxStackSpace = max(code.maxStackSpace, c.maxStackSpace)
        else:
            # default initialisers?
            pass

    return code

Declaration.to_code = declaration_to_code

def funcdef_to_code(self, env : Environment) -> CodeNode:
    code = CodeNode()

    name = self.name
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


    # Make a deeper instance of the current environment
    bodyEnv = env.deepen()
    # Register the function arguments as variables
    for p in parameters:
        bodyEnv.register_variable(p[1], p[0])
    # Use it to generate the body's code
    bodyc = self.body.to_code(bodyEnv)


    # Before entering the body we must make space
    code.add(instructions.Ent(bodyc.maxStackSpace, bodyc.maxVarSpace + paramSpace))
    code.add(bodyc)

    # Add the implicit return in case of a void function
    if returnType == CVoid:
        code.add(instructions.Retp())

    # Safety halt in case execution flow continues past the function boundary...?
    code.add(instructions.Hlt())

    return code

FunctionDefinition.to_code = funcdef_to_code

def comp_to_code(self, env : Environment) -> CodeNode:
    code = CodeNode()

    declCount = 0
    for stmt in self.statements:
        c = stmt.to_code(env)
        code.add(c)

        # max stack space is the max space any statement uses.
        code.maxStackSpace = max(code.maxStackSpace, c.maxStackSpace)

        # Special case regarding maxVarSpace for compound statements.
        if isinstance(stmt, CompoundStatement):
            code.maxVarSpace = max(code.maxVarSpace, declCount + c.maxVarSpace)
        else:
            declCount += c.maxVarSpace

    code.maxVarSpace = max(code.maxVarSpace, declCount)
    print('maxVarSpace =', code.maxVarSpace)

    return code

CompoundStatement.to_code = comp_to_code

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