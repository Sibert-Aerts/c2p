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
        dotList = Visualiser.to_dot_list(ast)
        return formatStr.format(dotList)

    def to_dot_list(item):
        myId = Visualiser.getId()

        out = str(myId) + '\n'
        out += '{0}[label={1}]'.format(myId, item.__class__.__name__) + '\n'

        for c in list(item):
            if isinstance(c, str) or isinstance(c, int) or isinstance(c, float) or c is None:
                out += '{0} -> {1}'.format(myId, Visualiser.val_to_dot(c))
            elif isinstance(c, CType):
                out += '{0} -> {1}'.format(myId, Visualiser.ctype_to_dot(c))
            elif isinstance(c, list):
                for q in c:
                    out += '{0} -> {1}'.format(myId, Visualiser.to_dot_list(q))
            else:
                out += '{0} -> {1}'.format(myId, Visualiser.to_dot_list(c))
        return out

    def ctype_to_dot(item):
        myId = Visualiser.getId()

        out = str(myId) + '\n'
        out += '{0}[label={1}]'.format(myId, item.__class__.__name__) + '\n'
        try:
            out += '{0} -> {1}'.format(myId, Visualiser.ctype_to_dot(item.t))
        except:
            pass
        return out

    def val_to_dot(item):
        myId = Visualiser.getId()

        out = str(myId) + '\n'
        out += '{0}[label={1}]'.format(myId, item) + '\n'
        return out
