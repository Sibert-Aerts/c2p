from antlr4 import *
from SmallCListener import SmallCListener
from SmallCVisitor import SmallCVisitor
from SmallCLexer import SmallCLexer
from SmallCParser import SmallCParser

code = r'''
#include <stdio.h>
int main(int argc, char **argv)
{
   int number;
 
   printf("Enter an integer\nasdf");
   scanf("%d",&number);
 
   printf("Integer entered by you is %d", number);
 
   return 0;
}
'''

class TestC(SmallCVisitor):
    def visitProgram(self, ctx):
        #print(dir(ctx))
        return ctx

    pass
#    def visit(self, ctx):
#        print(ctx)
#        return ctx
# print(dir(SmallCListener))

def pctx(ctx, indent=0):
  if isinstance(ctx, TerminalNode):
    print('{0}{1}'.format('   '*indent, repr(str(ctx))))
  else:
    print('{0}{1}'.format('   '*indent, ctx.__class__.__name__[:-7]))
    for child in ctx.getChildren():
      pctx(child, indent+1)

test = TestC()
parser = SmallCParser(CommonTokenStream(SmallCLexer(InputStream(code))))
#print_level_order(parser.program().tree)
ctx = (test.visit(parser.program()))
pctx(ctx)

