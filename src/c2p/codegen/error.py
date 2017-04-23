from typing import Any
from c2p.source_interval import SourceInterval

class PositionalError(Exception):
    '''An error, tagged with a SourceInterval.'''
    def __init__(self, message: Any, where: SourceInterval) -> None:
        super(PositionalError, self).__init__(message)
        self.where = where

class ParseError(PositionalError):
    '''A parse error. The given program is syntactically incorrect.'''
    pass

class SemanticError(PositionalError):
    '''A semantic error encountered in a syntactically correct program.'''
    pass
