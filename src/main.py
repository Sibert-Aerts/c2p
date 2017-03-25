import sys
import c2p

from antlr4 import *
from c2p.grammar.antlr.SmallCLexer import SmallCLexer
from c2p.grammar.antlr.SmallCParser import SmallCParser
from c2p.grammar.ast.visitor import ASTVisitor

def run(argv):
    if len(argv) < 2:
        sys.exit('Supply a C code file to compile.')

    parser = SmallCParser(CommonTokenStream(SmallCLexer(FileStream(argv[1]))))
    tree = parser.program()
    print(ASTVisitor().visit(tree))

if __name__ == '__main__':
    run(sys.argv)
