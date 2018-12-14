from gen.CminusParser import CminusParser
from gen.CminusVisitor import CminusVisitor


class AstNumber:
    def __init__(self, line=-1):
        self.line = line


class Program(AstNumber):
    def __init__(self, decl_list, line=-1):
        super().__init__(line)
        self.decl_list = decl_list


class Decl(AstNumber):
    def __init__(self, varDecl, funDecl, line=-1):
        super().__init__(line)
        self.varDecl = varDecl
        self.funDecl = funDecl


class VarDecl(AstNumber):
    def __init__(self, type, id_, num=None, line=-1):
        super().__init__(line)
        self.type = type
        self.id_ = id_
        self.num = num


class TypeSp(AstNumber):
    def __init__(self, typeS_, line=-1):
        super().__init__(line)
        self.typeS = typeS_


class FunDecl(AstNumber):
    def __init__(self, typeS, id_, params, compStatement, line=-1):
        super().__init__(line)
        self.typeS = typeS
        self.id_ = id_
        self.params = params
        self.compStatement = compStatement


class Params(AstNumber):
    def __init__(self, paramList=None, type=None, line=-1):
        super().__init__(line)
        self.paramList = paramList
        self.type = type


class ParamList(AstNumber):
    def __init__(self, paramList, param, line=-1):
        super().__init__(line)
        self.paramList = paramList
        self.param = param


class Param(AstNumber):
    def __init__(self, typeSp, id_, flagVet=None, line=-1):
        super().__init__(line)
        self.typeSp = typeSp
        self.id_ = id_
        self.flagVet = flagVet


class CompStm(AstNumber):
    def __init__(self, localDecl, stmList, line=-1):
        super().__init__(line)
        self.localDecl = localDecl
        self.stmList = stmList


class LocalDeclarations(AstNumber):
    def __init__(self, varDecl, line=-1):
        super().__init__(line)
        self.varDecl = varDecl


class StatementList(AstNumber):
    def __init__(self, stm, line=-1):
        super().__init__(line)
        self.stm = stm


class Stm(AstNumber):
    def __init__(self, child, line=-1):
        super().__init__(line)
        self.child = child


class ExpressionStm(AstNumber):
    def __init__(self, exp, line=-1):
        super().__init__(line)
        self.exp = exp


class IfDecl(AstNumber):
    def __init__(self, condition, bodyIf, bodyElse=None, line=-1):
        super().__init__(line)
        self.condition = condition
        self.bodyIf = bodyIf
        self.bodyElse = bodyElse


class WhileDecl(AstNumber):
    def __init__(self, condition, body, line=-1):
        super().__init__(line)
        self.condition = condition
        self.body = body


class ReturnDecl(AstNumber):
    def __init__(self, expression=None, line=-1):
        super().__init__(line)
        self.expression = expression


class Express(AstNumber):
    def __init__(self, var, expression, simpleExpression, line=-1):
        super().__init__(line)
        self.var = var
        self.expression = expression
        self.simplesExpression = simpleExpression


class Var(AstNumber):
    def __init__(self, id_, expression=None, line=-1):
        super().__init__(line)
        self.id_ = id_
        self.expression = expression


class Comp(AstNumber):
    def __init__(self, left, relational, right, op=None, line=-1):
        super().__init__(line)
        self.left = left
        self.relational = relational
        self.right = right
        self.op = op


class Oper(AstNumber):
    def __init__(self, left, op, right, line=-1):
        super().__init__(line)
        self.left = left
        self.op = op
        self.right = right


class Call(AstNumber):
    def __init__(self, id_, argList=None, line=-1):
        super().__init__(line)
        self.id_ = id_;
        self.argList = argList


class Factor(AstNumber):
    def __init__(self, num, variable, call, expression, line=-1):
        super().__init__(line)
        self.num = num
        self.variable = variable
        self.call = call
        self.expression = expression


