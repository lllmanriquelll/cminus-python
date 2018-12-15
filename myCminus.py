from antlr4 import *
from CminusAST import CreateAst
from gen.CminusLexer import CminusLexer
from gen.CminusParser import CminusParser
from CminusTable import SemanticAnalysisTableG

# Criado um input lendo o arquivo utilizando o metodo FileStream do ANTLR4
input_stream = FileStream('files/simple_test.c-')
lexer = CminusLexer(input_stream)
stream = CommonTokenStream(lexer)
parser = CminusParser(stream)
tree = parser.program()


ast = CreateAst().visit(tree)
semantic = SemanticAnalysisTableG(ast)


