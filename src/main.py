import sys
import c2p
import traceback

from antlr4 import * # type: ignore
from c2p.grammar.antlr.SmallCLexer import SmallCLexer
from c2p.grammar.antlr.SmallCParser import SmallCParser
from c2p.grammar.ast.visitor import ASTVisitor
from c2p.grammar.ast.visualize import Visualiser
from c2p.codegen.codegen import *

def run(argv):
    if len(argv) < 2:
        sys.exit('Supply a C code file to compile.')

    parser = SmallCParser(CommonTokenStream(SmallCLexer(FileStream(argv[1]))))
    tree = parser.program()

    try:
        ast = ASTVisitor().visit(tree)

        dotFileName = 'AST.dot'
        f = open(dotFileName, 'w')
        f.write(Visualiser.make_dot(ast))
        print('AST generation successful. Output written to \'{}\''.format(dotFileName))

        code = ast.to_code(Environment()).code
        print('CODE:')
        codeText = ''
        for l in code:
            try:
                codeText += l.emit()
            except:
                codeText += l
            codeText += '\n'
        print(codeText)

        codeFileName = 'code.p'
        p = open(codeFileName, 'w')
        p.write(codeText)
        print('Code generation successful. Output written to \'{}\''.format(codeFileName))

    except:
        # Don't print a gigantic stack trace each time.
        exceptiondata = traceback.format_exc().splitlines()
        print('Encountered {0}:'.format(exceptiondata[-1]))
        [print(l) for l in exceptiondata[-3:-1]]

if __name__ == '__main__':
    run(sys.argv)
