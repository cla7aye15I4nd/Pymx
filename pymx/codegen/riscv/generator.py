from pymx.fakecode import Const
from pymx.fakecode.inst import Branch

from .context import ctx
from .register import VirtualRegister as vr
from .register import zero, a0
from .isa import (
    LI, LUI,
    ADDI,
    ADD,
    BEQ, BNE, BLT, BLE, BGT, BGE,
    J,
    Ret, MV
)

def generate(g, obj):
    name = 'generate_{}'.format(obj.__class__.__name__.lower())
    return getattr(g, name)(g, obj)

def generate_store(g, obj):
    pass

def generate_load(g, obj):
    pass

def generate_branch(g, obj):
    pass

def generate_jump(g, obj):
    idx = obj.label.label
    if idx != ctx.next_block:
        return J(ctx.fmt_label(idx))

def generate_ret(g, obj):
    res = []
    if obj.reg:
        res.append(MV(a0, generate_register(obj.reg)))
    return res + [Ret()]

def generate_arith(g, obj):
    res = []
    dv = generate_register(obj.dst, res)
    lv = generate_register(obj.lhs, res)
    if type(obj.rhs) is Const:
        res.append({
            'add'  : ADDI,            
        }[obj.oper](dv, lv, obj.rhs.name))
    else:
        rv = generate_register(obj.rhs, res)
        res.append({
            'add'  : ADD,            
        }[obj.oper](dv, lv, rv))        
    return res

def generate_logic(g, obj):
    ninst = ctx.next_inst()
    res = []
    if type(ninst) is Branch and ninst.var == obj.dst:                
        if ninst.true.label == ctx.next_block:
            obj.reverse()
            ninst.reverse()

        lv = generate_register(obj.lhs, res)
        rv = generate_register(obj.rhs, res)
        if ninst.false.label == ctx.next_block:                    
            offset = ctx.fmt_label(ninst.true.label)            
            res.append(generate_branch_inst(obj.oper, lv, rv, offset))            
        else:
            pass
    else:
        pass

    return res

def generate_register(obj, res=None):
    if type(obj) is Const:
        if obj.name == 0:
            return zero
        else:
            rv = ctx.get_vr()
            res.append(LI(rv, obj.name))
            return rv
    
    return vr(obj)

def generate_branch_inst(op, lv, rv, offset):
    return {
        'slt' : BLT,
        'sgt' : BGT,
        'sle' : BLE,
        'sge' : BGE,
        'eq'  : BEQ,
        'ne'  : BNE,
    }[op](lv, rv, offset)

def generate_call(g, obj):
    pass

def generate_malloc(g, obj):
    pass

def generate_move(g, obj):
    if type(obj.src.name) is int:
        return LI(vr(obj.dst), obj.src.name)
    else:
        return LUI(vr(obj.dst), vr(obj.src))
