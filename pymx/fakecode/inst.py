from copy import deepcopy

from . import Const, Reg
from ..parser.operators import arith, logic
from ..parser.operators import arith_compute, logic_compute

class Base:
    def dest(self):
        if type(self) is Store:
            return None
        if hasattr(self, 'dst'):
            return getattr(self, 'dst')        
        return None

    def depend(self):
        return []

    def compute(self):
        return None

    def to_jump(self):
        return None

    def generate(self, gen):
        return gen.generate(gen, self)

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

    def depend(self):
        ret = []
        if type(self.src) is Reg:
            ret.append(self.src.name)
        if type(self.dst) is Reg:
            ret.append(self.dst.name)
        return ret

class Load(Base):
    def __init__(self, src, dst):
        self.src = deepcopy(src)
        self.dst = deepcopy(dst)
        self.user = [] # using shadow copy

    def __str__(self):
        return '  {} = load {}, {}, align {}\n'.format(self.dst.name, self.src.type, self.src, self.src.type.align)

    def add_user(self, user):
        self.user.append(user)

    def depend(self):
        if type(self.src) is Reg:
            return [self.src.name]
        return []

class Branch(Base):
    def __init__(self, var, true, false):
        self.var = deepcopy(var)
        self.true = deepcopy(true)
        self.false = deepcopy(false)

    def __str__(self):
        return '  br {}, label %{}, label %{}\n'.format(self.var, self.true.label, self.false.label)

    def reverse(self):
        self.true, self.false = self.false, self.true

    def to_jump(self):
        if type(self.var) is Const:
            return self.true if self.var.name else self.false
        return None

    def depend(self):
        if type(self.var) is Reg:
            return [self.var.name]
        return []

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

    def depend(self):
        if type(self.reg) is Reg:
            return [self.reg.name]
        return []

class Arith(Base):
    def __init__(self, dst, oper, lhs, rhs):
        self.dst = deepcopy(dst)
        self.lhs = deepcopy(lhs)
        self.rhs = deepcopy(rhs)
        self.oper = arith[oper]

    def __str__(self):
        return '  {} = {} {}, {}\n'.format(self.dst.name, self.oper, self.lhs, self.rhs.name)    

    def compute(self):
        if type(self.lhs) is Const and type(self.rhs) is Const:
            return Const(self.dst.type, arith_compute(self.oper, self.lhs.name, self.rhs.name))
        if self.oper == arith['+']:
            if self.lhs.is_value(0):
                return self.rhs
            if self.rhs.is_value(0):
                return self.lhs

        if self.oper == arith['*']:
            if self.lhs.is_value(1):
                return self.rhs
            if self.rhs.is_value(1):
                return self.lhs
            if self.lhs.is_value(0) or self.rhs.is_value(0):
                return Const(self.dst.type, 0)
        if self.oper == arith['-']:
            if self.lhs == self.rhs:
                return Const(self.dst.type, 0)
            if self.rhs.is_value(0):
                return self.lhs
        return None

    def depend(self):
        dep = []
        if type(self.lhs) is Reg:
            dep.append(self.lhs.name)
        if type(self.rhs) is Reg:
            dep.append(self.rhs.name)
        return dep

class Logic(Base):
    def __init__(self, dst, oper, lhs, rhs):
        self.dst = deepcopy(dst)
        self.lhs = deepcopy(lhs)
        self.rhs = deepcopy(rhs)
        self.oper = logic[oper]

    def reverse(self):
        rev = {
            logic['>']  : logic['<'],
            logic['<']  : logic['>'],
            logic['>='] : logic['<='],
            logic['<='] : logic['>='],
        }
        self.oper = rev[self.oper]
        self.lhs, self.rhs = self.rhs, self.lhs

    def __str__(self):
        return '  {} = icmp {} {}, {}\n'.format(self.dst.name, self.oper, self.lhs, self.rhs.name)

    def compute(self):
        if type(self.lhs) is Const and type(self.rhs) is Const:
            return Const(self.dst.type, logic_compute(self.oper, self.lhs.name, self.rhs.name))
        return None

    def depend(self):
        dep = []
        if type(self.lhs) is Reg:
            dep.append(self.lhs.name)
        if type(self.rhs) is Reg:
            dep.append(self.rhs.name)
        return dep

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

    def depend(self):
        dep = []
        for par in self.params:
            if type(par) is Reg:
                dep.append(par.name)
        return dep

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

    def depend(self):
        dep = []
        for unit in self.units:
            if type(unit[0]) is Reg:
                dep.append(unit[0].name)
        return dep

class Move(Base):
    def __init__(self, dst, src):
        self.dst = deepcopy(dst)
        self.src = deepcopy(src)

    def depend(self):
        return [self.src]
    
    def __str__(self):
        return '  {} = {}\n'.format(self.dst.name, self.src)
