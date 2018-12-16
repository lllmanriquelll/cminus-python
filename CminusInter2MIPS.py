from tabulate import tabulate
from CminusInter import IntermedCode
from CminusTable import SemanticAnalysisTableG
import re


class IntermediateToMIPS:

    def __init__(self, semantic: SemanticAnalysisTableG, intermediate: IntermedCode):
        self.assembly = []
        self.semantic = semantic
        self.semantic_table = semantic.table
        self.intermediate = intermediate
        self.stack_register = []
        self.stack_args = []
        self.stack_vars = []
        self.temp_to_register = {}
        self.status_reg = []
        self.inicialize_reg_list()
        self.scope = 'global'
        self.convertToAssembly()

    def __str__(self):
        return tabulate(tabular_data=[row for row in self.assembly],
                        tablefmt="plain")

    def convertToAssembly(self):
        self.assembly.append(['li', '$s0', '0'])
        self.assembly.append(['li', '$sp', '0'])
        self.assembly.append(['li', '$ra', '0'])
        self.assembly.append(['j', 'main'])
        for inter in self.intermediate.intermediate:

            if inter[0] == 'function':
                self.assembly.append([f'{inter[1]}:'])
                self.scope = inter[1]
                lista_args = self.semantic_table[inter[1]].args
                for i in range(0, self.get_qtd_args_function(inter[1])):
                    type = self.search_type(lista_args[i])
                    RD = self.ret_reg_free()

                    if type == 'var':
                        pos_men = self.get_mem_pos(lista_args[i])
                        self.assembly.append(['subi', f'$sp', '$sp', '1'])
                        self.assembly.append(['pop', f'${RD}', '$sp'])
                        self.assembly.append(['li', f'$rl', pos_men])
                        self.assembly.append(['sw', f'${RD}', f'$rl'])
                    self.free_reg(RD)

            if inter[0] == 'label':
                self.assembly.append([f'{inter[1]}.'])

            if inter[0] == 'equal_to':
                line = self.operation_instructions(inter)
                line[0] = 'eq'
                self.assembly.append(line)

            if inter[0] == 'less_than_equal_to':
                line = self.operation_instructions(inter)
                line[0] = 'nab'
                self.assembly.append(line)

            if inter[0] == 'greatest_than_equal_to':
                line = self.operation_instructions(inter)
                line[0] = 'nlt'
                self.assembly.append(line)

            if inter[0] == 'diferent_to':
                line = self.operation_instructions(inter)
                line[0] = 'neq'
                self.assembly.append(line)

            if inter[0] == 'less_than':
                line = self.operation_instructions(inter)
                line[0] = 'lt'
                self.assembly.append(line)

            if inter[0] == 'greatest_than':
                line = self.operation_instructions(inter)
                line[0] = 'abv'
                self.assembly.append(line)

            if inter[0] == 'jump_if_false':
                type1 = self.search_type(inter[1])
                RS = self.ret_reg_free()
                if type1 == 'var':
                    pos_men = self.get_mem_pos(inter[1])
                    self.assembly.append(['li', f'$rl', pos_men])
                    self.assembly.append(['lw', f'${RS}', '$rl'])
                elif type1 == 'imt':
                    self.assembly.append(['li', f'${RS}', inter[1]])
                elif type1 == 'temp':
                    if inter[1] in self.temp_to_register:
                        self.free_reg(RS)
                        RS = self.temp_to_register[inter[1]]
                self.assembly.append(['jalr', f'$t0', f'${RS}', inter[2]])
                self.free_reg(RS)
                self.temp_to_register[inter[1]] = -1

            if inter[0] == 'addition':
                line = self.operation_instructions(inter)
                line[0] = 'add'
                self.assembly.append(line)

            if inter[0] == 'subtraction':
                line = self.operation_instructions(inter)
                line[0] = 'sub'
                self.assembly.append(line)

            if inter[0] == 'division':
                line = self.operation_instructions(inter)
                line[0] = 'div'
                self.assembly.append(line)

            if inter[0] == 'multiplication':
                line = self.operation_instructions(inter)
                line[0] = 'mult'
                self.assembly.append(line)

            if inter[0] == 'assign':
                type1 = self.search_type(inter[1])
                RS = self.ret_reg_free()

                if type1 == 'var':
                    pos_men = self.get_mem_pos(inter[1])
                    self.assembly.append(['li', f'${RS}', pos_men])
                elif type1 == 'imt':
                    self.assembly.append(['li', f'${RS}', inter[1]])
                elif type1 == 'temp':
                    if inter[1] in self.temp_to_register:
                        self.free_reg(RS)
                        RS = self.temp_to_register[inter[1]]

                type2 = self.search_type(inter[2])
                RD = self.ret_reg_free()

                if type2 == 'var':
                    pos_men = self.get_mem_pos(inter[2])
                    self.assembly.append(['li', f'$rl', pos_men])
                    self.assembly.append(['lw', f'${RD}', f'$rl'])
                elif type2 == 'imt':
                    self.assembly.append(['li',  f'${RD}', inter[2]])
                elif type2 == 'temp':
                    if inter[2] in self.temp_to_register:
                        self.free_reg(RD)
                        RD = self.temp_to_register[inter[2]]

                self.assembly.append(['sw', f'${RD}', f'${RS}'])
                self.free_reg(RS)
                self.temp_to_register[inter[1]] = -1
                self.free_reg(RD)
                self.temp_to_register[inter[2]] = -1

            if inter[0] == 'return':
                type1 = self.search_type(inter[1])
                RS = self.ret_reg_free()

                if type1 == 'var':
                    pos_men = self.get_mem_pos(inter[1])
                    self.assembly.append(['li', f'${RS}', pos_men])
                    self.assembly.append(['lw', f'$rt', f'${RS}'])
                elif type1 == 'imt':
                    self.assembly.append(['li', f'$rt', inter[1]])
                elif type1 == 'temp':
                    if inter[1] in self.temp_to_register:
                        self.free_reg(RS)
                        RS = self.temp_to_register[inter[1]]
                        self.assembly.append(['move', f'$rt', f'${RS}'])
                self.assembly.append(['jmp', f'$ra'])
                self.free_reg(RS)
                self.temp_to_register[inter[1]] = -1
                self.free_all_reg()

            if inter[0] == 'function_call':
                self.push_temp_ocuped_in_stack()
                if inter[1] == self.scope:
                    self.push_vars_in_scope()
                for i in range(0, inter[2]):
                    arg = self.stack_args.pop()
                    type1 = self.search_type(arg[1])
                    RS = self.ret_reg_free()

                    if type1 == 'var':
                        pos_men = self.get_mem_pos(arg[1])
                        if self.is_a_vet(arg[1]):
                            if self.is_a_parameter(arg[1]):
                                self.assembly.append(['li', f'$rl', pos_men])
                                self.assembly.append(['lw', f'${RS}', f'$rl'])
                            else:
                                self.assembly.append(['li', f'${RS}', pos_men])
                        else:
                            self.assembly.append(['li', f'$rl', pos_men])
                            self.assembly.append(['lw', f'${RS}', f'$rl'])
                    elif type1 == 'imt':
                        self.assembly.append(['li', f'${RS}', arg[1]])
                    elif type1 == 'temp':
                        if arg[1] in self.temp_to_register:
                            self.free_reg(RS)
                            RS = self.temp_to_register[arg[1]]

                    self.assembly.append(['push', f'${RS}', '$sp'])
                    self.assembly.append(['addi', f'$sp', '$sp', '1'])

                    self.free_reg(RS)
                    self.temp_to_register[inter[1]] = -1

                self.assembly.append(['jal', inter[1]])
                if inter[1] == self.scope:
                    self.pop_vars_in_scope()
                self.pop_temp_ocuped_in_stack()

            if inter[0] == 'arg':
                self.stack_args.append(inter)

            if inter[0] == 'assign_ret':
                if self.search_type(inter[1]) == 'temp':
                    self.temp_to_register[inter[1]] = self.ret_reg_free()
                    RD = self.temp_to_register[inter[1]]
                self.assembly.append(['move', f'${RD}', f'$rt'])

            if inter[0] == 'sys_call':
                if inter[1] == 'input':
                    self.assembly.append(['in', f'$rt'])
                if inter[1] == 'output':
                    arg = self.stack_args.pop()
                    type1 = self.search_type(arg[1])
                    RS = self.ret_reg_free()

                    if type1 == 'var':
                        pos_men = self.get_mem_pos(arg[1])
                        self.assembly.append(['li', f'$rl', pos_men])
                        self.assembly.append(['lw', f'${RS}', f'$rl'])
                    elif type1 == 'imt':
                        self.assembly.append(['li', f'${RS}', arg[1]])
                    elif type1 == 'temp':
                        if arg[1] in self.temp_to_register:
                            self.free_reg(RS)
                            RS = self.temp_to_register[arg[1]]
                    self.assembly.append(['out', f'${RS}'])
                    self.free_reg(RS)
                    self.temp_to_register[arg[1]] = -1

            if inter[0] == 'go_to':
                self.assembly.append(['j', f'{inter[1]}'])

            if inter[0] == 'assign_end_vet':
                if self.is_a_parameter(inter[1]):
                    type1 = self.search_type(inter[1])
                    RS = self.ret_reg_free()

                    if type1 == 'var':
                        pos_men = self.get_mem_pos(inter[1])
                        self.assembly.append(['li', f'$rl', pos_men])
                        self.assembly.append(['lw', f'${RS}', '$rl'])

                    type2 = self.search_type(inter[2])
                    RD = self.ret_reg_free()

                    if type2 == 'var':
                        pos_men = self.get_mem_pos(inter[2])
                        self.assembly.append(['li', f'$rl', pos_men])
                        self.assembly.append(['lw', f'${RD}', f'$rl'])
                    elif type2 == 'imt':
                        self.assembly.append(['li', f'${RD}', inter[2]])
                    elif type2 == 'temp':
                        if inter[2] in self.temp_to_register:
                            self.free_reg(RD)
                            RD = self.temp_to_register[inter[2]]

                    if self.search_type(inter[3]) == 'temp':
                        self.temp_to_register[inter[3]] = self.ret_reg_free()
                        RT = self.temp_to_register[inter[3]]

                    self.assembly.append(['add', f'${RT}', f'${RS}', f'${RD}'])
                    self.free_reg(RS)
                    self.temp_to_register[inter[1]] = -1
                    self.free_reg(RD)
                    self.temp_to_register[inter[2]] = -1
                else:
                    type1 = self.search_type(inter[1])
                    RS = self.ret_reg_free()

                    if type1 == 'var':
                        pos_men = self.get_mem_pos(inter[1])
                        self.assembly.append(['li', f'${RS}', pos_men])

                    type2 = self.search_type(inter[2])
                    RD = self.ret_reg_free()

                    if type2 == 'var':
                        pos_men = self.get_mem_pos(inter[2])
                        self.assembly.append(['li', f'$rl', pos_men])
                        self.assembly.append(['lw', f'${RD}', f'$rl'])
                    elif type2 == 'imt':
                        self.assembly.append(['li', f'${RD}', inter[2]])
                    elif type2 == 'temp':
                        if inter[2] in self.temp_to_register:
                            self.free_reg(RD)
                            RD = self.temp_to_register[inter[2]]

                    if self.search_type(inter[3]) == 'temp':
                        self.temp_to_register[inter[3]] = self.ret_reg_free()
                        RT = self.temp_to_register[inter[3]]

                    self.assembly.append(['add', f'${RT}', f'${RS}', f'${RD}'])
                    self.free_reg(RS)
                    self.temp_to_register[inter[1]] = -1
                    self.free_reg(RD)
                    self.temp_to_register[inter[2]] = -1

            if inter[0] == 'assign_vet':
                if self.is_a_parameter(inter[1]):
                    type1 = self.search_type(inter[1])
                    RS = self.ret_reg_free()

                    if type1 == 'var':
                        pos_men = self.get_mem_pos(inter[1])
                        self.assembly.append(['li', f'$rl', pos_men])
                        self.assembly.append(['lw', f'${RS}', '$rl'])

                    type2 = self.search_type(inter[2])
                    RD = self.ret_reg_free()

                    if type2 == 'var':
                        pos_men = self.get_mem_pos(inter[2])
                        self.assembly.append(['li', f'$rl', pos_men])
                        self.assembly.append(['lw', f'${RD}', f'$rl'])
                    elif type2 == 'imt':
                        self.assembly.append(['li', f'${RD}', inter[2]])
                    elif type2 == 'temp':
                        if inter[2] in self.temp_to_register:
                            self.free_reg(RD)
                            RD = self.temp_to_register[inter[2]]

                    if self.search_type(inter[3]) == 'temp':
                        self.temp_to_register[inter[3]] = self.ret_reg_free()
                        RT = self.temp_to_register[inter[3]]
                    rd = self.ret_reg_free()
                    self.assembly.append(['add', f'${rd}', f'${RS}', f'${RD}'])
                    self.assembly.append(['lw', f'${RT}', f'${rd}'])
                    self.free_reg(rd)
                    self.free_reg(RS)
                    self.temp_to_register[inter[1]] = -1
                    self.free_reg(RD)
                    self.temp_to_register[inter[2]] = -1
                else:
                    type1 = self.search_type(inter[1])
                    RS = self.ret_reg_free()

                    if type1 == 'var':
                        pos_men = self.get_mem_pos(inter[1])
                        self.assembly.append(['li', f'${RS}', pos_men])

                    type2 = self.search_type(inter[2])
                    RD = self.ret_reg_free()

                    if type2 == 'var':
                        pos_men = self.get_mem_pos(inter[2])
                        self.assembly.append(['li', f'$rl', pos_men])
                        self.assembly.append(['lw', f'${RD}', f'$rl'])
                    elif type2 == 'imt':
                        self.assembly.append(['li', f'${RD}', inter[2]])
                    elif type2 == 'temp':
                        if inter[2] in self.temp_to_register:
                            self.free_reg(RD)
                            RD = self.temp_to_register[inter[2]]

                    if self.search_type(inter[3]) == 'temp':
                        self.temp_to_register[inter[3]] = self.ret_reg_free()
                        RT = self.temp_to_register[inter[3]]
                    rd = self.ret_reg_free()
                    self.assembly.append(['add', f'${rd}', f'${RS}', f'${RD}'])
                    self.assembly.append(['lw', f'${RT}', f'${rd}'])
                    self.free_reg(rd)
                    self.free_reg(RS)
                    self.temp_to_register[inter[1]] = -1
                    self.free_reg(RD)
                    self.temp_to_register[inter[2]] = -1

    def is_a_vet(self, vet):
        name = f'{self.scope}.{vet}'
        if name in self.semantic_table:
            if self.semantic_table[name].id_type == 'var[]':
                return True
        name = f'global.{vet}'
        if name in self.semantic_table:
            if self.semantic_table[name].id_type == 'var[]':
                return True
        return False

    def is_a_parameter(self, var):
        if self.scope in self.semantic_table:
            parameters = self.semantic_table[self.scope].args
            if var in parameters:
                return True
        return False

    def is_a_arg(self, name):
        for arg in self.stack_args:
            type1 = self.search_type(arg[1])
            if type1 == 'temp':
                if arg[1] in self.temp_to_register:
                    RS = self.temp_to_register[arg[1]]
                    if name == RS:
                        return True
        return False

    def push_vars_in_scope(self):
        for key in self.semantic_table:
            if re.match(f'{self.scope}.[a-zA-Z]', key):
                RS = self.ret_reg_free()
                pos_men = self.get_mem_pos(self.semantic_table[key].name)
                self.stack_vars.append(self.semantic_table[key].name)
                self.assembly.append(['li', f'$rl', pos_men])
                self.assembly.append(['lw', f'${RS}', f'$rl'])
                self.assembly.append(['push', f'${RS}', f'$sp'])
                self.assembly.append(['addi', f'$sp', '$sp', '1'])
                self.free_reg(RS)

    def pop_vars_in_scope(self):
        for i in range(0, len(self.stack_vars)):

                register = self.ret_reg_free()
                var = self.stack_vars.pop()
                pos_men = self.get_mem_pos(var)
                self.assembly.append(['subi', f'$sp', '$sp', '1'])
                self.assembly.append(['pop', f'${register}', '$sp'])
                self.assembly.append(['li', f'$rl', pos_men])
                self.assembly.append(['sw', f'${register}', '$rl'])
                self.free_reg(register)

    def push_temp_ocuped_in_stack(self):
        self.assembly.append(['push', f'$ra', '$sp'])
        self.assembly.append(['addi', f'$sp', '$sp', '1'])
        for reg in self.status_reg:
            if reg[1] == 0:
                reg[1] = 1
                if not self.is_a_arg(reg[0]):
                    self.stack_register.append(reg[0])
                    self.assembly.append(['push', f'${reg[0]}', '$sp'])
                    self.assembly.append(['addi', f'$sp', '$sp', '1'])

    def pop_temp_ocuped_in_stack(self):
        for i in range(0, len(self.stack_register)):
            register = self.stack_register.pop()
            self.status_reg[register-1][1] = 0
            self.assembly.append(['subi', f'$sp', '$sp', '1'])
            self.assembly.append(['pop', f'${register}', '$sp'])
        self.assembly.append(['subi', f'$sp', '$sp', '1'])
        self.assembly.append(['pop', f'$ra', '$sp'])

    def operation_instructions(self,inst):
        type1 = self.search_type(inst[1])
        RS = self.ret_reg_free()

        if type1 == 'var':
            pos_men = self.get_mem_pos(inst[1])
            self.assembly.append(['li', f'$rl', pos_men])
            self.assembly.append(['lw', f'${RS}', f'$rl'])
        elif type1 == 'imt':
            self.assembly.append(['li', f'${RS}', inst[1]])
        elif type1 == 'temp':
            if inst[1] in self.temp_to_register:
                self.free_reg(RS)
                RS = self.temp_to_register[inst[1]]

        type2 = self.search_type(inst[2])
        RT = self.ret_reg_free()

        if type2 == 'var':
            pos_men = self.get_mem_pos(inst[2])
            self.assembly.append(['li', f'$rl', pos_men])
            self.assembly.append(['lw', f'${RT}', f'$rl'])
        elif type2 == 'imt':
            self.assembly.append(['li', f'${RT}', inst[2]])
        elif type2 == 'temp':
            if inst[2] in self.temp_to_register:
                self.free_reg(RT)
                RT = self.temp_to_register[inst[2]]

        if self.search_type(inst[3]) == 'temp':
            self.temp_to_register[inst[3]] = self.ret_reg_free()
            RD = self.temp_to_register[inst[3]]

        self.free_reg(RS)
        self.temp_to_register[inst[1]] = -1
        self.free_reg(RT)
        self.temp_to_register[inst[2]] = -1
        return ['', f'${RD}', f'${RS}', f'${RT}']

    def get_mem_pos(self,var):
        name = f'{self.scope}.{var}'
        if name in self.semantic_table:
            return self.semantic_table[name].pos_mem
        name = f'global.{var}'
        if name in self.semantic_table:
            return self.semantic_table[name].pos_mem

    def get_qtd_args_function(self, name):
        func = self.semantic_table[name]
        return func.qtd_args

    def free_reg(self, reg):
        for i in self.status_reg:
            if i[0] == reg:
                i[1] = 1
                return 1
        return 0

    def free_all_reg(self):
        for i in self.status_reg:
            if i[1] == 0:
                i[1] = 1
        return 1

    def ret_reg_free(self):
        for reg in self.status_reg:
            if reg[1] == 1:
                reg[1] = 0
                return reg[0]

    def inicialize_reg_list(self):
        cont = 1
        while cont < 8:
            self.status_reg.append(['s' + str(cont), 1])
            cont += 1

    def search_type(self, string):
        x=''
        if re.match('t[0-9]', string):
            x = 'temp'
        elif re.match('[0-9]', string):
            x = 'imt'
        elif re.match('[a-zA-Z]', string):
            x = 'var'
        return x
