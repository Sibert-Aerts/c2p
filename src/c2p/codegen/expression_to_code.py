from .environment import *
from .code_node import CodeNode
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


def comma_to_code(self, env : Environment) -> CodeNode:
    code = CodeNode()
    
    # Just treat the left hand side as an individual expression and move on.
    cl = ExprStatement(self.left).to_code(env)
    code.add(cl)
    cr = self.right.to_code(env)
    code.add(cr)
    code.type = cr.type

    code.maxStackSpace = max(cl.maxStackSpace, cr.maxStackSpace)

    return code

Comma.to_code = comma_to_code


def assignment_to_code(self, env : Environment) -> CodeNode:
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

Assignment.to_code = assignment_to_code



def const_to_code(self, env : Environment) -> CodeNode:
    code = CodeNode()

    code.type = self.type
    val = self.value
    
    # TODO: Do we need to convert val to something here?
    code.add(instructions.Ldc(code.type.ptype(), val))

    code.maxStackSpace = 1

    return code

Constant.to_code = const_to_code

def ident_to_code(self, env : Environment) -> CodeNode:
    code = CodeNode()

    var = env.get_var(self.identifier.name)

    code.add(instructions.Ldo(var.ptype, var.address))
    code.type = var.ctype

    code.maxStackSpace = 1

    return code

IdentifierExpression.to_code = ident_to_code