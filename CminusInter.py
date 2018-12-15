from tabulate import tabulate
import CminusAST


class IntermedCode(CminusAST.AstVisitor):

    def __init__(self, ast_):
        self.intermediate = []
        self.line = -1
        self.temp = 0
        self.label = 0
        self.sys_call = ['input', 'output']
        self.visit(ast_)

    def __str__(self):
        return tabulate(tabular_data=[line for line in self.intermediate],
                        headers=['Instruction', 'param 1', 'param 2', 'param 3'],
                        tablefmt='grid')

    def visit_Program(self, no: CminusAST.Program):
        for decl in no.declList:
            if no.declList is not None:
                self.visit(decl)

    def visit_Decl(self, no: CminusAST.Decl):
        if no.varDecl is not None:
            self.visit(no.varDecl)
        elif no.funDecl is not None:
            self.visit(no.funDecl)

    def visit_VarDecl(self, no: CminusAST.VarDecl):

        return

    def visit_FunDecl(self, no: CminusAST.FunDecl):
        aux_list = ['function', no.id_, '', '']
        self.intermediate.append(aux_list)
        self.visit(no.params)
        self.visit(no.declComp)
        if no.id_ != 'main':
            self.intermediate.append(['return', '0', '', ''])

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
        return

    def visit_CompDecl(self, no: CminusAST.CompDecl):
        for decls in no.localDecl:
            self.visit(decls)
        for stms in no.stmList:
            self.visit(stms)

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
        cond = self.visit(no.condition)
        self.label += 1
        end_if = self.label
        self.label += 1
        end_else = self.label
        aux_list = ['jump_if_false', cond, f'L{end_if}', '']
        self.intermediate.append(aux_list)

        if no.bodyElse:
            for ci in no.bodyIf:
                self.visit(ci)

            aux_list = ['go_to', f'L{end_else}', '', '']
            self.intermediate.append(aux_list)

            aux_list = ['label', f'L{end_if}', '', '']
            self.intermediate.append(aux_list)
            for ce in no.bodyElse:
                self.visit(ce)
            aux_list = ['label', f'L{end_else}', '', '']
            self.intermediate.append(aux_list)

        else:
            for ci in no.bodyIf:
                self.visit(ci)
            aux_list = ['label', f'L{end_if}', '', '']
            self.intermediate.append(aux_list)


    def visit_WhileDecl(self, no: CminusAST.WhileDecl):
        self.label += 1
        label_start = self.label
        aux_list = ['label', f'L{label_start}', '', '']
        self.intermediate.append(aux_list)

        cond = self.visit(no.condition)
        self.label += 1
        label_end = self.label

        aux_list = ['jump_if_false', cond, f'L{label_end}', '']
        self.intermediate.append(aux_list)

        self.visit(no.body)
        aux_list = ['go_to', f'L{label_start}', '', '']
        self.intermediate.append(aux_list)

        aux_list = ['label', f'L{label_end}', '', '']
        self.intermediate.append(aux_list)


    def visit_ReturnDecl(self, no: CminusAST.ReturnDecl):
        if no.expression:
            x = self.visit(no.expression)
            aux_list = ['return', x, '', '']
            self.intermediate.append(aux_list)
        else:
            aux_list = ['return', '', '', '']
            self.intermediate.append(aux_list)

    def visit_Express(self, no: CminusAST.Express):
        if no.simpleExpression:
            return self.visit(no.simpleExpression)
        else:

            if no.var.expression:
                k = self.visit(no.var.expression)
                y = self.visit(no.expression)
                self.temp += 1
                aux_list = ['assign_end_vet', no.var.id_, k, f't{self.temp}']
                self.intermediate.append(aux_list)
                aux_list = ['assign', f't{self.temp}', y, '']
                self.intermediate.append(aux_list)
            else:
                x = self.visit(no.var)
                y = self.visit(no.expression)
                aux_list = ['assign', x, y, '']
                self.intermediate.append(aux_list)

    def visit_Variable(self, no: CminusAST.Variable):
        if no.expression:
            x = self.visit(no.expression)
            self.temp += 1
            aux_list = ['assign_vet', no.id_, x, f't{self.temp}']
            self.intermediate.append(aux_list)
            return f't{self.temp}'
        elif no.id_:
            return no.id_

    def visit_Comp(self, no: CminusAST.Comp):
        if no.operation:
            return self.visit(no.operation)
        else:
            x = self.visit(no.left)
            y = self.visit(no.right)
            
            self.temp += 1
            operation = ''
            if no.relational == '<=':
                operation = 'less_than_equal_to'
            elif no.relational == '>=':
                operation = 'greatest_than_equal_to'
            elif no.relational == '==':
                operation = 'equal_to'
            elif no.relational == '!=':
                operation = 'diferent_to'
            elif no.relational == '<':
                operation = 'less_than'
            elif no.relational == '>':
                operation = 'greatest_than'

            aux_list = [operation, x, y, f't{self.temp}']
            self.intermediate.append(aux_list)
            return f't{self.temp}'



    def visit_Operation(self, no: CminusAST.Operation):
        if no.left:
            x = self.visit(no.left)
            y = self.visit(no.right)

            self.temp += 1
            operation = ''
            if no.op == '+':
                operation = 'addition'
            elif no.op == '-':
                operation = 'subtraction'
            elif no.op == '/':
                operation = 'division'
            elif no.op == '*':
                operation = 'multiplication'

            aux_list = [operation, x, y, f't{self.temp}']
            self.intermediate.append(aux_list)
            return f't{self.temp}'

        else:
            return self.visit(no.right)


    def visit_Factor(self, no: CminusAST.Factor):
        if no.num:
            return no.num
        elif no.variable:
            return self.visit(no.variable)
        elif no.expression:
            return self.visit(no.expression)
        elif no.call:
            return self.visit(no.call)


    def visit_Call(self, no: CminusAST.Call):
        i = 0
        if no.argList:
            if no.id_ in self.sys_call:
                call = 'sys_call'
            else:
                call = 'function_call'
            aux_list = [call, f'{no.id_}']
            for arg in no.argList:
                i += 1
                temp = self.visit(arg)
                self.intermediate.append(['arg', temp, '', ''])
            aux_list.append(i)
            aux_list.append('')
            self.intermediate.append(aux_list)
            self.temp += 1
            if no.id_ != 'output':
                aux_list = ['assign_ret', f't{self.temp}', 'RT', '']
                self.intermediate.append(aux_list)
                return f't{self.temp}'
        elif no.id_:
            if no.id_ in self.sys_call:
                call = 'sys_call'
            else:
                call = 'function_call'
            self.temp += 1
            aux_list = [call, f'{no.id_}', '', '']
            self.intermediate.append(aux_list)
            aux_list = ['assign_ret', f't{self.temp}', 'RT', '']
            self.intermediate.append(aux_list)
            return f't{self.temp}'
