class SemanticError(ValueError):
    '''A semantic error encountered in a syntactically correct program.'''
    def __init__(self, message):
        ValueError.__init__(self, message)
        
    def __repr__():
        return 'SemanticError'