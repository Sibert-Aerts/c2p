import sys
import c2p
import traceback

from antlr4 import * # type: ignore
from c2p.grammar.antlr.SmallCLexer import SmallCLexer
from c2p.grammar.antlr.SmallCParser import SmallCParser
from c2p.grammar.ast.visitor import ASTVisitor

def run(argv):
    if len(argv) < 2:
        sys.exit('Supply a C code file to compile.')

    parser = SmallCParser(CommonTokenStream(SmallCLexer(FileStream(argv[1]))))
    tree = parser.program()

    try:
        print(ASTVisitor().visit(tree))
    except:
        exceptiondata = traceback.format_exc().splitlines()
        print('Encountered {0}: \n{1}'.format(exceptiondata[-1], exceptiondata[-3]))
        
if __name__ == '__main__':
    run(sys.argv)
