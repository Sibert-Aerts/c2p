from typing import Any, List, NamedTuple, Optional, Union
from .ctypes import CType
from .antlr.SmallCVisitor import SmallCVisitor  # type: ignore
from .antlr.SmallCParser import SmallCParser  # type: ignore
# from ..ptypes import PType, PAddress, PBoolean, PCharacter, PInteger, PReal

### AST nodes
Identifier = NamedTuple('Identifier', [('name', str)])

# Expressions
Expression = Any  # of the following:
Comma = NamedTuple('Comma', [('left', Expression), ('right', Expression)])
Assignment = NamedTuple('Assignment', [('left', Expression), ('right', Expression)])
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
Cast = NamedTuple('Cast', [('left', Expression), ('right', Expression)])
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
Constant = NamedTuple('Constant', [('value', Any)])
IdentifierExpression = NamedTuple('IdentifierExpression', [('identifier', Identifier)])

# Declarators
Declarator = Any  # of the following:
IdentifierDeclarator = NamedTuple('IdentifierDeclarator', [('identifier', Identifier)])
PointerDeclarator = NamedTuple('PointerDeclarator', [('inner', 'Declarator')])
ArrayDeclarator = NamedTuple('ArrayDeclarator', [('inner', 'Declarator'), ('size', Expression)])

# Declarations
InitDeclarator = NamedTuple('InitDeclarator', [
    ('declarator', Declarator),
    ('init', Optional[Expression]),
])

