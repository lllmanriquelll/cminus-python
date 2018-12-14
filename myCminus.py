from antlr4 import *
from AstCreator import CreateAst
from gen.CminusLexer import CminusLexer
from gen.CminusParser import CminusParser

input_stream = FileStream('files/simple_test.c-')
lexer = CminusLexer(input_stream)
stream = CommonTokenStream(lexer)
parser = CminusParser(stream)
tree = parser.program()

ast = CreateAst().visit(tree)


