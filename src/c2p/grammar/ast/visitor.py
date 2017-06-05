from ..antlr.SmallCVisitor import SmallCVisitor  # type: ignore
from ..antlr.SmallCParser import SmallCParser  # type: ignore
from .node import *
from ..ctypes import *
from ...util import Impossible
from ast import literal_eval
from ...codegen.error import ASTError
from c2p.source_interval import SourceLocation, SourceInterval

# Figure out which part of the code the node relates to
def where(ctx: Any):
    return SourceInterval(
        SourceLocation(ctx.start.line, ctx.start.column),
        SourceLocation(ctx.stop.line, ctx.stop.column + len(ctx.stop.text.split('\n')[0]) - 1))

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
            decl = PointerDeclarator(decl.where, decl)
        elif token == 'const':
            decl = ConstantDeclarator(decl.where, decl)

    return decl

class ASTVisitor(SmallCVisitor):

    # Visit a parse tree produced by SmallCParser#program.
    def visitProgram(self, ctx:SmallCParser.ProgramContext):
        declarations = [self.visit(c) for c in ctx.getChildren()
            if isinstance(c, SmallCParser.FunctionDeclarationContext)
            or isinstance(c, SmallCParser.FunctionDefinitionContext)
            or isinstance(c, SmallCParser.DeclarationContext)]
        return Program(where(ctx), declarations)


    # Visit a parse tree produced by SmallCParser#functionDeclaration.
    def visitFunctionDeclaration(self, ctx:SmallCParser.FunctionDeclarationContext):
        children = list(ctx.getChildren())
        # Underscores indicate a variable is an antlr4 object
        _specifiers, _pointer, _name = children[:3]
        _parameters = children[-3] if len(children) == 7 else None

        name = _name.getText()
        returnType = applyPointerAsType(self.visit(_specifiers), _pointer)
        parameters = self.visit(_parameters) if _parameters else []

        return FunctionDeclaration(where(ctx), name, returnType, parameters)


    # Visit a parse tree produced by SmallCParser#functionDefinition.
    def visitFunctionDefinition(self, ctx:SmallCParser.FunctionDefinitionContext):
        children = list(ctx.getChildren())
        _specifiers, _pointer, _name = children[:3]
        _body = children[-1]
        _parameters = children[-3] if len(children) == 7 else None

        name = _name.getText()
        returnType = applyPointerAsType(self.visit(_specifiers), _pointer)
        parameters = self.visit(_parameters) if _parameters else []
        body = self.visit(_body)

        return FunctionDefinition(where(ctx), name, returnType, parameters, body)


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

        return ParameterDeclaration(where(ctx), theType, declarator)



    # Visit a parse tree produced by SmallCParser#compoundStatement.
    def visitCompoundStatement(self, ctx:SmallCParser.CompoundStatementContext):
        declarations = [self.visit(c) for c in ctx.getChildren()
            if isinstance(c, SmallCParser.DeclarationContext)
            or isinstance(c, SmallCParser.StatementContext)]
        return CompoundStatement(where(ctx), declarations)


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

            return CondStatement(where(ctx), expr, trueBody, None)

        # if ( expression ) statement else statement
        elif len(children) == 7:
            _, _, _expr, _, _trueBody, _, _falseBody = children

            expr = self.visit(_expr)
            trueBody = self.visit(_trueBody)
            falseBody = self.visit(_falseBody)

            return CondStatement(where(ctx), expr, trueBody, falseBody)

        raise Impossible()

    # Visit a parse tree produced by SmallCParser#whileStatement.
    def visitWhileStatement(self, ctx:SmallCParser.WhileStatementContext):
        children = list(ctx.getChildren())

        # while ( expression ) statement
        _, _, _expr, _, _body = children

        expr = self.visit(_expr)
        body = self.visit(_body)

        return WhileStatement(where(ctx), expr, body)

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

        return ForStatement(where(ctx), left, center, right, body)


    # Visit a parse tree produced by SmallCParser#breakStatement.
    def visitBreakStatement(self, ctx:SmallCParser.BreakStatementContext):
        return BreakStatement(where(ctx))


    # Visit a parse tree produced by SmallCParser#continueStatement.
    def visitContinueStatement(self, ctx:SmallCParser.ContinueStatementContext):
        return ContinueStatement(where(ctx))


    # Visit a parse tree produced by SmallCParser#returnStatement.
    def visitReturnStatement(self, ctx:SmallCParser.ReturnStatementContext):
        children = list(ctx.getChildren())

        # return expression ;
        if len(children) == 3:
            return ReturnStatement(where(ctx), self.visit(children[1]))
        # return;
        return ReturnStatement(where(ctx), None)


    # Visit a parse tree produced by SmallCParser#exprStatement.
    def visitExprStatement(self, ctx:SmallCParser.ExprStatementContext):
        children = list(ctx.getChildren())

        if isinstance(children[0], SmallCParser.ExpressionContext):
            return ExprStatement(where(ctx), self.visit(children[0]))

        # just a blank ; statement
        return ExprStatement(where(ctx), None)



    # Visit a parse tree produced by SmallCParser#declaration.
    def visitDeclaration(self, ctx:SmallCParser.DeclarationContext):
        children = list(ctx.getChildren())

        theType = self.visit(children[0])
        declarators = [] # type: List[InitDeclarator]

        # initDeclaratorList is present
        if len(children) == 3:
            declarators = self.visit(children[1])

        return Declaration(where(ctx), theType, declarators)


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
                raise ASTError("Too many type specifiers", where(ctx))

        if theType is None:
            raise ASTError("Missing type specifier", where(ctx))

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

        return InitDeclarator(where(ctx), declarator, assignment)


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
             return IdentifierDeclarator(where(ctx), Identifier(where(ctx), children[0].getText()))

        # ( declarator )
        elif len(children) == 3 and isinstance(children[1], SmallCParser.DeclaratorContext):
            return self.visit(children[1])

        # directDeclarator [ assignment? ]
        elif children and isinstance(children[0], SmallCParser.DirectDeclaratorContext):
            # directDeclarator []
            if len(children) == 3:
                # An array without a length is just a pointer.
                return PointerDeclarator(where(ctx), self.visit(children[0]))

            # directDeclarator [ Constant ]
            elif len(children) == 4:
                length = self.visit(children[2])
                if not isinstance(length, Constant):
                    raise SemanticError("Array length is not a compile-time constant", where(children[2]))
                if not length.type.ignoreConst() == CInt():
                    raise SemanticError("Array length is not of type int", where(children[2]))
                return ArrayDeclarator(where(ctx), self.visit(children[0]), length.value)

        else:
            raise Impossible()


    # Visit a parse tree produced by SmallCParser#expression.
    def visitExpression(self, ctx:SmallCParser.ExpressionContext):
        children = list(ctx.getChildren())

        if len(children) == 1:
            return self.visit(children[0])

        _left, _, _right = children

        left = self.visit(_left)
        right = self.visit(_right)

        return Comma(where(ctx), left, right)


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
            return Assignment(where(ctx), left, right)
        elif op == '+=':
            return AddAssignment(where(ctx), left, right)
        elif op == '-=':
            return SubAssignment(where(ctx), left, right)
        elif op == '*=':
            return MulAssignment(where(ctx), left, right)
        elif op == '/=':
            return DivAssignment(where(ctx), left, right)
        else:
            raise Impossible()

    # Visit a parse tree produced by SmallCParser#condition.
    def visitCondition(self, ctx:SmallCParser.ConditionContext):
        children = list(ctx.getChildren())

        if len(children) == 1:
            return self.visit(children[0])

        _cond, _, _left, _, _right = children

        cond = self.visit(_cond)
        left = self.visit(_left)
        right = self.visit(_right)

        return TernaryIf(where(ctx), cond, left, right)


    # Visit a parse tree produced by SmallCParser#disjunction.
    def visitDisjunction(self, ctx:SmallCParser.DisjunctionContext):
        children = list(ctx.getChildren())

        if len(children) == 1:
            return self.visit(children[0])

        _left, _, _right = children

        left = self.visit(_left)
        right = self.visit(_right)

        return LogicalOr(where(ctx), left, right)

    # Visit a parse tree produced by SmallCParser#conjunction.
    def visitConjunction(self, ctx:SmallCParser.ConjunctionContext):
        children = list(ctx.getChildren())

        if len(children) == 1:
            return self.visit(children[0])

        _left, _, _right = children

        left = self.visit(_left)
        right = self.visit(_right)

        return LogicalAnd(where(ctx), left, right)


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
            return Equals(where(ctx), left, right)
        elif op == '!=':
            return NotEquals(where(ctx), left, right)
        else:
            raise Impossible()


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
                return LessThan(where(ctx), left, right)
            elif op == '>':
                return GreaterThan(where(ctx), left, right)
            elif op == '<=':
                return LessThanEquals(where(ctx), left, right)
            elif op == '>=':
                return GreaterThanEquals(where(ctx), left, right)
            else:
                raise Impossible()


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
            return Add(where(ctx), left, right)
        elif op == '-':
            return Subtract(where(ctx), left, right)
        else:
            raise Impossible()


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
            return Multiply(where(ctx), left, right)
        elif op == '/':
            return Divide(where(ctx), left, right)
        else:
            raise Impossible()


    # Visit a parse tree produced by SmallCParser#cast.
    def visitCast(self, ctx:SmallCParser.CastContext):
        children = list(ctx.getChildren())

        if len(children) == 1:
            return self.visit(children[0])

        # ( declarationSpecifiers pointer ) cast
        _, _specifiers, _pointer, _, _cast = children

        theType = applyPointerAsType(self.visit(_specifiers), _pointer)
        cast = self.visit(_cast)

        return Cast(where(ctx), theType, cast)


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
            return PrefixIncrement(where(ctx), expr)
        elif op == '--':
            return PrefixDecrement(where(ctx), expr)
        elif op == '&':
            return AddressOf(where(ctx), expr)
        elif op == '*':
            return Dereference(where(ctx), expr)
        elif op == '!':
            return LogicalNot(where(ctx), expr)
        elif op == '-':
            return Negate(where(ctx), expr)
        elif op == '+':
            return expr     # ignore it entirely
        else:
            raise Impossible()


    # Visit a parse tree produced by SmallCParser#postfix.
    def visitPostfix(self, ctx:SmallCParser.PostfixContext):
        children = list(ctx.getChildren())

        if len(children) == 1:
            return self.visit(children[0])

        subject = self.visit(children[0])
        tail = children[1:]

        # `tail` = '[' expression ']' | '(' expressionList? ')' | '++' | '--'

        # subject++ | subject--
        if len(tail) == 1:
            op = tail[0].getText()
            if op == '++':
                return PostfixIncrement(where(ctx), subject)
            elif op == '--':
                return PostfixDecrement(where(ctx), subject)
            else:
                raise Impossible()

        brace = tail[0].getText()

        # subject [ expression ]
        if brace == '[':
            index = self.visit(tail[1])
            return Index(where(ctx), subject, index)

        # subject ( expressionList? )
        elif brace == '(':
            # there's an expressionList
            if len(tail) == 3:
                expressions = self.visit(tail[1])
                return Call(where(ctx), subject, expressions)
            elif len(tail) == 2:
                return Call(where(ctx), subject, [])
            else:
                raise Impossible()

        else:
            raise Impossible()


    # Visit a parse tree produced by SmallCParser#primary.
    def visitPrimary(self, ctx:SmallCParser.PrimaryContext):
        children = list(ctx.getChildren())

        # constant
        if isinstance(children[0], SmallCParser.ConstantContext):
            return self.visit(children[0])

        # Identifier
        elif children[0].symbol.type == SmallCParser.Identifier:
            w = where(ctx)
            return IdentifierExpression(w, Identifier(w, children[0].getText()))

        # ( expression )
        elif isinstance(children[1], SmallCParser.ExpressionContext):
            return self.visit(children[1])

        else:
            raise Impossible()


    # Visit a parse tree produced by SmallCParser#constant.
    def visitConstant(self, ctx:SmallCParser.ConstantContext):
        _token , = list(ctx.getChildren())
        _type = _token.symbol.type
        _value = _token.getText()

        if _type == SmallCParser.FloatingConstant:
            return Constant(where(ctx), CConst(CFloat()), float(_value))
        elif _type == SmallCParser.IntegerConstant:
            return Constant(where(ctx), CConst(CInt()), int(_value))
        elif _type == SmallCParser.CharacterConstant:
            return Constant(where(ctx), CConst(CChar()), literal_eval(_value))
        elif _type == SmallCParser.StringConstant:
            _value = literal_eval(_value)
            return Constant(where(ctx), CConst(CArray(CConst(CChar()), len(_value) + 1)), _value)
        elif _type == SmallCParser.BoolConstant:
            if _value == "true":
                _value = True
            elif _value == "false":
                _value = False
            else:
                raise Impossible()
            return Constant(where(ctx), CConst(CBool()), _value)
        else:
            raise Impossible()


    # Visit a parse tree produced by SmallCParser#expressionList.
    def visitExpressionList(self, ctx:SmallCParser.ExpressionListContext):
        declarations = [self.visit(c) for c in ctx.getChildren()
            if isinstance(c, SmallCParser.AssignmentContext)]
        return declarations
