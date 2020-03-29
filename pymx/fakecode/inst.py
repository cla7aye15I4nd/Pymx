from copy import deepcopy

from ..parser.operators import arith, logic

class Alloca:
    def __init__(self,  var):
        self.var = deepcopy(var)

    def __str__(self):
        return '  {} = alloca {}, align {}\n'.format(self.var.name, self.var.type, self.var.type.align)    

    def standard(self, table, count, first):
        if first:
            table[self.var.name] = count
        else:
            self.var.standard(table)
        return 1

    def replace_reg(self, table):
        self.var = replace_reg(self.var, table)

class Store:
    def __init__(self, src, dest):
        self.src = deepcopy(src)
        self.dest = deepcopy(dest)
    
    def __str__(self):
        return '  store {}, {}, align {}\n'.format(self.src, self.dest, self.src.type.align)
    
    def standard(self, table, count, first):
        if not first:
            self.src.standard(table)
            self.dest.standard(table)
        return 0

    def replace_reg(self, table):
        self.src = replace_reg(self.src, table)
        self.dest = replace_reg(self.dest, table)

class Load:
    def __init__(self, src, dest):
        self.src = deepcopy(src)
        self.dest = deepcopy(dest)

    def __str__(self):
        return '  {} = load {}, {}, align {}\n'.format(self.dest.name, self.src.type, self.src, self.src.type.align)

    def standard(self, table, count, first):
        if first:
            table[self.dest.name] = count
        else:
            self.src.standard(table)
            self.dest.standard(table)
        return 1

    def replace_reg(self, table):
        self.src = replace_reg(self.src, table)
        self.dest = replace_reg(self.dest, table)

class Branch:
    def __init__(self, var, true, false):
        self.var = deepcopy(var)
        self.true = deepcopy(true)
        self.false = deepcopy(false)

    def __str__(self):
        return '  br {}, label %{}, label %{}\n'.format(self.var, self.true.label, self.false.label)

    def standard(self, table, count, first):
        if not first:
            self.var.standard(table)
            self.true.standard(table, count, first)
            self.false.standard(table, count, first)
        return 0

    def replace_reg(self, table):
        self.var = replace_reg(self.var, table)

class Jump:
    def __init__(self, dest):
        self.dest = deepcopy(dest)

    def __str__(self):
        return '  br label %{}\n'.format(self.dest.label)

    def standard(self, table, count, first):
        if not first:
            self.dest.standard(table, count, first)
        return 0

    def replace_reg(self, table):
        pass

class Ret:
    def __init__(self, reg=None):
        self.reg = deepcopy(reg)

    def __str__(self):
        if self.reg:
            return '  ret {}\n'.format(self.reg)
        return '  ret void\n'

    def standard(self, table, count, first):
        if self.reg and not first:
            self.reg.standard(table)
        return 0

    def replace_reg(self, table):
        self.reg = replace_reg(self.reg, table)

class Arith:
    def __init__(self, reg, oper, lhs, rhs):
        self.reg = deepcopy(reg)
        self.lhs = deepcopy(lhs)
        self.rhs = deepcopy(rhs)
        self.oper = arith[oper]

    def __str__(self):
        return '  {} = {} {}, {}\n'.format(self.reg.name, self.oper, self.lhs, self.rhs.name)

    def standard(self, table, count, first):
        if first:
            table[self.reg.name] = count
        else:
            self.reg.standard(table)
            self.lhs.standard(table)
            self.rhs.standard(table)
        return 1

    def replace_reg(self, table):
        self.reg = replace_reg(self.reg, table)
        self.lhs = replace_reg(self.lhs, table)
        self.rhs = replace_reg(self.rhs, table)

class Logic:
    def __init__(self, reg, oper, lhs, rhs):
        self.reg = deepcopy(reg)
        self.lhs = deepcopy(lhs)
        self.rhs = deepcopy(rhs)
        self.oper = logic[oper]

    def __str__(self):
        return '  {} = icmp {} {}, {}\n'.format(self.reg.name, self.oper, self.lhs, self.rhs.name)

    def standard(self, table, count, first):
        if first:
            table[self.reg.name] = count
        else:
            self.reg.standard(table)
            self.lhs.standard(table)
            self.rhs.standard(table)
        return 1
    
    def replace_reg(self, table):
        self.reg = replace_reg(self.reg, table)
        self.lhs = replace_reg(self.lhs, table)
        self.rhs = replace_reg(self.rhs, table)

class Call:
    def __init__(self, reg, name, params):
        self.reg = deepcopy(reg)
        self.name = deepcopy(name)
        self.params = [deepcopy(par) for par in params]

    def __str__(self):
        params = ', '.join([str(par) for par in self.params])
        if self.reg:
            return '  {} = call {} @{}({})\n'.format(self.reg.name, self.reg.type, self.name, params)
        else:
            return '  call void @{}({})\n'.format(self.name, params)

    def standard(self, table, count, first):
        if first:
            if self.reg:
                table[self.reg.name] = count
        else:
            if self.reg:
                self.reg.standard(table)
            for par in self.params:
                par.standard(table)
        return 1

    def replace_reg(self, table):
        self.reg = replace_reg(self.reg, table)
        self.params = [replace_reg(par, table) for par in self.params]

class Malloc(Call):
    def __init__(self, reg, par):
        super().__init__(reg, '__malloc', [par])

class Phi:
    def __init__(self, reg, units):
        self.reg = deepcopy(reg)
        self.units = [deepcopy(unit) for unit in units]

    def __str__(self):
        br = ', '.join([f'[ {w[0].name}, %{w[1].label} ]' for w in self.units])
        return '  {} = phi {} {}\n'.format(self.reg.name, self.reg.type, br)

    def standard(self, table, count, first):
        if first:
            table[self.reg.name] = count
        else:
            self.reg.standard(table)
            for unit in self.units:
                unit[0].standard(table)
                unit[1].standard(table, count, first)
        return 1

    def replace_reg(self, table):
        self.reg = replace_reg(self.reg, table)
        self.units = [(replace_reg(unit[0], table), unit[1]) for unit in self.units]

def replace_reg(obj, table):
    from . import Reg
    if type(obj) is Reg and obj.name in table:
        return table[obj.name]
    return obj