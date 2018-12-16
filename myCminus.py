import sys
from antlr4 import *
import CminusInter
from CminusAST import CreateAst
from gen.CminusLexer import CminusLexer
from gen.CminusParser import CminusParser
from CminusTable import SemanticAnalysisTableG
from CminusInter2MIPS import IntermediateToMIPS

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

inter = CminusInter.IntermedCode(ast)

asm = IntermediateToMIPS(semantic, inter)

print("#" * 110)

print(asm)

print("#" * 110)

print(asm.semantic)

print("#" * 110)

print(asm.intermediate)
