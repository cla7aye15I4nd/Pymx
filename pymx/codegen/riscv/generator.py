from pymx.fakecode import Const
from pymx.fakecode.inst import Branch, Move, Load, Store

from .context import ctx
from .register import VirtualRegister as vr
from .register import zero, a0, register
from .isa import (
    LI, LUI,
    LB, LW, SB, SW,
    ADDI, SLLI, SRAI, ORI, ANDI, XORI,
    ADD, SUB, MUL, REM, DIV, SLL, SRA, OR, AND, XOR,
    SLTI, SLTZ, 
    SLT, 
    BEQ, BNE, BLT, BLE, BGT, BGE,  
    BEQZ, BNEZ, BLTZ, BLEZ, BGTZ, BGEZ,
    SEQZ, SNEZ,  
    J,
    Ret, MV,
    CALL, TAIL
)

def generate(g, obj):
    name = 'generate_{}'.format(obj.__class__.__name__.lower())
    return getattr(g, name)(g, obj)

def generate_store(g, obj):
    res = []
    src = generate_register(obj.src, res)
    if obj.dst.name[0] == '@':
        dst = ctx.get_vr()
        name = obj.dst.name[1:]
        offset = f'%lo({name})'                
        res.append(LUI(dst, f'%hi({name})'))
    else:
        offset = 0
        dst = generate_register(obj.dst, res)
    
    if obj.src.type.bit == 8:
        return res + [SB(src, dst, offset)]
    else:
        return res + [SW(src, dst, offset)]

def generate_load(g, obj):
    res = []
    dst = generate_register(obj.dst, res)    
    if obj.src.name[0] == '@':        
        src = ctx.get_vr()
        name = obj.src.name[1:]
        offset = f'%lo({name})'        
        res.append(LUI(src, f'%hi({name})'))
    else:
        offset = 0
        src = generate_register(obj.src, res)
    
    if obj.dst.type.bit == 8:
        return res + [LB(dst, src, offset)]
    else:
        return res + [LW(dst, src, offset)]

def generate_branch(g, obj):
    if obj.false.label == ctx.next_block:
        return BNEZ(vr(obj.var), ctx.fmt_label(obj.true.label))
    if obj.true.label == ctx.next_block:
        return BEQZ(vr(obj.var), ctx.fmt_label(obj.false.label))
    return [
        BEQZ(vr(obj.var), ctx.fmt_label(obj.false.label)), 
        J(ctx.fmt_label(obj.true.label))
    ]

def generate_jump(g, obj):
    idx = obj.label.label
    if idx != ctx.next_block:
        return J(ctx.fmt_label(idx))

def generate_ret(g, obj):
    res = []
    if obj.reg:
        if type(obj.reg) is Const:
            res.append(LI(a0, obj.reg.name))
        else:
            if ctx.parnum:
                res.append(MV(a0, vr(obj.reg)))
            else:
                ctx.book_reg(obj.reg, a0)
    return res + [Ret()]

def generate_arith(g, obj):
    res = []
    dv = generate_register(obj.dst, res)
    lv = generate_register(obj.lhs, res)
    if type(obj.rhs) is Const:
        operator = {
            'add'  : ADDI,            
            'shl'  : SLLI,
            'ashr'  : SRAI,
            'or'  : ORI,
            'and'  : ANDI,
            'xor'  : XORI,
        }
        if obj.oper in operator:
            res.append(operator[obj.oper](dv, lv, obj.rhs.name))
        else:
            rv = ctx.get_vr()
            res.append(LI(rv, obj.rhs.name))
            operator = {
                'srem' : REM,
                'mul'  : MUL,
                'sub'  : SUB,
                'sdiv' : DIV,
            }
            res.append(operator[obj.oper](dv, lv, rv))
    else:
        operator = {
            'add'  : ADD,   
            'shl'  : SLL,
            'ashr' : SRA,
            'or'   : OR,
            'and'  : AND,
            'xor'  : XOR,            
            'srem' : REM,
            'mul'  : MUL,
            'sub'  : SUB,
            'sdiv' : DIV,
        }
        rv = generate_register(obj.rhs, res)
        res.append(operator[obj.oper](dv, lv, rv))        
    return res

