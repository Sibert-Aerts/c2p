class CodeNode:
    '''A class that holds generated code, and meta-data about this code.'''
    def __init__(self):
        self.code = []
        # Data useful to higher-up nodes
        self.type = None            # By and for Expressions
        self.maxStackSpace = 0      # By expressions, for methods
        self.maxVarSpace = 0        # By code blocks, for methods

    def add(self, other) -> None:
        '''Add a new instruction, or append all instructions from another node.'''
        if isinstance(other, CodeNode):
            self.code += other.code
        else:
            self.code.append(other)