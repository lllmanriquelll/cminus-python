from tabulate import tabulate
import CminusAST


class Symbol:
    def __init__(self, name, scope, line, id_type, canonical_type, pos_mem=-1, qtd_args='', args=''):
        self.name = name
        self.scope = scope
        self.lines = {line}
        self.id_type = id_type
        self.canonical_type = canonical_type
        self.pos_mem = pos_mem
        self.qtd_args = qtd_args
        self.args = args

    def as_tuple(self):
        return (self.name, self.scope, ', '.join(map(str, sorted(self.lines))), self.id_type,
                self.canonical_type, self.pos_mem, self.qtd_args, self.args)


class SemanticAnalysisTableG(CminusAST.AstVisitor):

    def __init__(self, ast_):
        self.table = {}
        self.errors = []
        self._scope = ''
        self.count_pos_mem = 0
        self.sys_call = ['input', 'output']
        self.visit(ast_)
        self.count_args = 0
        self.list_args = []

        if 'main' not in self.table:
            self.errors.append(f'No main function declared')

    def __str__(self):
        return tabulate(
            tabular_data=[(key,) + symbol.as_tuple() for key, symbol in self.table.items()],
            headers=['Key', 'Name', 'Scope', 'Lines', 'Id Type', 'Data Type', 'Pos Mem', 'Qtd Args', 'Args'],
            tablefmt='grid',
        )

    def scoped_name(self, name):
        if not self._scope:
            return name
        return f'{self._scope}.{name}'

    def visit_Program(self, no: CminusAST.Program):
        for decl in no.declList:
            self.visit(decl)

    def visit_Decl(self, no: CminusAST.Decl):
        if no.varDecl:
            self.visit(no.varDecl)
        elif no.funDecl:
            self.visit(no.funDecl)

    def visit_VarDecl(self, no: CminusAST.VarDecl):
        name = self.scoped_name(no.id_)
        if name in self.table:
            self.errors.append(f'{no.line}: Variable "{no.id_}" already declared')
            return False
        if no.id_ in self.table:
            self.errors.append(f'{no.line}: Variable "{no.id_}" shares name with a function')
        if no.type.typeSpec == 'void':
            self.errors.append(f'{no.line}: Void variable cannot be declared')

        if no.num:
            if self._scope == '':
                self.table[f'global.{name}'] = Symbol(no.id_, 'global', no.line, f'var[]', no.type.typeSpec, self.count_pos_mem)
                self.count_pos_mem += int(no.num)
            else:
                self.table[name] = Symbol(no.id_, self._scope, no.line, f'var[]', no.type.typeSpec, self.count_pos_mem)
                self.count_pos_mem += int(no.num)
        else:
            if self._scope == '':
                self.table[f'global.{name}'] = Symbol(no.id_, 'global', no.line, 'var', no.type.typeSpec, self.count_pos_mem)
                self.count_pos_mem += 1
            else:
                self.table[name] = Symbol(no.id_, self._scope, no.line, 'var', no.type.typeSpec, self.count_pos_mem)
                self.count_pos_mem += 1
        return True

    def visit_FunDecl(self, no: CminusAST.FunDecl):
        if no.id_ in self.table:
            self.errors.append(f'{no.line}: Function "{no.id_}" already declared')

        if self._scope == '':
            self.table[no.id_] = Symbol(no.id_, 'global', no.line, 'funct', no.typeSpec.typeSpec)
        else:
            self.table[no.id_] = Symbol(no.id_, self._scope, no.line, 'funct', no.typeSpec.typeSpec)

        self._scope = no.id_
        self.count_args = 0
        self.list_args = []
        self.visit(no.params)
        self.table[no.id_].qtd_args = self.count_args
        self.table[no.id_].args = self.list_args
        self.visit(no.declComp)
        self._scope = ''

    def visit_Params(self, no: CminusAST.Params):
        if no.paramList:
            self.visit(no.paramList)

    def visit_ParamList(self, no: CminusAST.ParamList):
        if no.paramList:
            self.visit(no.paramList)
            self.visit(no.param)
        else:
            self.visit(no.param)

    def visit_Param(self, no: CminusAST.Param):
        self.count_args += 1
        self.list_args.append(no.id_)
        name = self.scoped_name(no.id_)
        if name in self.table:
            self.errors.append(f'{no.line}: Variable "{no.id_}" already declared')
            return False
        if no.typeSpec.typeSpec == 'void':
            self.errors.append(f'{no.line}: Cannot declare void variable')

        if no.flagVet:
            self.table[name] = Symbol(no.id_, self._scope, no.line, 'var[]', no.typeSpec.typeSpec, self.count_pos_mem)
            self.count_pos_mem += 1
        else:
            self.table[name] = Symbol(no.id_, self._scope, no.line, 'var', no.typeSpec.typeSpec, self.count_pos_mem)
            self.count_pos_mem += 1

    def visit_CompDecl(self, no: CminusAST.CompDecl):
        if no.localDecl:
            for decl in no.localDecl:
                self.visit(decl)
        if no.stmList:
            for stm in no.stmList:
                self.visit(stm)

    def visit_LocalDeclarations(self, no: CminusAST.LocalDeclarations):
        for locD in no.varDecl:
            self.visit(locD)

    def visit_StatementList(self, no: CminusAST.StatementList):
        for stm in no.stm:
            self.visit(stm)

    def visit_Stm(self, no: CminusAST.Stm):
        if no.child:
            self.visit(no.child)

    def visit_ExpressionDecl(self, no: CminusAST.ExpressionDecl):
        if no.exp:
            self.visit(no.exp)

    def visit_IfDecl(self, no: CminusAST.IfDecl):
        self.visit(no.condition)
        if no.bodyElse:
            for ci in no.bodyIf:
                self.visit(ci)
            for ce in no.bodyElse:
                self.visit(ce)
        else:
            for ci in no.bodyIf:
                self.visit(ci)

    def visit_WhileDecl(self, no: CminusAST.WhileDecl):
        self.visit(no.condition)
        self.visit(no.body)

    def visit_ReturnDecl(self, no: CminusAST.ReturnDecl):
        if no.expression:
            self.visit(no.expression)

    def visit_Express(self, no: CminusAST.Express):
        if no.simpleExpression:
            self.visit(no.simpleExpression)
        else:
            self.visit(no.var)
            if no.expression.simpleExpression:
                if no.expression.simpleExpression.operation:
                    if no.expression.simpleExpression.operation.right:
                        if no.expression.simpleExpression.operation.right.right:
                            if no.expression.simpleExpression.operation.right.right.call:
                                func = no.expression.simpleExpression.operation.right.right.call.id_
                                if func in self.table:
                                    if self.table[func].canonical_type == 'void':
                                        self.errors.append(f'{no.line}: Invalid Assignment of Type "void"')
            self.visit(no.expression)


    def visit_Variable(self, no: CminusAST.Variable):
        name = self.scoped_name(no.id_)
        in_local_scope = name in self.table
        in_global_scope = f'global.{no.id_}' in self.table
        if in_local_scope:
            self.table[name].lines.add(no.line)
        elif in_global_scope:
            self.table[f'global.{no.id_}'].lines.add(no.line)

        else:
            self.errors.append(f'{no.line}: Variable "{no.id_}" used without previous declaration')
            return False
        return True

    def visit_Comp(self, no: CminusAST.Comp):
        if no.relational:
            self.visit(no.left)
            self.visit(no.right)
        else:
            self.visit(no.operation)

    def visit_Operation(self, no: CminusAST.Operation):
        if no.left:
            self.visit(no.left)
            self.visit(no.right)
        else:
            self.visit(no.right)

    def visit_Factor(self, no: CminusAST.Factor):
        if no.variable:
            self.visit(no.variable)
        elif no.call:
            self.visit(no.call)
        elif no.expression:
            self.visit(no.expression)

    def visit_Call(self, no: CminusAST.Call):
        name = no.id_
        in_global_scope = name in self.table
        if not in_global_scope:
            if name in self.sys_call:
                self.table[name] = Symbol(name, self._scope, no.line, 'sys_call', 'int')
            else:
                self.errors.append(f'{no.line}: Function "{no.id_}" used without declaration')
            return False
        self.table[name].lines.add(no.line)
        for arg in no.argList:
            self.visit(arg)

