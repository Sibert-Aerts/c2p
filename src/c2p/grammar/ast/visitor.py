from ..antlr.SmallCVisitor import SmallCVisitor  # type: ignore
from ..antlr.SmallCParser import SmallCParser  # type: ignore
from .node import *
from ..ctypes import *


# Converts a CType and PointerContext into a CType properly wrapped in CPointer and CConst
def applyPointerAsType(ctype:CType, pointer:SmallCParser.PointerContext) -> CType:
    children = [c.getText() for c in pointer.getChildren()]

    # int *const** x → declare x as pointer to (pointer to (const pointer to (int))
    # so it's just layered left-to-right, starting from the first asterisk
    for token in children:
        if token == '*':
            ctype = CPointer(ctype)
        elif token == 'const':
            ctype = CConst(ctype)

    return ctype

def applyPointerAsDeclarator(decl:Declarator, pointer:SmallCParser.PointerContext) -> Declarator:
    children = [c.getText() for c in pointer.getChildren()]

    for token in children:
        if token == '*':
            decl = PointerDeclarator(decl)
        elif token == 'const':
            decl = ConstantDeclarator(decl)

    return decl

class ASTVisitor(SmallCVisitor):

    # Visit a parse tree produced by SmallCParser#program.
    def visitProgram(self, ctx:SmallCParser.ProgramContext):
        declarations = [self.visit(c) for c in ctx.getChildren()
            if isinstance(c, SmallCParser.FunctionDefinitionContext)
            or isinstance(c, SmallCParser.DeclarationContext)]
        return Program(declarations)


    # Visit a parse tree produced by SmallCParser#functionDefinition.
    def visitFunctionDefinition(self, ctx:SmallCParser.FunctionDefinitionContext):
        children = list(ctx.getChildren())
        # Underscores indicate a variable is an antlr4 object
        _specifiers, _pointer, _name  = children[:3]
        _body = children[-1]
        _parameters = children [-3] if len(children) == 7 else None
 
        name = _name.getText()
        returnType = applyPointerAsType(self.visit(_specifiers), _pointer)
        parameters = self.visit(_parameters) if _parameters is not None else []
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

        theType = self.visit(_specifiers)
        declarator = self.visit(_declarator)

        return ParameterDeclaration(theType, declarator)



    # Visit a parse tree produced by SmallCParser#compoundStatement.
    def visitCompoundStatement(self, ctx:SmallCParser.CompoundStatementContext):
        declarations = [self.visit(c) for c in ctx.getChildren()
            if isinstance(c, SmallCParser.DeclarationContext)
            or isinstance(c, SmallCParser.StatementContext)]
        return CompoundStatement(declarations)


    # Visit a parse tree produced by SmallCParser#statement.
    def visitStatement(self, ctx:SmallCParser.StatementContext):
        # A statement has exactly one child, nothing more, nothing less.
        return self.visit(list(ctx.getChildren())[0])


    # Visit a parse tree produced by SmallCParser#condStatement.
    def visitCondStatement(self, ctx:SmallCParser.CondStatementContext):
        children = list(ctx.getChildren())

        # if ( expression ) statement
        if len(children) == 5:
            _, _, _expr, _, _trueBody = children

            expr = self.visit(_expr)
            trueBody = self.visit(_trueBody)

            return CondStatement(expr, trueBody, None)

        # if ( expression ) statement else statement
        if len(children) == 7:
            _, _, _expr, _, _trueBody, _, _falseBody = children

            expr = self.visit(_expr)
            trueBody = self.visit(_trueBody)
            falseBody = self.visit(_falseBody)

            return CondStatement(expr, trueBody, falseBody)


    # Visit a parse tree produced by SmallCParser#whileStatement.
    def visitWhileStatement(self, ctx:SmallCParser.WhileStatementContext):
        children = list(ctx.getChildren())

        # while ( expression ) statement
        _, _, _expr, _, _body = children

        expr = self.visit(_expr)
        body = self.visit(_body)

        return WhileStatement(expr, body)

    # Visit a parse tree produced by SmallCParser#forStatement.
    def visitForStatement(self, ctx:SmallCParser.ForStatementContext):
        children = list(ctx.getChildren())

        # we know the last element will be the body
        body = self.visit(children[-1])

        # chop off the leading "while (" and ending ") statement" so we just get:
        # (declaration | expression? ';') expression? ';' expression?
        children = children[2: -2]
        
        left, center, right = None, None, None

        # declaration expression? ';' expression?
        if isinstance(children[0], SmallCParser.DeclarationContext):
            left = self.visit(children[0])
            children = children [1:]
        # expression ';' expression? ';' expression?
        elif isinstance(children[0], SmallCParser.ExpressionContext):
            left = self.visit(children[0])
            children = children [2:]
        # ';' expression? ';' expression?
        else:
            children = children [1:]

        # whatever the start was, we chopped it off, so now `children` holds
        # expression? ';' expression?

        if isinstance(children[0], SmallCParser.ExpressionContext):
            center = self.visit(children[0])
            children = children [1:]
        children = children [1:]

        # expression?

        if len(children) == 1:
            right = self.visit(children[0])

        return ForStatement(left, center, right, body)


    # Visit a parse tree produced by SmallCParser#breakStatement.
    def visitBreakStatement(self, ctx:SmallCParser.BreakStatementContext):
        return BreakStatement()


    # Visit a parse tree produced by SmallCParser#continueStatement.
    def visitContinueStatement(self, ctx:SmallCParser.ContinueStatementContext):
        return ContinueStatement()


    # Visit a parse tree produced by SmallCParser#returnStatement.
    def visitReturnStatement(self, ctx:SmallCParser.ReturnStatementContext):
        children = list(ctx.getChildren())
        
        # return expression ;
        if len(children) == 3:
            return ReturnStatement(self.visit(children[1]))
        # return;
        return ReturnStatement(None)


    # Visit a parse tree produced by SmallCParser#exprStatement.
    def visitExprStatement(self, ctx:SmallCParser.ExprStatementContext):
        children = list(ctx.getChildren())

        if isinstance(children[0], SmallCParser.ExpressionContext):
            return ExprStatement(self.visit(children[0]))
        
        # just a blank ; statement
        return ExprStatement(None)
        


    # Visit a parse tree produced by SmallCParser#declaration.
    def visitDeclaration(self, ctx:SmallCParser.DeclarationContext):
        children = list(ctx.getChildren())
        
        theType = self.visit(children[0])
        declarators = [] # type: List[InitDeclarator]

        # initDeclaratorList is present
        if len(children) == 3:
            declarators = self.visit(children[1])
        
        return Declaration(theType, declarators)


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
        declarators = [self.visit(c) for c in ctx.getChildren()
            if isinstance(c, SmallCParser.InitDeclaratorContext)]
        return declarators


    # Visit a parse tree produced by SmallCParser#initDeclarator.
    def visitInitDeclarator(self, ctx:SmallCParser.InitDeclaratorContext):
        children = list(ctx.getChildren())

        declarator = self.visit(children[0])
        assignment = None
        
        # assignment is present
        if len(children) == 3:
            assignment = self.visit(children[2])

        return InitDeclarator(declarator, assignment)


    # Visit a parse tree produced by SmallCParser#declarator.
    def visitDeclarator(self, ctx:SmallCParser.DeclaratorContext) -> Declarator:
        _pointer, _directDeclarator = list(ctx.getChildren())

        declarator = applyPointerAsDeclarator(self.visit(_directDeclarator), _pointer)

        return declarator


    # Visit a parse tree produced by SmallCParser#directDeclarator.
    def visitDirectDeclarator(self, ctx:SmallCParser.DirectDeclaratorContext) -> Declarator:
        children = list(ctx.getChildren())
        
        # Identifier
        if len(children) == 1:
             return IdentifierDeclarator(Identifier(children[0].getText()))
             
        # ( declarator )
        if isinstance(children[1], SmallCParser.DeclaratorContext):
            return self.visit(children[1])

        # directDeclarator [ assignment? ]
        if isinstance(children[0], SmallCParser.DirectDeclaratorContext):
            # directDeclarator []
            if len(children) == 3:
                # I put a None here and hope to remember it later.
                return ArrayDeclarator(self.visit(children[0]), None)
                
            # directDeclarator [ assignment ]
            if len(children) == 4:
                return ArrayDeclarator(self.visit(children[0]), self.visit(children[2]))


    # Visit a parse tree produced by SmallCParser#expression.
    def visitExpression(self, ctx:SmallCParser.ExpressionContext):
        children = list(ctx.getChildren())

        if len(children) == 1:
            return self.visit(children[0])

        _left, _, _right = children

        left = self.visit(_left)
        right = self.visit(_right)

        return Comma(left, right)


    # Visit a parse tree produced by SmallCParser#assignment.
    def visitAssignment(self, ctx:SmallCParser.AssignmentContext):
        children = list(ctx.getChildren())

        if len(children) == 1:
            return self.visit(children[0])

        _left, _op, _right = children

        left = self.visit(_left)
        op = _op.getText()
        right = self.visit(_right)

        if op == '=':
            return Assignment(left, right)
        if op == '+=':
            return AddAssignment(left, right)
        if op == '-=':
            return SubAssignment(left, right)
        if op == '*=':
            return MulAssignment(left, right)
        if op == '/=':
            return DivAssignment(left, right)


    # Visit a parse tree produced by SmallCParser#condition.
    def visitCondition(self, ctx:SmallCParser.ConditionContext):
        children = list(ctx.getChildren())

        if len(children) == 1:
            return self.visit(children[0])

        _cond, _, _left, _, _right = children

        cond = self.visit(_cond)
        left = self.visit(_left)
        right = self.visit(_right)

        return TernaryIf(cond, left, right)


    # Visit a parse tree produced by SmallCParser#disjunction.
    def visitDisjunction(self, ctx:SmallCParser.DisjunctionContext):
        children = list(ctx.getChildren())

        if len(children) == 1:
            return self.visit(children[0])

        _left, _, _right = children

        left = self.visit(_left)
        right = self.visit(_right)

        return LogicalOr(left, right)

    # Visit a parse tree produced by SmallCParser#conjunction.
    def visitConjunction(self, ctx:SmallCParser.ConjunctionContext):
        children = list(ctx.getChildren())

        if len(children) == 1:
            return self.visit(children[0])

        _left, _, _right = children

        left = self.visit(_left)
        right = self.visit(_right)

        return LogicalAnd(left, right)


    # Visit a parse tree produced by SmallCParser#comparison.
    def visitComparison(self, ctx:SmallCParser.ComparisonContext):
        children = list(ctx.getChildren())

        if len(children) == 1:
            return self.visit(children[0])

        _left, _op, _right = children

        left = self.visit(_left)
        op = _op.getText()
        right = self.visit(_right)

        if op == '==':
            return Equals(left, right)
        if op == '!=':
            return NotEquals(left, right)



    # Visit a parse tree produced by SmallCParser#relation.
    def visitRelation(self, ctx:SmallCParser.RelationContext):
        children = list(ctx.getChildren())

        # plus
        if len(children) == 1:
            return self.visit(children[0])

        # plus ('<' | '>' | '<=' | '>=') plus
        if len(children) == 3:
            _left, _op, _right = children

            left = self.visit(_left)
            op = _op.getText()
            right = self.visit(_right)
            
            if op == '<':
                return LessThan(left, right)
            if op == '>':
                return GreaterThan(left, right)
            if op == '<=':
                return LessThanEquals(left, right)
            if op == '>=':
                return GreaterThanEquals(left, right)


    # Visit a parse tree produced by SmallCParser#plus.
    def visitPlus(self, ctx:SmallCParser.PlusContext):
        children = list(ctx.getChildren())

        if len(children) == 1:
            return self.visit(children[0])

        _left, _op, _right  = children
        
        left = self.visit(_left)
        op = _op.getText()
        right = self.visit(_right)

        if op == '+':
            return Add(left, right)
        if op == '-':
            return Subtract(left, right)


    # Visit a parse tree produced by SmallCParser#times.
    def visitTimes(self, ctx:SmallCParser.TimesContext):
        children = list(ctx.getChildren())

        if len(children) == 1:
            return self.visit(children[0])

        _left, _op, _right  = children
        
        left = self.visit(_left)
        op = _op.getText()
        right = self.visit(_right)

        if op == '*':
            return Multiply(left, right)
        if op == '/':
            return Divide(left, right)


    # Visit a parse tree produced by SmallCParser#cast.
    def visitCast(self, ctx:SmallCParser.CastContext):
        children = list(ctx.getChildren())

        if len(children) == 1:
            return self.visit(children[0])

        # ( declarationSpecifiers pointer ) cast
        _, _specifiers, _pointer, _, _cast = children

        theType = applyPointerAsType(self.visit(_specifiers), _pointer)
        cast = self.visit(_cast)

        return Cast(theType, cast)


    # Visit a parse tree produced by SmallCParser#unary.
    def visitUnary(self, ctx:SmallCParser.UnaryContext):
        children = list(ctx.getChildren())

        if len(children) == 1:
            return self.visit(children[0])

        # ('++' | '--') unary | ('&' | '*' | '!' | '+' | '-') cast
        _op, _expr = children

        op = _op.getText()
        expr = self.visit(_expr)

        if op == '++':
            return PrefixIncrement(expr)
        if op == '--':
            return PrefixDecrement(expr)
        if op == '&':
            return AddressOf(expr)
        if op == '*':
            return Dereference(expr)
        if op == '!':
            return LogicalNot(expr)
        if op == '-':
            return Negate(expr)
        if op == '+':
            return expr     # ignore it entirely


    # Visit a parse tree produced by SmallCParser#postfix.
    def visitPostfix(self, ctx:SmallCParser.PostfixContext):
        children = list(ctx.getChildren())

        if len(children) == 1:
            return self.visit(children[0])

        subject = self.visit(children[0])
        children = children[1:]

        # `children` = '[' expression ']' | '(' expressionList? ')' | '++' | '--'

        # subject++ | subject--
        if len(children) == 1:
            op = children[0].getText()
            if op == '++':
                return PostfixIncrement(subject)
            if op == '--':
                return PostfixDecrement(subject)

        brace = children[0].getText()

        # subject [ expression ]
        if brace == '[':
            index = self.visit(children[1])
            return Index(subject, index)

        # subject ( expressionList? )
        if brace == '(':
            # there's an expressionList
            if len(children) == 3:
                expressions = self.visit(children[1])
                return Call(subject, expressions)
            return Call(subject, [])
            


    # Visit a parse tree produced by SmallCParser#primary.
    def visitPrimary(self, ctx:SmallCParser.PrimaryContext):
        children = list(ctx.getChildren())

        # constant
        if isinstance(children[0], SmallCParser.ConstantContext):
            return self.visit(children[0])

        # Identifier
        if children[0].symbol.type == SmallCParser.Identifier:
            return IdentifierExpression(Identifier(children[0].getText()))
            
        # ( expression )
        if isinstance(children[1], SmallCParser.ExpressionContext):
            return self.visit(children[1])



    # Visit a parse tree produced by SmallCParser#constant.
    def visitConstant(self, ctx:SmallCParser.ConstantContext):
        _token , = list(ctx.getChildren())
        _type = _token.symbol.type
        _value = _token.getText()

        if(_type == SmallCParser.FloatingConstant):
            return Constant(CConst(CFloat()), float(_value))

        if(_type == SmallCParser.IntegerConstant):
            return Constant(CConst(CInt()), int(_value))

        if(_type == SmallCParser.CharacterConstant):
            return Constant(CConst(CChar()), _value[1])

        if(_type == SmallCParser.StringConstant):
            return Constant(CConst(CArray(CConst(CChar()))), _value[1:-1])


    # Visit a parse tree produced by SmallCParser#expressionList.
    def visitExpressionList(self, ctx:SmallCParser.ExpressionListContext):
        declarations = [self.visit(c) for c in ctx.getChildren()
            if isinstance(c, SmallCParser.AssignmentContext)]
        return declarations
