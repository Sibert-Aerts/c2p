from .environment import *
from c2p.grammar import *
from c2p.instructions import *
from c2p.grammar.ast.node_methods import *

# All expressions incapable of producing L-Values use this for their to_lcode method
def invalid_to_lcode(self, env : Environment) -> List:
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

def comma_to_lcode(self, env : Environment) -> (List, CType):
    code = []
    
    # the left hand side of a comma expression is basically just an independent statement right?
    c, _ = ExprStatement(self.left).to_code(env)
    code += c
    # Notice that this will cause an error unless the right instance is a valid L-value expression
    (c, t) = self.right.to_lcode(env)
    code += c

    return  (code, t)

Comma.to_lcode = comma_to_lcode

def deref_to_lcode(self, env : Environment) -> (List, CType):
    code = []

    # make sure the inner code is of type pointer
    c, t = self.inner.to_code(env)
    code += c
    if isinstance(t, CPointer):
        print('we dereferencin a pointer ova here!!!!!!')
        # the type of this expression is the type that's being pointed at
        t = t.t
    else:
        raise ValueError('Expression of type {} cannot be dereferenced into an L-Value.'.format(t))

    return (code, t)


Dereference.to_lcode = deref_to_lcode

def index_to_lcode(self, env : Environment) -> (List, CType):
    code = []
    
    c, t = self.array.to_code(env)
    code += c
    if isinstance(t, (CPointer, CArray)):
        print('we indexin an array ova here!!!!!')
        t = t.t
    else:
        raise ValueError('Expression of type {} cannot be indexed into an L-Value.'.format(t))

    c, it = self.index.to_code(env)
    if it.ignoreConst() == CInt():
        # implement indexing logic
        raise NotImplementedError()
    else:
        raise ValueError('Cannot use type {} as array index.'.format(it))

    return (code, t)

Index.to_lcode = index_to_lcode

def ident_to_lcode(self, env : Environment) -> (List, CType):
    code = []

    var = env.get_var(self.identifier.name)
    
    # TODO: stored address needs to be relative from (stack ptr + # protected spots)
    # so replace this dumb Ldo with a smarter LoadVariable(name, env) or something
    # once we figure out how calls will happen
    code.append(Ldo(var.ptype, var.address))
    
    return (code, var.ctype)

IdentifierExpression.to_lcode = ident_to_lcode