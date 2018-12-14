# Generated from Cminus.g4 by ANTLR 4.7.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .CminusParser import CminusParser
else:
    from CminusParser import CminusParser

# This class defines a complete listener for a parse tree produced by CminusParser.
class CminusListener(ParseTreeListener):

    # Enter a parse tree produced by CminusParser#program.
    def enterProgram(self, ctx:CminusParser.ProgramContext):
        pass

    # Exit a parse tree produced by CminusParser#program.
    def exitProgram(self, ctx:CminusParser.ProgramContext):
        pass


    # Enter a parse tree produced by CminusParser#declaration.
    def enterDeclaration(self, ctx:CminusParser.DeclarationContext):
        pass

    # Exit a parse tree produced by CminusParser#declaration.
    def exitDeclaration(self, ctx:CminusParser.DeclarationContext):
        pass


    # Enter a parse tree produced by CminusParser#var_declaration.
    def enterVar_declaration(self, ctx:CminusParser.Var_declarationContext):
        pass

    # Exit a parse tree produced by CminusParser#var_declaration.
    def exitVar_declaration(self, ctx:CminusParser.Var_declarationContext):
        pass


    # Enter a parse tree produced by CminusParser#type_specifier.
    def enterType_specifier(self, ctx:CminusParser.Type_specifierContext):
        pass

    # Exit a parse tree produced by CminusParser#type_specifier.
    def exitType_specifier(self, ctx:CminusParser.Type_specifierContext):
        pass


    # Enter a parse tree produced by CminusParser#fun_declaration.
    def enterFun_declaration(self, ctx:CminusParser.Fun_declarationContext):
        pass

    # Exit a parse tree produced by CminusParser#fun_declaration.
    def exitFun_declaration(self, ctx:CminusParser.Fun_declarationContext):
        pass


    # Enter a parse tree produced by CminusParser#params.
    def enterParams(self, ctx:CminusParser.ParamsContext):
        pass

    # Exit a parse tree produced by CminusParser#params.
    def exitParams(self, ctx:CminusParser.ParamsContext):
        pass


    # Enter a parse tree produced by CminusParser#param_list.
    def enterParam_list(self, ctx:CminusParser.Param_listContext):
        pass

    # Exit a parse tree produced by CminusParser#param_list.
    def exitParam_list(self, ctx:CminusParser.Param_listContext):
        pass


    # Enter a parse tree produced by CminusParser#param.
    def enterParam(self, ctx:CminusParser.ParamContext):
        pass

    # Exit a parse tree produced by CminusParser#param.
    def exitParam(self, ctx:CminusParser.ParamContext):
        pass


    # Enter a parse tree produced by CminusParser#compound_decl.
    def enterCompound_decl(self, ctx:CminusParser.Compound_declContext):
        pass

    # Exit a parse tree produced by CminusParser#compound_decl.
    def exitCompound_decl(self, ctx:CminusParser.Compound_declContext):
        pass


    # Enter a parse tree produced by CminusParser#local_declarations.
    def enterLocal_declarations(self, ctx:CminusParser.Local_declarationsContext):
        pass

    # Exit a parse tree produced by CminusParser#local_declarations.
    def exitLocal_declarations(self, ctx:CminusParser.Local_declarationsContext):
        pass


    # Enter a parse tree produced by CminusParser#statement_list.
    def enterStatement_list(self, ctx:CminusParser.Statement_listContext):
        pass

    # Exit a parse tree produced by CminusParser#statement_list.
    def exitStatement_list(self, ctx:CminusParser.Statement_listContext):
        pass


    # Enter a parse tree produced by CminusParser#statement.
    def enterStatement(self, ctx:CminusParser.StatementContext):
        pass

    # Exit a parse tree produced by CminusParser#statement.
    def exitStatement(self, ctx:CminusParser.StatementContext):
        pass


    # Enter a parse tree produced by CminusParser#expression_decl.
    def enterExpression_decl(self, ctx:CminusParser.Expression_declContext):
        pass

    # Exit a parse tree produced by CminusParser#expression_decl.
    def exitExpression_decl(self, ctx:CminusParser.Expression_declContext):
        pass


    # Enter a parse tree produced by CminusParser#selection_decl.
    def enterSelection_decl(self, ctx:CminusParser.Selection_declContext):
        pass

    # Exit a parse tree produced by CminusParser#selection_decl.
    def exitSelection_decl(self, ctx:CminusParser.Selection_declContext):
        pass


    # Enter a parse tree produced by CminusParser#iteration_decl.
    def enterIteration_decl(self, ctx:CminusParser.Iteration_declContext):
        pass

    # Exit a parse tree produced by CminusParser#iteration_decl.
    def exitIteration_decl(self, ctx:CminusParser.Iteration_declContext):
        pass


    # Enter a parse tree produced by CminusParser#return_decl.
    def enterReturn_decl(self, ctx:CminusParser.Return_declContext):
        pass

    # Exit a parse tree produced by CminusParser#return_decl.
    def exitReturn_decl(self, ctx:CminusParser.Return_declContext):
        pass


    # Enter a parse tree produced by CminusParser#expression.
    def enterExpression(self, ctx:CminusParser.ExpressionContext):
        pass

    # Exit a parse tree produced by CminusParser#expression.
    def exitExpression(self, ctx:CminusParser.ExpressionContext):
        pass


    # Enter a parse tree produced by CminusParser#var.
    def enterVar(self, ctx:CminusParser.VarContext):
        pass

    # Exit a parse tree produced by CminusParser#var.
    def exitVar(self, ctx:CminusParser.VarContext):
        pass


    # Enter a parse tree produced by CminusParser#simple_expression.
    def enterSimple_expression(self, ctx:CminusParser.Simple_expressionContext):
        pass

    # Exit a parse tree produced by CminusParser#simple_expression.
    def exitSimple_expression(self, ctx:CminusParser.Simple_expressionContext):
        pass


    # Enter a parse tree produced by CminusParser#additive_expression.
    def enterAdditive_expression(self, ctx:CminusParser.Additive_expressionContext):
        pass

    # Exit a parse tree produced by CminusParser#additive_expression.
    def exitAdditive_expression(self, ctx:CminusParser.Additive_expressionContext):
        pass


    # Enter a parse tree produced by CminusParser#term.
    def enterTerm(self, ctx:CminusParser.TermContext):
        pass

    # Exit a parse tree produced by CminusParser#term.
    def exitTerm(self, ctx:CminusParser.TermContext):
        pass


    # Enter a parse tree produced by CminusParser#factor.
    def enterFactor(self, ctx:CminusParser.FactorContext):
        pass

    # Exit a parse tree produced by CminusParser#factor.
    def exitFactor(self, ctx:CminusParser.FactorContext):
        pass


    # Enter a parse tree produced by CminusParser#call.
    def enterCall(self, ctx:CminusParser.CallContext):
        pass

    # Exit a parse tree produced by CminusParser#call.
    def exitCall(self, ctx:CminusParser.CallContext):
        pass


