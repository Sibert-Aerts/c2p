from ..antlr.SmallCVisitor import SmallCVisitor  # type: ignore
from ..antlr.SmallCParser import SmallCParser  # type: ignore
from .node import *
from ..ctypes import *

class Visualizer:
    def __init__(self) -> None:
        self.id = 0

    def getId(self) -> int:
        self.id += 1
        return self.id

    # Convert an AST into a full DOT file
    def make_dot(self, ast: ASTNode):
        formatStr = \
            'digraph tree{{\nrankdir=TD\n{0}}}'
        rootId, dotList = self.ast_to_dot(ast)
        return formatStr.format(dotList)

    # Convert an AST node and its children into a series of DOT statements
    def ast_to_dot(self, item: ASTNode):
        myId = self.getId()

        stmts = '{0}[label={1}]'.format(myId, item.__class__.__name__) + '\n'

        def makeStmts(item, field):
            childId, childStmts = item
            return '{0} -> {1}[label={2}]\n{3}'.format(myId, childId, field, childStmts)

        for field, c in item.__dict__.items():

            if isinstance(c, str):
                stmts += makeStmts(self.str_to_dot(c), field)

            elif isinstance(c, int) or isinstance(c, float) or c is None:
                stmts += makeStmts(self.num_to_dot(c), field)

            elif isinstance(c, CType):
                stmts += makeStmts(self.ctype_to_dot(c), field)

            elif isinstance(c, list):
                # just append the elements in a list to the same parent node
                for q in c:
                    stmts += makeStmts(self.ast_to_dot(q), field)
                    
            elif isinstance(c, ASTNode):
                stmts += makeStmts(self.ast_to_dot(c), field)

        return myId, stmts

    # Convert a CType (and its children) into a series of DOT statements
    def ctype_to_dot(self, item: CType):
        myId = self.getId()

        stmts = '{0}[label={1}]'.format(myId, item.__class__.__name__) + '\n'

        # Try to access the CType's child to make it into a node too
        if isinstance(item, CLayerType):
            childId, childStmts = self.ctype_to_dot(item.t)
            stmts += '{0} -> {1}\n{2}'.format(myId, childId, childStmts)

        return myId, stmts

    # Convert a numeric value (or None) into a DOT statement
    def num_to_dot(self, item):
        myId = self.getId()
        stmts = '{0}[label={1}, shape=square]'.format(myId, item) + '\n'
        return myId, stmts

    # Convert a string value into a DOT statement
    def str_to_dot(self, item):
        myId = self.getId()
        stmts = '{0}[label="\\"{1}\\"", shape=square]'.format(myId, item) + '\n'
        return myId, stmts