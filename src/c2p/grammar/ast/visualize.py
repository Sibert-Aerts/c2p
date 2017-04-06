from ..antlr.SmallCVisitor import SmallCVisitor  # type: ignore
from ..antlr.SmallCParser import SmallCParser  # type: ignore
from .node import *
from ..ctypes import *

class Visualiser:
    id = 0
    def getId():
        Visualiser.id += 1
        return Visualiser.id

    def to_dot(ast):
        formatStr = \
            'digraph tree{{\nrankdir=TD\n{0}}}'
        rootId, dotList = Visualiser.to_dot_list(ast)
        return formatStr.format(dotList)

    def to_dot_list(item):
        myId = Visualiser.getId()

        stmts = '{0}[label={1}]'.format(myId, item.__class__.__name__) + '\n'

        def makeStmts(item, field):
            childId, childStmts = item
            return '{0} -> {1}[label={2}]\n{3}'.format(myId, childId, field, childStmts)
            
        for field in item._fields:
            c = getattr(item, field)

            if isinstance(c, str):
                stmts += makeStmts(Visualiser.str_to_dot(c), field)

            elif isinstance(c, int) or isinstance(c, float) or c is None:
                stmts += makeStmts(Visualiser.num_to_dot(c), field)

            elif isinstance(c, CType):
                stmts += makeStmts(Visualiser.ctype_to_dot(c), field)

            elif isinstance(c, list):
                # just append the elements in a list to the same parent node
                for q in c:
                    stmts += makeStmts(Visualiser.to_dot_list(q), field)

            else:
                stmts += makeStmts(Visualiser.to_dot_list(c), field)

        return myId, stmts

    def ctype_to_dot(item):
        myId = Visualiser.getId()

        stmts = '{0}[label={1}]'.format(myId, item.__class__.__name__) + '\n'

        # Try to access the CType's child to make it into a node too
        try:
            childId, childStmts = Visualiser.ctype_to_dot(item.t)
            stmts += '{0} -> {1}\n{2}'.format(myId, childId, childStmts)
        except:
            pass

        return myId, stmts

    def num_to_dot(item):
        myId = Visualiser.getId()
        stmts = '{0}[label={1}, shape=square]'.format(myId, item) + '\n'
        return myId, stmts

    def str_to_dot(item):
        myId = Visualiser.getId()
        stmts = '{0}[label="\\"{1}\\"", shape=square]'.format(myId, item) + '\n'
        return myId, stmts