Declaration = NamedTuple('Declaration', [
    ('specifiers', List[str]),
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
ParameterDeclaration = NamedTuple('ParameterDeclaration', [
    ('specifiers', List[str]),
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


# TODO
class ASTVisitor(SmallCVisitor):

    # Visit a parse tree produced by SmallCParser#program.
    def visitProgram(self, ctx:SmallCParser.ProgramContext):
        raise NotImplementedError()


    # Visit a parse tree produced by SmallCParser#includeStdio.
    def visitIncludeStdio(self, ctx:SmallCParser.IncludeStdioContext):
        raise NotImplementedError()


    # Visit a parse tree produced by SmallCParser#externalDeclaration.
    def visitExternalDeclaration(self, ctx:SmallCParser.ExternalDeclarationContext):
        raise NotImplementedError()


    # Visit a parse tree produced by SmallCParser#functionDefinition.
    def visitFunctionDefinition(self, ctx:SmallCParser.FunctionDefinitionContext):
        raise NotImplementedError()


    # Visit a parse tree produced by SmallCParser#parameterDeclarationList.
    def visitParameterDeclarationList(self, ctx:SmallCParser.ParameterDeclarationListContext):
        raise NotImplementedError()


    # Visit a parse tree produced by SmallCParser#parameterDeclaration.
    def visitParameterDeclaration(self, ctx:SmallCParser.ParameterDeclarationContext):
        raise NotImplementedError()


    # Visit a parse tree produced by SmallCParser#compoundStatement.
    def visitCompoundStatement(self, ctx:SmallCParser.CompoundStatementContext):
        raise NotImplementedError()


    # Visit a parse tree produced by SmallCParser#statement.
    def visitStatement(self, ctx:SmallCParser.StatementContext):
        raise NotImplementedError()


    # Visit a parse tree produced by SmallCParser#condStatement.
    def visitCondStatement(self, ctx:SmallCParser.CondStatementContext):
        raise NotImplementedError()


    # Visit a parse tree produced by SmallCParser#whileStatement.
    def visitWhileStatement(self, ctx:SmallCParser.WhileStatementContext):
        raise NotImplementedError()


    # Visit a parse tree produced by SmallCParser#forStatement.
    def visitForStatement(self, ctx:SmallCParser.ForStatementContext):
        raise NotImplementedError()


    # Visit a parse tree produced by SmallCParser#breakStatement.
    def visitBreakStatement(self, ctx:SmallCParser.BreakStatementContext):
        raise NotImplementedError()


    # Visit a parse tree produced by SmallCParser#continueStatement.
    def visitContinueStatement(self, ctx:SmallCParser.ContinueStatementContext):
        raise NotImplementedError()


    # Visit a parse tree produced by SmallCParser#returnStatement.
    def visitReturnStatement(self, ctx:SmallCParser.ReturnStatementContext):
        raise NotImplementedError()


    # Visit a parse tree produced by SmallCParser#exprStatement.
    def visitExprStatement(self, ctx:SmallCParser.ExprStatementContext):
        raise NotImplementedError()


    # Visit a parse tree produced by SmallCParser#declaration.
    def visitDeclaration(self, ctx:SmallCParser.DeclarationContext):
        raise NotImplementedError()


    # Visit a parse tree produced by SmallCParser#declarationSpecifiers.
    def visitDeclarationSpecifiers(self, ctx:SmallCParser.DeclarationSpecifiersContext):
        raise NotImplementedError()


    # Visit a parse tree produced by SmallCParser#initDeclaratorList.
    def visitInitDeclaratorList(self, ctx:SmallCParser.InitDeclaratorListContext):
        raise NotImplementedError()


    # Visit a parse tree produced by SmallCParser#initDeclarator.
    def visitInitDeclarator(self, ctx:SmallCParser.InitDeclaratorContext):
        raise NotImplementedError()


    # Visit a parse tree produced by SmallCParser#declarator.
    def visitDeclarator(self, ctx:SmallCParser.DeclaratorContext):
        raise NotImplementedError()


    # Visit a parse tree produced by SmallCParser#directDeclarator.
    def visitDirectDeclarator(self, ctx:SmallCParser.DirectDeclaratorContext):
        raise NotImplementedError()


    # Visit a parse tree produced by SmallCParser#pointer.
    def visitPointer(self, ctx:SmallCParser.PointerContext):
        raise NotImplementedError()


    # Visit a parse tree produced by SmallCParser#typeSpecifier.
    def visitTypeSpecifier(self, ctx:SmallCParser.TypeSpecifierContext):
        raise NotImplementedError()


    # Visit a parse tree produced by SmallCParser#typeQualifier.
    def visitTypeQualifier(self, ctx:SmallCParser.TypeQualifierContext):
        raise NotImplementedError()


    # Visit a parse tree produced by SmallCParser#expression.
    def visitExpression(self, ctx:SmallCParser.ExpressionContext):
        raise NotImplementedError()


    # Visit a parse tree produced by SmallCParser#assignment.
    def visitAssignment(self, ctx:SmallCParser.AssignmentContext):
        raise NotImplementedError()


    # Visit a parse tree produced by SmallCParser#condition.
    def visitCondition(self, ctx:SmallCParser.ConditionContext):
        raise NotImplementedError()


    # Visit a parse tree produced by SmallCParser#disjunction.
    def visitDisjunction(self, ctx:SmallCParser.DisjunctionContext):
        raise NotImplementedError()


    # Visit a parse tree produced by SmallCParser#conjunction.
    def visitConjunction(self, ctx:SmallCParser.ConjunctionContext):
        raise NotImplementedError()


    # Visit a parse tree produced by SmallCParser#comparison.
    def visitComparison(self, ctx:SmallCParser.ComparisonContext):
        raise NotImplementedError()


    # Visit a parse tree produced by SmallCParser#relation.
    def visitRelation(self, ctx:SmallCParser.RelationContext):
        raise NotImplementedError()


    # Visit a parse tree produced by SmallCParser#plus.
    def visitPlus(self, ctx:SmallCParser.PlusContext):
        raise NotImplementedError()


    # Visit a parse tree produced by SmallCParser#times.
    def visitTimes(self, ctx:SmallCParser.TimesContext):
        raise NotImplementedError()


    # Visit a parse tree produced by SmallCParser#cast.
    def visitCast(self, ctx:SmallCParser.CastContext):
        raise NotImplementedError()


    # Visit a parse tree produced by SmallCParser#unary.
    def visitUnary(self, ctx:SmallCParser.UnaryContext):
        raise NotImplementedError()


    # Visit a parse tree produced by SmallCParser#postfix.
    def visitPostfix(self, ctx:SmallCParser.PostfixContext):
        raise NotImplementedError()


    # Visit a parse tree produced by SmallCParser#primary.
    def visitPrimary(self, ctx:SmallCParser.PrimaryContext):
        raise NotImplementedError()


    # Visit a parse tree produced by SmallCParser#constant.
    def visitConstant(self, ctx:SmallCParser.ConstantContext):
        raise NotImplementedError()


    # Visit a parse tree produced by SmallCParser#assignmentOperator.
    def visitAssignmentOperator(self, ctx:SmallCParser.AssignmentOperatorContext):
        raise NotImplementedError()


    # Visit a parse tree produced by SmallCParser#expressionList.
    def visitExpressionList(self, ctx:SmallCParser.ExpressionListContext):
        raise NotImplementedError()
