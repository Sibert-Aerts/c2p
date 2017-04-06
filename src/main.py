import sys
import c2p
import traceback

from antlr4 import * # type: ignore
from c2p.grammar.antlr.SmallCLexer import SmallCLexer
from c2p.grammar.antlr.SmallCParser import SmallCParser
from c2p.grammar.ast.visitor import ASTVisitor
from c2p.grammar.ast.visualize import Visualiser

def run(argv):
    if len(argv) < 2:
        sys.exit('Supply a C code file to compile.')

    parser = SmallCParser(CommonTokenStream(SmallCLexer(FileStream(argv[1]))))
    tree = parser.program()

    try:
        AST = ASTVisitor().visit(tree)

        f = open('out.dot', 'w')
        f.write(Visualiser.make_dot(AST))
        print("AST generation successful. Output written to \'out.dot\'")

        
    except:
        exceptiondata = traceback.format_exc().splitlines()
        print('Encountered {0}:'.format(exceptiondata[-1]))
        [print(l) for l in exceptiondata[-3:-1]]
        
if __name__ == '__main__':
    run(sys.argv)
