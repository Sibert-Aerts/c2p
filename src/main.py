import sys
import c2p
import traceback

from antlr4 import * # type: ignore
from c2p.grammar.antlr.SmallCLexer import SmallCLexer
from c2p.grammar.antlr.SmallCParser import SmallCParser
from c2p.grammar.ast.visitor import ASTVisitor
from c2p.grammar.ast.visualize import Visualizer
from c2p.codegen.environment import Environment

def to_file(filename, text):
    f = open(filename, 'w')
    f.write(text)

def run(argv):
    if len(argv) < 2:
        sys.exit('Supply a C code file to compile.')

    parser = SmallCParser(CommonTokenStream(SmallCLexer(FileStream(argv[1]))))
    tree = parser.program()

    action = ''
    try:
        action = 'generating the AST'
        ast = ASTVisitor().visit(tree)

        action = 'rendering the AST to DOT'
        dotFileName = 'AST.dot'
        to_file(dotFileName, Visualizer().make_dot(ast))
        print('AST generation successful. Output written to \'{}\''.format(dotFileName))

        action = 'compiling the AST to code'
        code = ast.to_code(Environment()).code
        codeText = '\n'.join(op.emit() for op in code) + '\n'

        action = 'writing the code to a file'
        codeFileName = 'code.p'
        to_file(codeFileName, codeText)
        print('Code generation successful. Output written to \'{}\''.format(codeFileName))

    except ValueError as e:
        # Don't print a gigantic stack trace each time.
        exceptiondata = traceback.format_exc().splitlines()
        print('Encountered {0} while {1}:'.format(e.__class__.__name__, action))
        print(e)
    except NotImplementedError as e:
        exceptiondata = traceback.format_exc().splitlines()
        print('Encountered {0} while {1}:'.format(e.__class__.__name__, action))
        if isinstance(e, NotImplementedError):
            [print(l) for l in exceptiondata[-3:-1]]

if __name__ == '__main__':
    run(sys.argv)