def generate_logic(g, obj):
    ninst = ctx.next_inst()
    res = []
    if type(ninst) is Branch and ninst.var == obj.dst and ctx.users.get(obj.dst.name, 0) == 1:  
        ctx.pop_front()              
        if ninst.true.label == ctx.next_block and ctx.users.get(obj.dst.name, 0) == 1:
            obj.reverse()
            ninst.reverse()

        lv = generate_register(obj.lhs, res)
        rv = generate_register(obj.rhs, res)
        if ninst.false.label == ctx.next_block:                    
            offset = ctx.fmt_label(ninst.true.label)                        
            res.append(generate_branch_inst(obj.oper, lv, rv, offset))
        else:
            offset = ctx.fmt_label(ninst.true.label)
            res.append(generate_branch_inst(obj.oper, lv, rv, offset))
            res.append(J(ctx.fmt_label(ninst.false.label)))
    else:
        if type(obj.lhs) is Const:
            obj.reverse()

        lv = generate_register(obj.lhs, res)
        dv = vr(obj.dst)
        if obj.oper == 'eq':
            temp = ctx.get_vr()
            res.append(XORI(temp, lv, obj.rhs.name))
            res.append(SEQZ(dv, temp))
        elif obj.oper == 'ne':
            temp = ctx.get_vr()
            res.append(XORI(temp, lv, obj.rhs.name))
            res.append(SNEZ(dv, temp))
        elif obj.oper == 'slt':
            if type(obj.rhs) is Const:
                if obj.rhs.name == 0:
                    res.append(SLTZ(dv, lv))
                else:
                    res.append(SLTI(dv, lv, obj.rhs.name))
            else:
                res.append(SLT(dv, lv, vr(obj.rhs)))
        elif obj.oper == 'sgt':
            rv = generate_register(obj.rhs, res)
            res.append(SLT(dv, rv, lv))
        elif obj.oper == 'sge':
            temp = ctx.get_vr()
            if type(obj.rhs) is Const:
                if obj.rhs.name == 0:
                    res.append(SLTZ(temp, lv))
                else:
                    res.append(SLTI(temp, lv, obj.rhs.name))
            else:
                res.append(SLT(temp, lv, vr(obj.rhs)))
            res.append(XORI(dv, temp, 1))
        elif obj.oper == 'sle':
            temp = ctx.get_vr()
            rv = generate_register(obj.rhs, res)
            res.append(SLT(temp, rv, lv))
            res.append(XORI(dv, temp, 1))        

    return res

def generate_register(obj, res=None):
    if type(obj) is Const:
        if obj.name == 0:
            return zero
        else:
            rv = ctx.get_vr()
            res.append(LI(rv, obj.name))
            return rv
    if obj.name[0] == '@':
        temp = ctx.get_vr()        
        name = obj.name[1:]
        res.append(LUI(temp, f'%hi({name})'))
        res.append(LW(temp, temp, f'%lo({name})'))
        return temp
    else:
        return vr(obj)

def generate_branch_inst(op, lv, rv, offset):
    if rv == zero:
        return {
            'slt' : BLTZ, 'sgt' : BGTZ, 'sle' : BLEZ,
            'sge' : BGEZ, 'eq'  : BEQZ, 'ne'  : BNEZ,
        }[op](lv, offset)
    else:
        return {
            'slt' : BLT, 'sgt' : BGT, 'sle' : BLE,
            'sge' : BGE, 'eq'  : BEQ, 'ne'  : BNE,
        }[op](lv, rv, offset)

def generate_call(g, obj):
    res = []

    cur = 9
    for par in obj.params:
        cur += 1
        r = register[cur]
        if type(par) is Const:
            res.append(LI(r, par.name))
        elif par.name[0] == '@':
            rv = ctx.get_vr()
            name = par.name[1:]
            res.append(LUI(rv, f'%hi({name})'))
            res.append(LW(r, rv, f'%lo({name})'))
        else:
            res.append(MV(r, vr(par)))

    res.append(CALL(obj.name))
    if obj.dst:
        res.append(MV(vr(obj.dst), a0))
    return res

def generate_malloc(g, obj):
    res = []

    par = obj.params[0]
    if type(par.name) is int:
        res.append(LI(a0, par.name))
    else:
        res.append(MV(a0, vr(par)))

    res.append(CALL('malloc'))
    res.append(MV(vr(obj.dst), a0))
    return res

def generate_move(g, obj):
    if type(obj.src.name) is int:
        return LI(vr(obj.dst), obj.src.name)
    elif obj.src.name[0] == '@':
        res = []
        temp = vr(obj.dst)
        name = obj.src.name[1:]
        res.append(LUI(temp, f'%hi({name})'))
        res.append(LW(temp, temp, f'%lo({name})'))        
        return res
    else:
        return MV(vr(obj.dst), vr(obj.src))
