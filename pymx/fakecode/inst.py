from copy import deepcopy

from ..parser.operators import arith, logic

class Base:
    def dest(self):
        if type(self) is Store:
            return None
        if hasattr(self, 'dst'):
            return getattr(self, 'dst')        
        return None

class Alloca(Base):
    def __init__(self,  dst):
        self.dst = deepcopy(dst)
        self.load = []
        self.store = []

    def add_load(self, load):
        self.load.append(load)

    def add_store(self, store):
        self.store.append(store)    
    
    def __str__(self):
        return '  {} = alloca {}, align {}\n'.format(self.dst.name, self.dst.type, self.dst.type.align)

class Store(Base):
    def __init__(self, src, dst):
        self.src = deepcopy(src)
        self.dst = deepcopy(dst)
    
    def __str__(self):
        return '  store {}, {}, align {}\n'.format(self.src, self.dst, self.src.type.align)

class Load(Base):
    def __init__(self, src, dst):
        self.src = deepcopy(src)
        self.dst = deepcopy(dst)

    def __str__(self):
        return '  {} = load {}, {}, align {}\n'.format(self.dst.name, self.src.type, self.src, self.src.type.align)

class Branch(Base):
    def __init__(self, var, true, false):
        self.var = deepcopy(var)
        self.true = deepcopy(true)
        self.false = deepcopy(false)

    def __str__(self):
        return '  br {}, label %{}, label %{}\n'.format(self.var, self.true.label, self.false.label)

class Jump(Base):
    def __init__(self, label):
        self.label = deepcopy(label)

    def __str__(self):
        return '  br label %{}\n'.format(self.label.label)

class Ret(Base):
    def __init__(self, reg=None):
        self.reg = deepcopy(reg)

    def __str__(self):
        if self.reg:
            return '  ret {}\n'.format(self.reg)
        return '  ret void\n'

class Arith(Base):
    def __init__(self, dst, oper, lhs, rhs):
        self.dst = deepcopy(dst)
        self.lhs = deepcopy(lhs)
        self.rhs = deepcopy(rhs)
        self.oper = arith[oper]

    def __str__(self):
        return '  {} = {} {}, {}\n'.format(self.dst.name, self.oper, self.lhs, self.rhs.name)

class Logic(Base):
    def __init__(self, dst, oper, lhs, rhs):
        self.dst = deepcopy(dst)
        self.lhs = deepcopy(lhs)
        self.rhs = deepcopy(rhs)
        self.oper = logic[oper]

    def __str__(self):
        return '  {} = icmp {} {}, {}\n'.format(self.dst.name, self.oper, self.lhs, self.rhs.name)

class Call(Base):
    def __init__(self, dst, name, params):
        self.dst = deepcopy(dst)
        self.name = deepcopy(name)
        self.params = [deepcopy(par) for par in params]

    def __str__(self):
        params = ', '.join([str(par) for par in self.params])
        if self.dst:
            return '  {} = call {} @{}({})\n'.format(self.dst.name, self.dst.type, self.name, params)
        else:
            return '  call void @{}({})\n'.format(self.name, params)

class Malloc(Call):
    def __init__(self, dst, par):
        super().__init__(dst, '__malloc', [par])

class Phi(Base):
    def __init__(self, dst, units):
        self.dst = deepcopy(dst)
        self.units = [deepcopy(unit) for unit in units]

    def __str__(self):
        br = ', '.join([f'[ {w[0].name}, %{w[1].label} ]' for w in self.units])
        return '  {} = phi {} {}\n'.format(self.dst.name, self.dst.type, br)
