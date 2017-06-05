from antlr4.error.ErrorListener import ErrorListener
from .codegen.error import PositionalError
from .source_interval import SourceLocation, SourceInterval

class ParserSyntaxErrorListener(ErrorListener):
    def __init__(self):
        super(ParserSyntaxErrorListener, self).__init__()

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        loc = SourceLocation(line, column)
        raise PositionalError('Syntax error: ' + msg, SourceInterval(loc, loc))
