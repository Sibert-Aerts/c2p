from .environment import *
from c2p.grammar import *
from c2p.grammar.ast.node_methods import *

def make_code(AST):
    env = Environment()
    code = AST.to_code(env)
    return code

def program_to_code(self, env : Environment) -> List:
    code = []
    code.append('start:')
    for child in self.declarations:
        code += child.to_code(env)
    code.append('end:')
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

def assignment_to_code(self, env : Environment) -> List:
    code = []
    # figure this out lol
    raise NotImplementedError()
    return code

Assignment.to_code = assignment_to_code