class CreateAst(CminusVisitor):
    # Visit a parse tree produced by CminusParser#programa.
    def visitProgram(self, ctx: CminusParser.ProgramContext):
        return Program(
            decl_list=[self.visit(decls) for decls in ctx.declaration_list()],
            line=ctx.start.line,
        )

    # Visit a parse tree produced by CminusParser#declaracao_lista.
    def visitDeclaration(self, ctx: CminusParser.DeclarationContext):
        return Decl(
            varDecl=self.visit(ctx.var_declaration()) if ctx.var_declaration() is not None else None,
            funDecl=self.visit(ctx.fun_declaration()) if ctx.fun_declaration() is not None else None,
            line=ctx.start.line,
        )

    # Visit a parse tree produced by CminusParser#var_declaracao.
    def visitVar_declaration(self, ctx: CminusParser.Var_declarationContext):
        if ctx.NUMBER() is not None:
            return VarDecl(
                type=(self.visit(ctx.type_specifier())),
                id_=ctx.ID().getText(),
                num=ctx.NUMBER().getText(),
                line=ctx.start.line,
            )
        return VarDecl(
            type=self.visit(ctx.type_specifier()),
            id_=ctx.ID().getText(),
            line=ctx.start.line,
        )

    # Visit a parse tree produced by CminusParser#type_specifier.
    def visitType_specifier(self, ctx: CminusParser.Type_specifierContext):
        return TypeSp(
            typeS_=ctx.getText(),
            line=ctx.start.line,
        )

    # Visit a parse tree produced by CminusParser#fun_declaracao.
    def visitFun_declaration(self, ctx: CminusParser.Fun_declarationContext):
        return FunDecl(
            typeS=self.visit(ctx.type_specifier()),
            id_=ctx.ID().getText(),
            params=self.visit(ctx.params()),
            compStatement=self.visit(ctx.compound_statement()),
            line=ctx.start.line,
        )

    # Visit a parse tree produced by CminusParser#params.
    def visitParams(self, ctx: CminusParser.ParamsContext):
        if ctx.param_list() is not None:
            return Params(
                paramList=self.visit(ctx.param_list()),
                line=ctx.start.line,
            )
        return Params(
            type=ctx.getText(),
            line=ctx.start.line,
        )

    # Visit a parse tree produced by CminusParser#param_lista.
    def visitParam_list(self, ctx: CminusParser.Param_listContext):
        if ctx.param_list() is not None:
            return ParamList(
                paramList=self.visit(ctx.param_list()),
                param=self.visit(ctx.param()),
                line=ctx.start.line
            )
        return ParamList(
            paramList=None,
            param=self.visit(ctx.param()),
            line=ctx.start.line
        )

    # Visit a parse tree produced by CminusParser#param.
    def visitParam(self, ctx: CminusParser.ParamContext):
        return Param(
            typeSp=self.visit(ctx.type_specifier()),
            id_=ctx.ID().getText(),
            flagVet=True if ctx.LBRACK() else False,
            line=ctx.start.line,
        )

    # Visit a parse tree produced by CminusParser#compound_statement.
    def visitCompound_statement(self, ctx: CminusParser.Compound_statementContext):
        return CompStm(
            localDecl=[self.visit(decl) for decl in ctx.local_declarations()] if ctx.local_declarations() else [],
            stmList=[self.visit(stm) for stm in ctx.statement_list()] if ctx.statement_list() else [],
            line=ctx.start.line,
        )

    # Visit a parse tree produced by CminusParser#local_declarations.
    def visitLocal_declarations(self, ctx: CminusParser.Local_declarationsContext):
        return LocalDeclarations(
            varDecl=[self.visit(decl) for decl in ctx.var_declaration()],
            line=ctx.start.line,
        )

    # Visit a parse tree produced by CminusParser#statement_lista.
    def visitStatement_list(self, ctx: CminusParser.Statement_listContext):
        return StatementList(
            stm=[self.visit(stm) for stm in ctx.statement()],
            line=ctx.start.line,
        )

    # Visit a parse tree produced by CminusParser#statement.
    def visitStatement(self, ctx: CminusParser.StatementContext):
        if ctx.expression_statement():
            return Stm(child=self.visit(ctx.expression_statement()),
                       line=ctx.start.line,
                       )
        elif ctx.compound_statement():
            return Stm(child=self.visit(ctx.compound_statement()),
                       line=ctx.start.line, )
        elif ctx.selection_statement():
            return Stm(child=self.visit(ctx.selection_statement()),
                       line=ctx.start.line, )
        elif ctx.iteration_statement():
            return Stm(child=self.visit(ctx.iteration_statement()),
                       line=ctx.start.line, )
        elif ctx.return_statemet():
            return Stm(child=self.visit(ctx.return_statemet()),
                       line=ctx.start.line, )

    # Visit a parse tree produced by CminusParser#expression_statement.
    def visitExpression_statement(self, ctx: CminusParser.Expression_statementContext):
        return ExpressionStm(
            exp=self.visit(ctx.expression()) if ctx.expression() is not None else None,
            line=ctx.start.line,
        )

    # Visit a parse tree produced by CminusParser#selection_statement.
    def visitSelection_statement(self, ctx: CminusParser.Selection_statementContext):
        if ctx.ELSE is not None:
            return IfDecl(
                condition=self.visit(ctx.expression),
                bodyIf=[self.visit(cif) for cif in ctx.IF()],
                bodyElse=[self.visit(cel) for cel in ctx.ELSE()],
                line=ctx.start.line,
            )
        return IfDecl(
            condition=self.visit(ctx.expression()),
            bodyIf=[self.visit(cif) for cif in ctx.IF()],
            bodyElse=[],
            line=ctx.start.line,
        )

    # Visit a parse tree produced by CminusParser#iteration_statement.
    def visitIteration_statement(self, ctx: CminusParser.Iteration_statementContext):
        return WhileDecl(
            condition=self.visit(ctx.expression()),
            body=self.visit(ctx.statement()),
            line=ctx.start.line,
        )

    # Visit a parse tree produced by CminusParser#return_statemet.
    def visitReturn_statemet(self, ctx: CminusParser.Return_statemetContext):
        if ctx.expression() is not None:
            return ReturnDecl(
                expression=self.visit(ctx.expression()),
                line=ctx.start.line,
            )
        return ReturnDecl(
            expression=None,
            line=ctx.start.line,
        )

    # Visit a parse tree produced by CminusParser#expressao.
    def visitExpression(self, ctx: CminusParser.ExpressionContext):
        if ctx.simple_expression() is not None:
            return Express(
                var=None,
                expression=None,
                simpleExpression=self.visit(ctx.simple_expression()),
                line=ctx.start.line,
            )
        return Express(
            var=self.visit(ctx.var()),
            expression=self.visit(ctx.expression()),
            simpleExpression=None,
            line=ctx.start.line,
        )

    # Visit a parse tree produced by CminusParser#var.
    def visitVar(self, ctx: CminusParser.VarContext):
        if ctx.expression() is not None:
            return Var(
                id_=ctx.ID().getText(),
                expression=self.visit(ctx.expression()),
                line=ctx.start.line,
            )
        return Var(
            id_=ctx.ID().getText(),
            line=ctx.start.line,
        )

    # Visit a parse tree produced by CminusParser#simples_expressao.
    def visitSimple_expression(self, ctx: CminusParser.Simple_expressionContext):
        return Comp(
            left=self.visit(ctx.left) if ctx.left else None,
            relational=ctx.relop.text if ctx.relop else None,
            right=self.visit(ctx.right) if ctx.right else None,
            op=self.visit(ctx.operation) if ctx.operation else None,
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
            num=ctx.NUMBER().getText() if ctx.NUMBER() else None,
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

