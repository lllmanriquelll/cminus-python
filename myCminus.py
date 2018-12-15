import sys
from antlr4 import *
import CminusInter
from CminusAST import CreateAst
from gen.CminusLexer import CminusLexer
from gen.CminusParser import CminusParser
from CminusTable import SemanticAnalysisTableG

input_stream = FileStream('files/simple_test.c-')
lexer = CminusLexer(input_stream)
stream = CommonTokenStream(lexer)
parser = CminusParser(stream)
tree = parser.program()

ast = CreateAst().visit(tree)
semantic = SemanticAnalysisTableG(ast)

if semantic.errors:
    print('The input file contains errors:')
    for error in semantic.errors:
        print(error)
    sys.exit()

print(semantic)

inter = CminusInter.IntermedCode(ast)

for line in inter.intermediate:
    for elem in line:
        print('{:<15}'.format(elem) + '|', end=' ')
    print('')
