from typing import Any
from c2p.source_interval import SourceInterval
from sys import stderr, argv
from antlr4 import FileStream # type: ignore

class PositionalError(Exception):
    '''An error, tagged with a SourceInterval.'''
    def __init__(self, message: Any, where: SourceInterval, warning: bool=False) -> None:
        super(PositionalError, self).__init__(message)
        self.where = where
        self.warning = warning

    def pretty_print(self, inputStream) -> str:
        sL = self.where.start.line - 1
        sC = self.where.start.column
        eL = self.where.stop.line - 1
        eC = self.where.stop.column + 1

        lines = inputStream.strdata.split('\n')
        HIGHLIGHT = '\x1b[36m' if self.warning else '\x1b[31;1m'
        RESET = '\x1b[0m'
        lines[sL] = lines[sL][:sC] + HIGHLIGHT + lines[sL][sC:]
        if sL == eL:
            eC += len(HIGHLIGHT)
        lines[eL] = lines[eL][:eC] + RESET + lines[eL][eC:]

        noun = 'Warning' if self.warning else 'Error'
        output = []
        output.append('\n%s in file %s:' % (noun, argv[1]))
        for i, l in list(enumerate(lines, 1))[max(0, sL - 1) : eL + 2]:
            output.append('\x1b[33;1m%4d \x1b[0m%s' % (i, l))

        output.append(HIGHLIGHT + str(self) + RESET + '\n')
        return '\n'.join(output)

def warn(message: Any, where: SourceInterval) -> None:
    '''Show a warning to stderr.'''

    if "-w" in argv: return
    # HACK: we read argv[1] all over, here! Blah.
    e = PositionalError(message, where, True)
    stderr.write(e.pretty_print(FileStream(argv[1])))

class ParseError(PositionalError):
    '''A parse error. The given program is syntactically incorrect.'''
    pass

class ASTError(PositionalError):
    '''
    This error indicates that the source file, while syntactically valid, contains some
    semantic error that prevents us from parsing a proper AST. Compilation should fail.
    '''
    pass

class SemanticError(PositionalError):
    '''A semantic error encountered in a syntactically correct program.'''
    pass
