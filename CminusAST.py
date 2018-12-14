from gen.CminusParser import CminusParser
from gen.CminusVisitor import CminusVisitor
from CminusComponents import *

class CreateAst(CminusVisitor):
    # Visit a parse tree produced by CminusParser#programa.
    def visitPrograma(self, ctx: CminusParser.ProgramaContext):
        return Programa(
            decl_lista=[self.visit(decls) for decls in ctx.decl],
            line=ctx.start.line,
        )

    # Visit a parse tree produced by CminusParser#declaracao_lista.
    def visitDeclaracao(self, ctx: CminusParser.DeclaracaoContext):
        return Decl(
            varDecl=self.visit(ctx.var_declaracao()) if ctx.var_declaracao() is not None else None,
            funDecl=self.visit(ctx.fun_declaracao()) if ctx.fun_declaracao() is not None else None,
            line=ctx.start.line,
        )

    # Visit a parse tree produced by CminusParser#var_declaracao.
    def visitVar_declaracao(self, ctx: CminusParser.Var_declaracaoContext):
        if ctx.NUM() is not None:
            return VarDecl(
                tipo=(self.visit(ctx.tipo_especificador())),
                id_=ctx.ID().getText(),
                num=ctx.NUM().getText(),
                line=ctx.start.line,
            )
        return VarDecl(
            tipo=self.visit(ctx.tipo_especificador()),
            id_=ctx.ID().getText(),
            line=ctx.start.line,
        )

    # Visit a parse tree produced by CminusParser#tipo_especificador.
    def visitTipo_especificador(self, ctx: CminusParser.Tipo_especificadorContext):
        return TipoEsp(
            tipoE_=ctx.getText(),
            line=ctx.start.line,
        )

    # Visit a parse tree produced by CminusParser#fun_declaracao.
    def visitFun_declaracao(self, ctx: CminusParser.Fun_declaracaoContext):
        return FunDecl(
            tipoE=self.visit(ctx.tipo_especificador()),
            id_=ctx.ID().getText(),
            parametros=self.visit(ctx.params()),
            declComp=self.visit(ctx.composto_decl()),
            line=ctx.start.line,
        )

    # Visit a parse tree produced by CminusParser#params.
    def visitParams(self, ctx: CminusParser.ParamsContext):
        if ctx.param_lista() is not None:
            return Parametros(
                listaParam=self.visit(ctx.param_lista()),
                line=ctx.start.line,
            )
        return Parametros(
            tipo=ctx.getText(),
            line=ctx.start.line,
        )

    # Visit a parse tree produced by CminusParser#param_lista.
    def visitParam_lista(self, ctx: CminusParser.Param_listaContext):
        if ctx.param_lista() is not None:
            return ListaParametros(
                listaParam=self.visit(ctx.param_lista()),
                param=self.visit(ctx.param()),
                line=ctx.start.line
            )
        return ListaParametros(
            listaParam=None,
            param=self.visit(ctx.param()),
            line=ctx.start.line
        )

    # Visit a parse tree produced by CminusParser#param.
    def visitParam(self, ctx: CminusParser.ParamContext):
        return Param(
            tipoEsp=self.visit(ctx.tipo_especificador()),
            id_=ctx.ID().getText(),
            flagVet=True if ctx.LSBRACKET() else False,
            line=ctx.start.line,
        )

    # Visit a parse tree produced by CminusParser#composto_decl.
    def visitComposto_decl(self, ctx: CminusParser.Composto_declContext):
        return CompDecl(
            localDecl=[self.visit(decl) for decl in ctx.l_decl] if ctx.local_declaracoes() else [],
            stmLista=[self.visit(stm) for stm in ctx.stm_list] if ctx.statement_lista() else [],
            line=ctx.start.line,
        )

    # Visit a parse tree produced by CminusParser#local_declaracoes.
    def visitLocal_declaracoes(self, ctx: CminusParser.Local_declaracoesContext):
        return LocalDeclaracoes(
            varDecl=[self.visit(decl) for decl in ctx.var_decl],
            line=ctx.start.line,
        )

    # Visit a parse tree produced by CminusParser#statement_lista.
    def visitStatement_lista(self, ctx: CminusParser.Statement_listaContext):
        return StatementLista(
            stm=[self.visit(stm) for stm in ctx.stms],
            line=ctx.start.line,
        )

    # Visit a parse tree produced by CminusParser#statement.
    def visitStatement(self, ctx: CminusParser.StatementContext):
        if ctx.expressao_decl():
            return Stm(child=self.visit(ctx.expressao_decl()),
                       line=ctx.start.line,
                       )
        elif ctx.composto_decl():
            return Stm(child=self.visit(ctx.composto_decl()),
                       line=ctx.start.line, )
        elif ctx.selecao_decl():
            return Stm(child=self.visit(ctx.selecao_decl()),
                       line=ctx.start.line, )
        elif ctx.iteracao_decl():
            return Stm(child=self.visit(ctx.iteracao_decl()),
                       line=ctx.start.line, )
        elif ctx.retorno_decl():
            return Stm(child=self.visit(ctx.retorno_decl()),
                       line=ctx.start.line, )

    # Visit a parse tree produced by CminusParser#expressao_decl.
    def visitExpressao_decl(self, ctx: CminusParser.Expressao_declContext):
        return ExpressaoDecl(
            exp=self.visit(ctx.expressao()) if ctx.expressao() is not None else None,
            line=ctx.start.line,
        )

    # Visit a parse tree produced by CminusParser#selecao_decl.
    def visitSelecao_decl(self, ctx: CminusParser.Selecao_declContext):
        if ctx.corpoElse is not None:
            return IfDecl(
                condicao=self.visit(ctx.condicao),
                corpoIf=[self.visit(cif) for cif in ctx.corpoIF],
                corpoElse=[self.visit(cel) for cel in ctx.corpoElse],
                line=ctx.start.line,
            )
        return IfDecl(
            condicao=self.visit(ctx.expressao()),
            corpoIf=[self.visit(cif) for cif in ctx.corpoIF],
            corpoElse=[],
            line=ctx.start.line,
        )

    # Visit a parse tree produced by CminusParser#iteracao_decl.
    def visitIteracao_decl(self, ctx: CminusParser.Iteracao_declContext):
        return WhileDecl(
            condicao=self.visit(ctx.expressao()),
            corpo=self.visit(ctx.statement()),
            line=ctx.start.line,
        )

    # Visit a parse tree produced by CminusParser#retorno_decl.
    def visitRetorno_decl(self, ctx: CminusParser.Retorno_declContext):
        if ctx.expressao() is not None:
            return ReturnDecl(
                expressao=self.visit(ctx.expressao()),
                line=ctx.start.line,
            )
        return ReturnDecl(
            expressao=None,
            line=ctx.start.line,
        )

    # Visit a parse tree produced by CminusParser#expressao.
    def visitExpressao(self, ctx: CminusParser.ExpressaoContext):
        if ctx.simples_expressao() is not None:
            return Express(
                var=None,
                expressao=None,
                simplesExpressao=self.visit(ctx.simples_expressao()),
                line=ctx.start.line,
            )
        return Express(
            var=self.visit(ctx.var()),
            expressao=self.visit(ctx.expressao()),
            simplesExpressao=None,
            line=ctx.start.line,
        )

    # Visit a parse tree produced by CminusParser#var.
    def visitVar(self, ctx: CminusParser.VarContext):
        if ctx.expressao() is not None:
            return Variavel(
                id_=ctx.ID().getText(),
                expressao=self.visit(ctx.expressao()),
                line=ctx.start.line,
            )
        return Variavel(
            id_=ctx.ID().getText(),
            line=ctx.start.line,
        )

    # Visit a parse tree produced by CminusParser#simples_expressao.
    def visitSimples_expressao(self, ctx: CminusParser.Simples_expressaoContext):
        return Comp(
            esq=self.visit(ctx.esquerda) if ctx.esquerda else None,
            relacional=ctx.relacional.text if ctx.relacional else None,
            dir=self.visit(ctx.direita) if ctx.direita else None,
            operacao=self.visit(ctx.operacao) if ctx.operacao else None,
            line=ctx.start.line,
        )

        # Visit a parse tree produced by CminusParser#soma_expressao.

    def visitSoma_expressao(self, ctx: CminusParser.Soma_expressaoContext):
        return Operacao(
            esq=self.visit(ctx.soma_expressao()) if ctx.soma_expressao() else None,
            op=ctx.op.text if ctx.op else None,
            dir=self.visit(ctx.termo()) if ctx.termo() else None,
            line=ctx.start.line,
        )

    # Visit a parse tree produced by CminusParser#termo.
    def visitTermo(self, ctx: CminusParser.TermoContext):
        return Operacao(
            esq=self.visit(ctx.termo()) if ctx.termo() else None,
            op=ctx.op.text if ctx.op else None,
            dir=self.visit(ctx.fator()) if ctx.fator() else None,
            line=ctx.start.line,
        )

    # Visit a parse tree produced by CminusParser#fator.
    def visitFator(self, ctx: CminusParser.FatorContext):
        return fat(
            num=ctx.NUM().getText() if ctx.NUM() else None,
            variavel=self.visit(ctx.var()) if ctx.var() else None,
            ativacao=self.visit(ctx.ativacao()) if ctx.ativacao() else None,
            expressao=self.visit(ctx.expressao()) if ctx.expressao() else None,
            line=ctx.start.line,
        )

    # Visit a parse tree produced by CminusParser#ativacao.
    def visitAtivacao(self, ctx: CminusParser.AtivacaoContext):
        return Ativ(
            id_=ctx.ID().getText(),
            argLista=[self.visit(args) for args in ctx.arg_list] if ctx.expressao() is not None else None,
            line=ctx.start.line,
        )


class AstVisitor:
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))


