from ..parser.operators import arith, logic
from copy import deepcopy

class Alloca:
    def __init__(self,  var):
        self.var = deepcopy(var)

    def __str__(self):
        return '  {} = alloca {}, align {}\n'.format(self.var.name, self.var.type, self.var.type.align)    

    def replace(self, table, count, first):
        if first:
            table[self.var.name] = count
        else:
            self.var.replace(table)
        return 1
    
class Store:
    def __init__(self, src, dest):
        self.src = deepcopy(src)
        self.dest = deepcopy(dest)
    
    def __str__(self):
        return '  store {}, {}, align {}\n'.format(self.src, self.dest, self.src.type.align)
    
    def replace(self, table, count, first):
        if not first:
            self.src.replace(table)
            self.dest.replace(table)
        return 0

class Load:
    def __init__(self, src, dest):
        self.src = deepcopy(src)
        self.dest = deepcopy(dest)

    def __str__(self):
        return '  {} = load {}, {}, align {}\n'.format(self.dest.name, self.src.type, self.src, self.src.type.align)

    def replace(self, table, count, first):
        if first:
            table[self.dest.name] = count
        else:
            self.src.replace(table)
            self.dest.replace(table)
        return 1

class Branch:
    def __init__(self, var, true, false):
        self.var = deepcopy(var)
        self.true = deepcopy(true)
        self.false = deepcopy(false)

    def __str__(self):
        return '  br {}, label %{}, label %{}\n'.format(self.var, self.true.label, self.false.label)

    def replace(self, table, count, first):
        if not first:
            self.var.replace(table)
            self.true.replace(table, count, first)
            self.false.replace(table, count, first)
        return 0

class Jump:
    def __init__(self, dest):
        self.dest = deepcopy(dest)

    def __str__(self):
        return '  br label %{}\n'.format(self.dest.label)

    def replace(self, table, count, first):
        if not first:
            self.dest.replace(table, count, first)
        return 0

class Ret:
    def __init__(self, reg=None):
        self.reg = deepcopy(reg)

    def __str__(self):
        if self.reg:
            return '  ret {}\n'.format(self.reg)
        return '  ret void\n'

    def replace(self, table, count, first):
        if self.reg and not first:
            self.reg.replace(table)
        return 0

class Arith:
    def __init__(self, reg, oper, lhs, rhs):
        self.reg = deepcopy(reg)
        self.lhs = deepcopy(lhs)
        self.rhs = deepcopy(rhs)
        self.oper = arith[oper]

    def __str__(self):
        return '  {} = {} {}, {}\n'.format(self.reg.name, self.oper, self.lhs, self.rhs.name)

    def replace(self, table, count, first):
        if first:
            table[self.reg.name] = count
        else:
            self.reg.replace(table)
            self.lhs.replace(table)
            self.rhs.replace(table)
        return 1

class Logic:
    def __init__(self, reg, oper, lhs, rhs):
        self.reg = deepcopy(reg)
        self.lhs = deepcopy(lhs)
        self.rhs = deepcopy(rhs)
        self.oper = logic[oper]

    def __str__(self):
        return '  {} = icmp {} {}, {}\n'.format(self.reg.name, self.oper, self.lhs, self.rhs.name)

    def replace(self, table, count, first):
        if first:
            table[self.reg.name] = count
        else:
            self.reg.replace(table)
            self.lhs.replace(table)
            self.rhs.replace(table)
        return 1

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

    def replace(self, table, count, first):
        if first:
            if self.reg:
                table[self.reg.name] = count
        else:
            if self.reg:
                self.reg.replace(table)
            for par in self.params:
                par.replace(table)
        return 1

class Malloc(Call):
    def __init__(self, reg, par):
        super().__init__(reg, '__malloc', [par])

class Phi:
    def __init__(self, reg, units):
        self.reg = deepcopy(reg)
        self.units = [deepcopy(unit) for unit in units]

    def __str__(self):
        br = ', '.join([f'[ {w[0].name}, @{w[1].label} ]' for w in self.units])
        return '  {} = phi {} {}\n'.format(self.reg.name, self.reg.type, br)

    def replace(self, table, count, first):
        if first:
            table[self.reg.name] = count
        else:
            self.reg.replace(table)
            for unit in self.units:
                unit[0].replace(table)
                unit[1].replace(table, count, first)
        return 1
