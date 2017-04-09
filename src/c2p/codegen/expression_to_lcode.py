from .environment import *
from .code_node import CodeNode
from c2p.grammar import *
from c2p import instructions
from c2p.grammar.ast.node_methods import *

# All expressions incapable of producing L-Values use this for their to_lcode method
def invalid_to_lcode(self, env : Environment) -> CodeNode:
    raise ValueError('{} is not a valid L-Value expression'.format(self.__class__.__name__))

# All of these expressions are invalid as an L-Value
Assignment.to_lcode = invalid_to_lcode
AddAssignment.to_lcode = invalid_to_lcode
SubAssignment.to_lcode = invalid_to_lcode
MulAssignment.to_lcode = invalid_to_lcode
DivAssignment.to_lcode = invalid_to_lcode
TernaryIf.to_lcode = invalid_to_lcode
LogicalOr.to_lcode = invalid_to_lcode
LogicalAnd.to_lcode = invalid_to_lcode
Equals.to_lcode = invalid_to_lcode
NotEquals.to_lcode = invalid_to_lcode
LessThan.to_lcode = invalid_to_lcode
GreaterThan.to_lcode = invalid_to_lcode
LessThanEquals.to_lcode = invalid_to_lcode
GreaterThanEquals.to_lcode = invalid_to_lcode
Add.to_lcode = invalid_to_lcode
Subtract.to_lcode = invalid_to_lcode
Multiply.to_lcode = invalid_to_lcode
Divide.to_lcode = invalid_to_lcode
Cast.to_lcode = invalid_to_lcode
PrefixIncrement.to_lcode = invalid_to_lcode
PostfixIncrement.to_lcode = invalid_to_lcode
PrefixDecrement.to_lcode = invalid_to_lcode
PostfixDecrement.to_lcode = invalid_to_lcode
AddressOf.to_lcode = invalid_to_lcode
LogicalNot.to_lcode = invalid_to_lcode
Negate.to_lcode = invalid_to_lcode
Call.to_lcode = invalid_to_lcode
Constant.to_lcode = invalid_to_lcode

# The only valid L-Value expressions are:

def comma_to_lcode(self, env : Environment) -> CodeNode:
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

Comma.to_lcode = comma_to_lcode

def deref_to_lcode(self, env : Environment) -> CodeNode:
    code = CodeNode()

    c = self.inner.to_code(env)
    code.add(c)

    # make sure the inner code is of type pointer
    if isinstance(t, CPointer):
        print('we dereferencin a pointer ova here!')
        # the type of this expression is the type that's being pointed at
        code.type = c.type.t
    else:
        raise ValueError('Expression of type {} cannot be dereferenced into an L-Value.'.format(c.type))

    # We don't need to add any instructions, because of how assignment instructions work.
    code.maxStackSpace = c.maxStackSpace

    return code


Dereference.to_lcode = deref_to_lcode

def index_to_lcode(self, env : Environment) -> CodeNode:
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

Index.to_lcode = index_to_lcode

def ident_to_lcode(self, env : Environment) -> CodeNode:
    code = CodeNode()

    var = env.get_var(self.identifier.name)
    
    code.add(instructions.Lda(0, var.address))

    # TODO: Something about checking whether or not the variable is (at some level) const?
    code.type = var.ctype
    code.maxStackSpace = 1

    return code

IdentifierExpression.to_lcode = ident_to_lcode