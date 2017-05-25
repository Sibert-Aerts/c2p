import sys
import c2p
import traceback

from antlr4 import * # type: ignore
from c2p.grammar.antlr.SmallCLexer import SmallCLexer
from c2p.grammar.antlr.SmallCParser import SmallCParser
from c2p.grammar.ast.visitor import ASTVisitor
from c2p.grammar.ast.visualize import Visualizer
from c2p.codegen.environment import Environment
from c2p.codegen.error import PositionalError

def to_file(filename, text):
    f = open(filename, 'w')
    f.write(text)

def run(argv):
    if len(argv) < 2:
        sys.exit('Supply a C code file to compile.')

    inputStream = FileStream(argv[1])
    parser = SmallCParser(CommonTokenStream(SmallCLexer(inputStream)))
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

    except PositionalError as e:
        # XXX make this less ugly ;-;
        sL = e.where.start.line - 1
        sC = e.where.start.column
        eL = e.where.stop.line - 1
        eC = e.where.stop.column + 1

        lines = inputStream.strdata.split('\n')
        HIGHLIGHT = '\x1b[31m'
        RESET = '\x1b[0m'
        lines[sL] = lines[sL][:sC] + HIGHLIGHT + lines[sL][sC:]
        if sL == eL:
            eC += len(HIGHLIGHT)
        lines[eL] = lines[eL][:eC] + RESET + lines[eL][eC:]

        sys.stderr.write('\nError in file %s:\n' % argv[1])
        for i, l in list(enumerate(lines, 1))[sL - 1 : eL + 2]:
            sys.stderr.write('\x1b[33;1m%4d \x1b[0m%s\n' % (i, l))

        sys.stderr.write(HIGHLIGHT + str(e) + RESET + '\n\n')

    except ValueError as e:
        # Don't print a gigantic stack trace each time.
        exceptiondata = traceback.format_exc().splitlines()
        print('Encountered {0} while {1}:'.format(e.__class__.__name__, action))
        print(e)
    except NotImplementedError as e:
        exceptiondata = traceback.format_exc().splitlines()
        print('Encountered {0} while {1}:'.format(e.__class__.__name__, action))
        print(e)
        if isinstance(e, NotImplementedError):
            [print(l) for l in exceptiondata[-3:-1]]

if __name__ == '__main__':
    run(sys.argv)
