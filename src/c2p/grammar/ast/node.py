from typing import Any, List, NamedTuple, Optional, Union
from ..ctypes import CType, CConst
# from ..ptypes import PType, PAddress, PBoolean, PCharacter, PInteger, PReal

### AST nodes
Identifier = NamedTuple('Identifier', [('name', str)])

# Expressions
Expression = Any  # of the following:
Comma = NamedTuple('Comma', [('left', Expression), ('right', Expression)])
Assignment = NamedTuple('Assignment', [('left', Expression), ('right', Expression)])
AddAssignment = NamedTuple('Assignment', [('left', Expression), ('right', Expression)])
SubAssignment = NamedTuple('Assignment', [('left', Expression), ('right', Expression)])
MulAssignment = NamedTuple('Assignment', [('left', Expression), ('right', Expression)])
DivAssignment = NamedTuple('Assignment', [('left', Expression), ('right', Expression)])
TernaryIf = NamedTuple('TernaryIf', [('left', Expression), ('right', Expression)])
LogicalOr = NamedTuple('LogicalOr', [('left', Expression), ('right', Expression)])
LogicalAnd = NamedTuple('LogicalAnd', [('left', Expression), ('right', Expression)])
Equals = NamedTuple('Equals', [('left', Expression), ('right', Expression)])
NotEquals = NamedTuple('NotEquals', [('left', Expression), ('right', Expression)])
LessThan = NamedTuple('LessThan', [('left', Expression), ('right', Expression)])
GreaterThan = NamedTuple('GreaterThan', [('left', Expression), ('right', Expression)])
LessThanEquals = NamedTuple('LessThanEquals', [('left', Expression), ('right', Expression)])
GreaterThanEquals = NamedTuple('GreaterThanEquals', [('left', Expression), ('right', Expression)])
Add = NamedTuple('Add', [('left', Expression), ('right', Expression)])
Subtract = NamedTuple('Subtract', [('left', Expression), ('right', Expression)])
Multiply = NamedTuple('Multiply', [('left', Expression), ('right', Expression)])
Divide = NamedTuple('Divide', [('left', Expression), ('right', Expression)])
Cast = NamedTuple('Cast', [('type', CType), ('right', Expression)])
PrefixIncrement = NamedTuple('PrefixIncrement', [('inner', Expression)])
PostfixIncrement = NamedTuple('PostfixIncrement', [('inner', Expression)])
PrefixDecrement = NamedTuple('PrefixDecrement', [('inner', Expression)])
PostfixDecrement = NamedTuple('PostfixDecrement', [('inner', Expression)])
AddressOf = NamedTuple('AddressOf', [('inner', Expression)])
Dereference = NamedTuple('Dereference', [('inner', Expression)])
LogicalNot = NamedTuple('LogicalNot', [('inner', Expression)])
Negate = NamedTuple('Negate', [('inner', Expression)])
Index = NamedTuple('Index', [('array', Expression), ('index', Expression)])
Call = NamedTuple('Call', [('name', Expression), ('arguments', List[Expression])])
Constant = NamedTuple('Constant', [('type', CConst), ('value', Any)])
IdentifierExpression = NamedTuple('IdentifierExpression', [('identifier', Identifier)])

# Declarators
Declarator = Any  # of the following:
IdentifierDeclarator = NamedTuple('IdentifierDeclarator', [('identifier', Identifier)])
PointerDeclarator = NamedTuple('PointerDeclarator', [('inner', 'Declarator')])
ConstantDeclarator = NamedTuple('ConstantDeclarator', [('inner', 'Declarator')])
ArrayDeclarator = NamedTuple('ArrayDeclarator', [('inner', 'Declarator'), ('size', Expression)])

# Declarations
InitDeclarator = NamedTuple('InitDeclarator', [
    ('declarator', Declarator),
    ('init', Optional[Expression]),
])

Declaration = NamedTuple('Declaration', [
    ('type', CType),
    ('initDeclarators', List[InitDeclarator]),
])

# Statements
Statement = Any  # of the following:
CondStatement = NamedTuple('CondStatement', [
    ('condition', Expression),
    ('trueBody', Statement),
    ('falseBody', Optional[Statement]),
])
WhileStatement = NamedTuple('WhileStatement', [
    ('condition', Expression),
    ('body', Statement),
])
ForStatement = NamedTuple('ForStatement', [
    ('left', Optional[Union[Declaration, Expression]]),
    ('center', Optional[Expression]),
    ('right', Optional[Expression]),
    ('body', Statement),
])
BreakStatement = NamedTuple('BreakStatement', [])
ContinueStatement = NamedTuple('ContinueStatement', [])
ReturnStatement = NamedTuple('ReturnStatement', [('expression', Expression)])
ExprStatement = NamedTuple('ExprStatement', [('expression', Optional[Expression])])
CompoundStatement = NamedTuple('CompoundStatement', [
    ('statements', List[Union[Declaration, Statement]])
])

# Top-level stuff
# this is still a bit funky, because the declarator and type go together
ParameterDeclaration = NamedTuple('ParameterDeclaration', [
    ('type', CType),
    ('declarator', Declarator),
])

FunctionDefinition = NamedTuple('FunctionDefinition', [
    ('name', str),
    ('returnType', CType),
    ('parameters', List[ParameterDeclaration]),
    ('body', CompoundStatement),
])

Program = NamedTuple('Program', [
    ('declarations', List[Union[FunctionDefinition, Declaration]]),
])
