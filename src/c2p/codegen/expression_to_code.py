from .environment import *
from c2p.grammar import *
from c2p import instructions
from c2p.grammar.ast.node_methods import *

'''
List of unimplemented expressions:

AddAssignment
SubAssignment
MulAssignment
DivAssignment
TernaryIf
LogicalOr
LogicalAnd
Equals
NotEquals
LessThan
GreaterThan
LessThanEquals
GreaterThanEquals
Add
Subtract
Multiply
Divide
Cast
PrefixIncrement
PostfixIncrement
PrefixDecrement
PostfixDecrement
AddressOf
Dereference
LogicalNot
Negate
Index
Call
'''

'''
def expr_to_code(self, env : Environment) -> (List, CType):
    code = []
    
    return (code, t)

Expression.to_code = expr_to_code
'''


def comma_to_code(self, env : Environment) -> (List, CType):
    code = []
    
    # Just treat the left hand side as an individual expression and move on.
    c, _ = ExprStatement(self.left).to_code(env)
    code += c
    c, t = self.right.to_code(env)
    code += c

    return (code, t)

Comma.to_code = comma_to_code


def assignment_to_code(self, env : Environment) -> (List, CType):
    code = []
    
    # Load the left hand side as an L-Value, right hand side as an R-Value, and write R to L
    c, tl = self.left.to_lcode(env)
    code += c
    c, tr = self.right.to_code(env)
    code += c


    if(tl != tr.ignoreConst()):
        raise ValueError('Incompatible assignment of {} to {}.'.format(tr, tl))

    code.append(instructions.Sto(tl.ptype()))

    return (code, tl)

Assignment.to_code = assignment_to_code



def const_to_code(self, env : Environment) -> (List, CType):
    code = []

    t = self.type
    val = self.value
    
    # TODO: Do we need to convert val to something here?
    code.append(instructions.Ldc(t.ptype(), val))

    return (code, t)

Constant.to_code = const_to_code

def ident_to_code(self, env : Environment) -> (List, CType):
    code = []

    var = env.get_var(self.identifier.name)

    # TODO: stored address needs to be relative from (stack ptr + # protected spots)
    # so replace this dumb Ldo with a smarter LoadVariable(name, env) or something
    # once we figure out how stack frames look like
    code.append(instructions.Ldo(var.ptype, var.address))

    return (code, var.ptype)

IdentifierExpression.to_code = ident_to_code