# Generated from SmallC.g4 by ANTLR 4.6
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .SmallCParser import SmallCParser
else:
    from SmallCParser import SmallCParser

# This class defines a complete listener for a parse tree produced by SmallCParser.
class SmallCListener(ParseTreeListener):

    # Enter a parse tree produced by SmallCParser#program.
    def enterProgram(self, ctx:SmallCParser.ProgramContext):
        pass

    # Exit a parse tree produced by SmallCParser#program.
    def exitProgram(self, ctx:SmallCParser.ProgramContext):
        pass


    # Enter a parse tree produced by SmallCParser#functionDefinition.
    def enterFunctionDefinition(self, ctx:SmallCParser.FunctionDefinitionContext):
        pass

    # Exit a parse tree produced by SmallCParser#functionDefinition.
    def exitFunctionDefinition(self, ctx:SmallCParser.FunctionDefinitionContext):
        pass


    # Enter a parse tree produced by SmallCParser#parameterDeclarationList.
    def enterParameterDeclarationList(self, ctx:SmallCParser.ParameterDeclarationListContext):
        pass

    # Exit a parse tree produced by SmallCParser#parameterDeclarationList.
    def exitParameterDeclarationList(self, ctx:SmallCParser.ParameterDeclarationListContext):
        pass


    # Enter a parse tree produced by SmallCParser#parameterDeclaration.
    def enterParameterDeclaration(self, ctx:SmallCParser.ParameterDeclarationContext):
        pass

    # Exit a parse tree produced by SmallCParser#parameterDeclaration.
    def exitParameterDeclaration(self, ctx:SmallCParser.ParameterDeclarationContext):
        pass


    # Enter a parse tree produced by SmallCParser#compoundStatement.
    def enterCompoundStatement(self, ctx:SmallCParser.CompoundStatementContext):
        pass

    # Exit a parse tree produced by SmallCParser#compoundStatement.
    def exitCompoundStatement(self, ctx:SmallCParser.CompoundStatementContext):
        pass


    # Enter a parse tree produced by SmallCParser#statement.
    def enterStatement(self, ctx:SmallCParser.StatementContext):
        pass

    # Exit a parse tree produced by SmallCParser#statement.
    def exitStatement(self, ctx:SmallCParser.StatementContext):
        pass


    # Enter a parse tree produced by SmallCParser#condStatement.
    def enterCondStatement(self, ctx:SmallCParser.CondStatementContext):
        pass

    # Exit a parse tree produced by SmallCParser#condStatement.
    def exitCondStatement(self, ctx:SmallCParser.CondStatementContext):
        pass


    # Enter a parse tree produced by SmallCParser#whileStatement.
    def enterWhileStatement(self, ctx:SmallCParser.WhileStatementContext):
        pass

    # Exit a parse tree produced by SmallCParser#whileStatement.
    def exitWhileStatement(self, ctx:SmallCParser.WhileStatementContext):
        pass


    # Enter a parse tree produced by SmallCParser#forStatement.
    def enterForStatement(self, ctx:SmallCParser.ForStatementContext):
        pass

    # Exit a parse tree produced by SmallCParser#forStatement.
    def exitForStatement(self, ctx:SmallCParser.ForStatementContext):
        pass


    # Enter a parse tree produced by SmallCParser#breakStatement.
    def enterBreakStatement(self, ctx:SmallCParser.BreakStatementContext):
        pass

    # Exit a parse tree produced by SmallCParser#breakStatement.
    def exitBreakStatement(self, ctx:SmallCParser.BreakStatementContext):
        pass


    # Enter a parse tree produced by SmallCParser#continueStatement.
    def enterContinueStatement(self, ctx:SmallCParser.ContinueStatementContext):
        pass

    # Exit a parse tree produced by SmallCParser#continueStatement.
    def exitContinueStatement(self, ctx:SmallCParser.ContinueStatementContext):
        pass


    # Enter a parse tree produced by SmallCParser#returnStatement.
    def enterReturnStatement(self, ctx:SmallCParser.ReturnStatementContext):
        pass

    # Exit a parse tree produced by SmallCParser#returnStatement.
    def exitReturnStatement(self, ctx:SmallCParser.ReturnStatementContext):
        pass


    # Enter a parse tree produced by SmallCParser#exprStatement.
    def enterExprStatement(self, ctx:SmallCParser.ExprStatementContext):
        pass

    # Exit a parse tree produced by SmallCParser#exprStatement.
    def exitExprStatement(self, ctx:SmallCParser.ExprStatementContext):
        pass


    # Enter a parse tree produced by SmallCParser#declaration.
    def enterDeclaration(self, ctx:SmallCParser.DeclarationContext):
        pass

    # Exit a parse tree produced by SmallCParser#declaration.
    def exitDeclaration(self, ctx:SmallCParser.DeclarationContext):
        pass


    # Enter a parse tree produced by SmallCParser#declarationSpecifiers.
    def enterDeclarationSpecifiers(self, ctx:SmallCParser.DeclarationSpecifiersContext):
        pass

    # Exit a parse tree produced by SmallCParser#declarationSpecifiers.
    def exitDeclarationSpecifiers(self, ctx:SmallCParser.DeclarationSpecifiersContext):
        pass


    # Enter a parse tree produced by SmallCParser#initDeclaratorList.
    def enterInitDeclaratorList(self, ctx:SmallCParser.InitDeclaratorListContext):
        pass

    # Exit a parse tree produced by SmallCParser#initDeclaratorList.
    def exitInitDeclaratorList(self, ctx:SmallCParser.InitDeclaratorListContext):
        pass


    # Enter a parse tree produced by SmallCParser#initDeclarator.
    def enterInitDeclarator(self, ctx:SmallCParser.InitDeclaratorContext):
        pass

    # Exit a parse tree produced by SmallCParser#initDeclarator.
    def exitInitDeclarator(self, ctx:SmallCParser.InitDeclaratorContext):
        pass


    # Enter a parse tree produced by SmallCParser#declarator.
    def enterDeclarator(self, ctx:SmallCParser.DeclaratorContext):
        pass

    # Exit a parse tree produced by SmallCParser#declarator.
    def exitDeclarator(self, ctx:SmallCParser.DeclaratorContext):
        pass


    # Enter a parse tree produced by SmallCParser#directDeclarator.
    def enterDirectDeclarator(self, ctx:SmallCParser.DirectDeclaratorContext):
        pass

    # Exit a parse tree produced by SmallCParser#directDeclarator.
    def exitDirectDeclarator(self, ctx:SmallCParser.DirectDeclaratorContext):
        pass


    # Enter a parse tree produced by SmallCParser#pointer.
    def enterPointer(self, ctx:SmallCParser.PointerContext):
        pass

    # Exit a parse tree produced by SmallCParser#pointer.
    def exitPointer(self, ctx:SmallCParser.PointerContext):
        pass


    # Enter a parse tree produced by SmallCParser#expression.
    def enterExpression(self, ctx:SmallCParser.ExpressionContext):
        pass

    # Exit a parse tree produced by SmallCParser#expression.
    def exitExpression(self, ctx:SmallCParser.ExpressionContext):
        pass


    # Enter a parse tree produced by SmallCParser#assignment.
    def enterAssignment(self, ctx:SmallCParser.AssignmentContext):
        pass

    # Exit a parse tree produced by SmallCParser#assignment.
    def exitAssignment(self, ctx:SmallCParser.AssignmentContext):
        pass


    # Enter a parse tree produced by SmallCParser#condition.
    def enterCondition(self, ctx:SmallCParser.ConditionContext):
        pass

    # Exit a parse tree produced by SmallCParser#condition.
    def exitCondition(self, ctx:SmallCParser.ConditionContext):
        pass


    # Enter a parse tree produced by SmallCParser#disjunction.
    def enterDisjunction(self, ctx:SmallCParser.DisjunctionContext):
        pass

    # Exit a parse tree produced by SmallCParser#disjunction.
    def exitDisjunction(self, ctx:SmallCParser.DisjunctionContext):
        pass


    # Enter a parse tree produced by SmallCParser#conjunction.
    def enterConjunction(self, ctx:SmallCParser.ConjunctionContext):
        pass

    # Exit a parse tree produced by SmallCParser#conjunction.
    def exitConjunction(self, ctx:SmallCParser.ConjunctionContext):
        pass


    # Enter a parse tree produced by SmallCParser#comparison.
    def enterComparison(self, ctx:SmallCParser.ComparisonContext):
        pass

    # Exit a parse tree produced by SmallCParser#comparison.
    def exitComparison(self, ctx:SmallCParser.ComparisonContext):
        pass


    # Enter a parse tree produced by SmallCParser#relation.
    def enterRelation(self, ctx:SmallCParser.RelationContext):
        pass

    # Exit a parse tree produced by SmallCParser#relation.
    def exitRelation(self, ctx:SmallCParser.RelationContext):
        pass


    # Enter a parse tree produced by SmallCParser#plus.
    def enterPlus(self, ctx:SmallCParser.PlusContext):
        pass

    # Exit a parse tree produced by SmallCParser#plus.
    def exitPlus(self, ctx:SmallCParser.PlusContext):
        pass


    # Enter a parse tree produced by SmallCParser#times.
    def enterTimes(self, ctx:SmallCParser.TimesContext):
        pass

    # Exit a parse tree produced by SmallCParser#times.
    def exitTimes(self, ctx:SmallCParser.TimesContext):
        pass


    # Enter a parse tree produced by SmallCParser#cast.
    def enterCast(self, ctx:SmallCParser.CastContext):
        pass

    # Exit a parse tree produced by SmallCParser#cast.
    def exitCast(self, ctx:SmallCParser.CastContext):
        pass


    # Enter a parse tree produced by SmallCParser#unary.
    def enterUnary(self, ctx:SmallCParser.UnaryContext):
        pass

    # Exit a parse tree produced by SmallCParser#unary.
    def exitUnary(self, ctx:SmallCParser.UnaryContext):
        pass


    # Enter a parse tree produced by SmallCParser#postfix.
    def enterPostfix(self, ctx:SmallCParser.PostfixContext):
        pass

    # Exit a parse tree produced by SmallCParser#postfix.
    def exitPostfix(self, ctx:SmallCParser.PostfixContext):
        pass


    # Enter a parse tree produced by SmallCParser#primary.
    def enterPrimary(self, ctx:SmallCParser.PrimaryContext):
        pass

    # Exit a parse tree produced by SmallCParser#primary.
    def exitPrimary(self, ctx:SmallCParser.PrimaryContext):
        pass


    # Enter a parse tree produced by SmallCParser#constant.
    def enterConstant(self, ctx:SmallCParser.ConstantContext):
        pass

    # Exit a parse tree produced by SmallCParser#constant.
    def exitConstant(self, ctx:SmallCParser.ConstantContext):
        pass


    # Enter a parse tree produced by SmallCParser#assignmentOperator.
    def enterAssignmentOperator(self, ctx:SmallCParser.AssignmentOperatorContext):
        pass

    # Exit a parse tree produced by SmallCParser#assignmentOperator.
    def exitAssignmentOperator(self, ctx:SmallCParser.AssignmentOperatorContext):
        pass


    # Enter a parse tree produced by SmallCParser#expressionList.
    def enterExpressionList(self, ctx:SmallCParser.ExpressionListContext):
        pass

    # Exit a parse tree produced by SmallCParser#expressionList.
    def exitExpressionList(self, ctx:SmallCParser.ExpressionListContext):
        pass


