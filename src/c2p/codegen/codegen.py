from .environment import *
from .expression_to_lcode import *
from .expression_to_code import *
from c2p.grammar import *
from c2p import instructions
from c2p.grammar.ast.node_methods import *

def make_code(AST):
    env = Environment()
    code = AST.to_code(env)
    return code

def program_to_code(self, env : Environment) -> List:
    code = []
    for child in self.declarations:
        c, _ = child.to_code(env)
        code += c
    return code

Program.to_code = program_to_code

def declaration_to_code(self, env : Environment) -> List:
    code = []

    baseType = self.type

    for decl in self.initDeclarators:
        declType, name = decl.declarator.to_ctype(baseType)
        env.register_variable(name, declType)
        
        if decl.init != None:
            node = Assignment(left=IdentifierExpression(Identifier(name)), right=decl.init)
            code += node.to_code(env)

    print('env as seen after this decl:', env.variables)
    return code

Declaration.to_code = declaration_to_code

def funcdef_to_code(self, env : Environment) -> List:
    code = []

    name = self.name
    returnType = self.returnType
    parameters = [p.to_ctype() for p in self.parameters]
    signature = [p[0] for p in parameters]

    label = env.register_function(name, returnType, signature)
    
    # Append the label pointing to this function
    code.append(label)

    

    # haha, lol
    raise NotImplementedError()
    return code

FunctionDefinition.to_code = funcdef_to_code