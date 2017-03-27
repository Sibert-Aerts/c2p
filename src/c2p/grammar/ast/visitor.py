from ..antlr.SmallCVisitor import SmallCVisitor  # type: ignore
from ..antlr.SmallCParser import SmallCParser  # type: ignore
from .node import *
from ..ctypes import *


def applyStars(ctype:CType, stars:SmallCParser.PointerContext) -> CType:
    children = [c.getText() for c in stars.getChildren()]

    # int *const** x → declare x as pointer to (pointer to (const (pointer to (int)))
    # so it's just layered left-to-right starting from the first asterisk
    for token in children:
        if token == '*':
            ctype = CPointer(ctype)
        elif token == 'const':
            ctype = CConst(ctype)

    return ctype


class ASTVisitor(SmallCVisitor):

    # Visit a parse tree produced by SmallCParser#program.
    def visitProgram(self, ctx:SmallCParser.ProgramContext):
        declarations = [self.visit(c) for c in ctx.getChildren()
            if isinstance(c, SmallCParser.FunctionDefinitionContext)
            or isinstance(c, SmallCParser.DeclarationContext)]
        return Program(declarations)


    # Visit a parse tree produced by SmallCParser#functionDefinition.
    def visitFunctionDefinition(self, ctx:SmallCParser.FunctionDefinitionContext):
        # Underscores indicate a variable is an antlr4 object
        _declSpec, _pointer, _name,  _, _parameters, _, _body = list(ctx.getChildren())

        name = _name.getText()
        returnType = applyStars(self.visit(_declSpec), _pointer)
        parameters = self.visit(_parameters)
        body = self.visit(_body)

        return FunctionDefinition(name, returnType, parameters, body)


    # Visit a parse tree produced by SmallCParser#parameterDeclarationList.
    def visitParameterDeclarationList(self, ctx:SmallCParser.ParameterDeclarationListContext):
        declarations = [self.visit(c) for c in ctx.getChildren()
            if isinstance(c, SmallCParser.ParameterDeclarationContext)]
        return declarations


    # Visit a parse tree produced by SmallCParser#parameterDeclaration.
    def visitParameterDeclaration(self, ctx:SmallCParser.ParameterDeclarationContext):
        _specifiers, _declarator = list(ctx.getChildren())

        specifiers = self.visit(_specifiers)
        declarator = self.visit(_declarator)

        return ParameterDeclaration(specifiers, declarator)



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
        specifiers = [c.getText() for c in ctx.getChildren()]
        
        theType = None
        isConst = False
        for spec in specifiers:
            if spec == 'const':
                isConst = True
            elif theType is None:
                theType = fromTypeName[spec]
            else:
                raise ValueError("Too many type specifiers")

        if theType is None:
            raise ValueError("Missing type specifier")
        
        if isConst:
            return CConst(theType)
        return theType
               

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
