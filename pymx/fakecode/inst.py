from ..parser.operators import arith, logic

class Alloca:
    def __init__(self,  var):
        self.var = var

    def __str__(self):
        return '  {} = alloca {}, align {}\n'.format(self.var.name, self.var.type, self.var.type.align)

class Store:
    def __init__(self, src, dest):
        self.src = src
        self.dest = dest
    
    def __str__(self):
        return '  store {}, {}, align {}\n'.format(self.src, self.dest, self.src.type.align)

class Load:
    def __init__(self, src, dest):
        self.src = src
        self.dest = dest

    def __str__(self):
        return '  {} = load {}, {}, align {}\n'.format(self.src.name, self.src.type, self.dest, self.src.type.align)

class Branch:
    def __init__(self, var, true, false):
        self.var = var
        self.true = true
        self.false = false

    def __str__(self):
        return '  br {}, label %{}, label %{}\n'.format(self.var, self.true.label, self.false.label)

class Jump:
    def __init__(self, dest):
        self.dest = dest

    def __str__(self):
        return '  br {}\n'.format(self.dest)

class Ret:
    def __init__(self, reg=None):
        self.reg = reg

    def __str__(self):
        if self.reg:
            return '  ret {}\n'.format(self.reg)
        return '  ret void\n'

class Arith:
    def __init__(self, reg, oper, lhs, rhs):
        self.reg = reg
        self.lhs = lhs
        self.rhs = rhs
        self.oper = arith[oper]

    def __str__(self):
        return '  {} = {} nsw, {}, {}\n'.format(self.reg.name, self.oper, self.lhs, self.rhs.name)

class Logic:
    def __init__(self, reg, oper, lhs, rhs):
        self.reg = reg
        self.lhs = lhs
        self.rhs = rhs
        self.oper = logic[oper]

    def __str__(self):
        return '  {} = icmp {} {}, {}\n'.format(self.reg.name, self.oper, self.lhs, self.rhs.name)
