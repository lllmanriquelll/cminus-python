# Generated from Cminus.g4 by ANTLR 4.7.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .CminusParser import CminusParser
else:
    from CminusParser import CminusParser

# This class defines a complete generic visitor for a parse tree produced by CminusParser.

class CminusVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by CminusParser#program.
    def visitProgram(self, ctx:CminusParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CminusParser#declaration_list.
    def visitDeclaration_list(self, ctx:CminusParser.Declaration_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CminusParser#declaration.
    def visitDeclaration(self, ctx:CminusParser.DeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CminusParser#var_declaration.
    def visitVar_declaration(self, ctx:CminusParser.Var_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CminusParser#type_specifier.
    def visitType_specifier(self, ctx:CminusParser.Type_specifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CminusParser#fun_declaration.
    def visitFun_declaration(self, ctx:CminusParser.Fun_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CminusParser#params.
    def visitParams(self, ctx:CminusParser.ParamsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CminusParser#param_list.
    def visitParam_list(self, ctx:CminusParser.Param_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CminusParser#param.
    def visitParam(self, ctx:CminusParser.ParamContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CminusParser#compound_statement.
    def visitCompound_statement(self, ctx:CminusParser.Compound_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CminusParser#local_declarations.
    def visitLocal_declarations(self, ctx:CminusParser.Local_declarationsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CminusParser#statement_list.
    def visitStatement_list(self, ctx:CminusParser.Statement_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CminusParser#statement.
    def visitStatement(self, ctx:CminusParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CminusParser#expression_statement.
    def visitExpression_statement(self, ctx:CminusParser.Expression_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CminusParser#selection_statement.
    def visitSelection_statement(self, ctx:CminusParser.Selection_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CminusParser#iteration_statement.
    def visitIteration_statement(self, ctx:CminusParser.Iteration_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CminusParser#return_statemet.
    def visitReturn_statemet(self, ctx:CminusParser.Return_statemetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CminusParser#expression.
    def visitExpression(self, ctx:CminusParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CminusParser#var.
    def visitVar(self, ctx:CminusParser.VarContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CminusParser#simple_expression.
    def visitSimple_expression(self, ctx:CminusParser.Simple_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CminusParser#relop.
    def visitRelop(self, ctx:CminusParser.RelopContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CminusParser#additive_expression.
    def visitAdditive_expression(self, ctx:CminusParser.Additive_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CminusParser#addop.
    def visitAddop(self, ctx:CminusParser.AddopContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CminusParser#term.
    def visitTerm(self, ctx:CminusParser.TermContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CminusParser#mulop.
    def visitMulop(self, ctx:CminusParser.MulopContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CminusParser#factor.
    def visitFactor(self, ctx:CminusParser.FactorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CminusParser#call.
    def visitCall(self, ctx:CminusParser.CallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CminusParser#args.
    def visitArgs(self, ctx:CminusParser.ArgsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CminusParser#arg_list.
    def visitArg_list(self, ctx:CminusParser.Arg_listContext):
        return self.visitChildren(ctx)



del CminusParser