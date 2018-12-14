class AstNumber:
    def __init__(self, line=-1):
        self.line = line


class Program(AstNumber):
    def __init__(self, decl_list, line=-1):
        super().__init__(line)
        self.declList = decl_list


class Decl(AstNumber):
    def __init__(self, var_decl, fun_decl, line=-1):
        super().__init__(line)
        self.varDecl = var_decl
        self.funDecl = fun_decl


class VarDecl(AstNumber):
    def __init__(self, type_, id_, num=None, line=-1):
        super().__init__(line)
        self.type = type_
        self.id_ = id_
        self.num = num


class TypeSpec(AstNumber):
    def __init__(self, type_spec, line=-1):
        super().__init__(line)
        self.typeSpec = type_spec


class FunDecl(AstNumber):
    def __init__(self, type_spec, id_, params, decl_comp, line=-1):
        super().__init__(line)
        self.typeSpec = type_spec
        self.id_ = id_
        self.params = params
        self.declComp = decl_comp


class Params(AstNumber):
    def __init__(self, param_list=None, type_=None, line=-1):
        super().__init__(line)
        self.paramList = param_list
        self.type = type_


class ParamList(AstNumber):
    def __init__(self, param_list, param, line=-1):
        super().__init__(line)
        self.paramList = param_list
        self.param = param


class Param(AstNumber):
    def __init__(self, type_spec, id_, flag_vet=None, line=-1):
        super().__init__(line)
        self.typeSpec = type_spec
        self.id_ = id_
        self.flagVet = flag_vet


class CompDecl(AstNumber):
    def __init__(self, local_decl, stm_list, line=-1):
        super().__init__(line)
        self.localDecl = local_decl
        self.stmList = stm_list


class LocalDeclarations(AstNumber):
    def __init__(self, var_decl, line=-1):
        super().__init__(line)
        self.varDecl = var_decl


class StatementList(AstNumber):
    def __init__(self, stm, line=-1):
        super().__init__(line)
        self.stm = stm


class Stm(AstNumber):
    def __init__(self, child, line=-1):
        super().__init__(line)
        self.child = child


class ExpressionoDecl(AstNumber):
    def __init__(self, exp, line=-1):
        super().__init__(line)
        self.exp = exp


class IfDecl(AstNumber):
    def __init__(self, condition, body_if, body_else=None, line=-1):
        super().__init__(line)
        self.condition = condition
        self.bodyIf = body_if
        self.bodyElse = body_else


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
    def __init__(self, var, expression, simple_expression, line=-1):
        super().__init__(line)
        self.var = var
        self.expression = expression
        self.simplesExpression = simple_expression


class Variable(AstNumber):
    def __init__(self, id_, expression=None, line=-1):
        super().__init__(line)
        self.id_ = id_
        self.expression = expression


class Comp(AstNumber):
    def __init__(self, left, relational, right, operation=None, line=-1):
        super().__init__(line)
        self.left = left
        self.relational = relational
        self.right = right
        self.operation = operation


class Operation(AstNumber):
    def __init__(self, left, op, right, line=-1):
        super().__init__(line)
        self.left = left
        self.op = op
        self.right = right


class Call(AstNumber):
    def __init__(self, id_, arg_list=None, line=-1):
        super().__init__(line)
        self.id_ = id_
        self.argList = arg_list


class Factor(AstNumber):
    def __init__(self, num, variable, call, expression, line=-1):
        super().__init__(line)
        self.num = num
        self.variable = variable
        self.call = call
        self.expression = expression