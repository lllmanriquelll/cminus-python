from gen.CminusParser import CminusParser
from gen.CminusVisitor import CminusVisitor
from CminusComponents import *


class CreateAst(CminusVisitor):

    def visitProgram(self, ctx: CminusParser.ProgramContext):
        return Program(
            decl_list=[self.visit(decls) for decls in ctx.declaration_list],
            line=ctx.start.line,
        )

    def visitDeclaration(self, ctx: CminusParser.DeclarationContext):
        return Decl(
            var_decl=self.visit(ctx.var_declaration()) if ctx.var_declaration() is not None else None,
            fun_decl=self.visit(ctx.fun_declaration()) if ctx.fun_declaration() is not None else None,
            line=ctx.start.line,
        )

    def visitVar_declaration(self, ctx: CminusParser.Var_declarationContext):
        if ctx.NUMBER() is not None:
            return VarDecl(
                type_=(self.visit(ctx.type_specifier())),
                id_=ctx.ID().getText(),
                num=ctx.NUMBER().getText(),
                line=ctx.start.line,
            )
        return VarDecl(
            type_=self.visit(ctx.type_specifier()),
            id_=ctx.ID().getText(),
            line=ctx.start.line,
        )

    def visitType_specifier(self, ctx: CminusParser.Type_specifierContext):
        return TypeSpecifier(
            type_spec=ctx.getText(),
            line=ctx.start.line,
        )

    def visitFun_declaration(self, ctx: CminusParser.Fun_declarationContext):
        return FunDecl(
            type_spec=self.visit(ctx.type_specifier()),
            id_=ctx.ID().getText(),
            params=self.visit(ctx.params()),
            decl_comp=self.visit(ctx.compound_decl()),
            line=ctx.start.line,
        )

    def visitParams(self, ctx: CminusParser.ParamsContext):
        if ctx.param_list() is not None:
            return Params(
                param_list=self.visit(ctx.param_list()),
                line=ctx.start.line,
            )
        return Params(
            type_=ctx.getText(),
            line=ctx.start.line,
        )

    def visitParam_list(self, ctx: CminusParser.Param_listContext):
        if ctx.param_list() is not None:
            return ParamList(
                param_list=self.visit(ctx.param_list()),
                param=self.visit(ctx.param()),
                line=ctx.start.line
            )
        return ParamList(
            param_list=None,
            param=self.visit(ctx.param()),
            line=ctx.start.line
        )

    def visitParam(self, ctx: CminusParser.ParamContext):
        return Param(
            type_spec=self.visit(ctx.type_specifier()),
            id_=ctx.ID().getText(),
            flag_vet=True if ctx.LSBRACKET() else False,
            line=ctx.start.line,
        )

    def visitCompound_decl(self, ctx: CminusParser.Compound_declContext):
        return CompDecl(
            local_decl=[self.visit(decl) for decl in ctx.l_decl] if ctx.local_declarations() else [],
            stm_list=[self.visit(stm) for stm in ctx.stm_list] if ctx.statement_list() else [],
            line=ctx.start.line,
        )

    def visitLocal_declarations(self, ctx: CminusParser.Local_declarationsContext):
        return LocalDeclarations(
            var_decl=[self.visit(decl) for decl in ctx.var_decl],
            line=ctx.start.line,
        )

    def visitStatement_list(self, ctx: CminusParser.Statement_listContext):
        return StatementList(
            stm=[self.visit(stm) for stm in ctx.stms],
            line=ctx.start.line,
        )

    def visitStatement(self, ctx: CminusParser.StatementContext):
        if ctx.expression_decl():
            return Stm(child=self.visit(ctx.expression_decl()),
                       line=ctx.start.line,
                       )
        elif ctx.compound_decl():
            return Stm(child=self.visit(ctx.compound_decl()),
                       line=ctx.start.line, )
        elif ctx.selection_decl():
            return Stm(child=self.visit(ctx.selection_decl()),
                       line=ctx.start.line, )
        elif ctx.iteration_decl():
            return Stm(child=self.visit(ctx.iteration_decl()),
                       line=ctx.start.line, )
        elif ctx.return_decl():
            return Stm(child=self.visit(ctx.return_decl()),
                       line=ctx.start.line, )

    def visitExpression_decl(self, ctx: CminusParser.Expression_declContext):
        return ExpressionDecl(
            exp=self.visit(ctx.expression()) if ctx.expression() is not None else None,
            line=ctx.start.line,
        )

    def visitSelection_decl(self, ctx: CminusParser.Selection_declContext):
        if ctx.bodyElse is not None:
            return IfDecl(
                condition=self.visit(ctx.condition),
                body_if=[self.visit(cif) for cif in ctx.bodyIF],
                body_else=[self.visit(cel) for cel in ctx.bodyElse],
                line=ctx.start.line,
            )
        return IfDecl(
            condition=self.visit(ctx.expression()),
            body_if=[self.visit(cif) for cif in ctx.bodyIF],
            body_else=[],
            line=ctx.start.line,
        )

    def visitIteration_decl(self, ctx: CminusParser.Iteration_declContext):
        return WhileDecl(
            condition=self.visit(ctx.expression()),
            body=self.visit(ctx.statement()),
            line=ctx.start.line,
        )

    def visitReturn_decl(self, ctx: CminusParser.Return_declContext):
        if ctx.expression() is not None:
            return ReturnDecl(
                expression=self.visit(ctx.expression()),
                line=ctx.start.line,
            )
        return ReturnDecl(
            expression=None,
            line=ctx.start.line,
        )

    def visitExpression(self, ctx: CminusParser.ExpressionContext):
        if ctx.simple_expression() is not None:
            return Express(
                var=None,
                expression=None,
                simple_expression=self.visit(ctx.simple_expression()),
                line=ctx.start.line,
            )
        return Express(
            var=self.visit(ctx.var()),
            expression=self.visit(ctx.expression()),
            simple_expression=None,
            line=ctx.start.line,
        )

    def visitVar(self, ctx: CminusParser.VarContext):
        if ctx.expression() is not None:
            return Variable(
                id_=ctx.ID().getText(),
                expression=self.visit(ctx.expression()),
                line=ctx.start.line,
            )
        return Variable(
            id_=ctx.ID().getText(),
            line=ctx.start.line,
        )

    def visitSimple_expression(self, ctx: CminusParser.Simple_expressionContext):
        return Comp(
            left=self.visit(ctx.left) if ctx.left else None,
            relational=ctx.relational.text if ctx.relational else None,
            right=self.visit(ctx.right) if ctx.right else None,
            operation=self.visit(ctx.operation) if ctx.operation else None,
            line=ctx.start.line,
        )

    def visitAdditive_expression(self, ctx: CminusParser.Additive_expressionContext):
        return Operation(
            left=self.visit(ctx.additive_expression()) if ctx.additive_expression() else None,
            op=ctx.op.text if ctx.op else None,
            right=self.visit(ctx.term()) if ctx.term() else None,
            line=ctx.start.line,
        )

    def visitTerm(self, ctx: CminusParser.TermContext):
        return Operation(
            left=self.visit(ctx.term()) if ctx.term() else None,
            op=ctx.op.text if ctx.op else None,
            right=self.visit(ctx.factor()) if ctx.factor() else None,
            line=ctx.start.line,
        )

    def visitFactor(self, ctx: CminusParser.FactorContext):
        return Factor(
            num=ctx.NUMBER().getText() if ctx.NUMBER() else None,
            variable=self.visit(ctx.var()) if ctx.var() else None,
            call=self.visit(ctx.call()) if ctx.call() else None,
            expression=self.visit(ctx.expression()) if ctx.expression() else None,
            line=ctx.start.line,
        )

    def visitCall(self, ctx: CminusParser.CallContext):
        return Call(
            id_=ctx.ID().getText(),
            arg_list=[self.visit(args) for args in ctx.arg_list] if ctx.expression() is not None else None,
            line=ctx.start.line,
        )


class AstVisitor:
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))
