from ..tree.expr import Binary, Assign, Dot
from ..tree.expr import Unary, Self
from ..tree.expr import Constant, This, Var
from ..tree.expr import Access, Creator, FuncCall

from ..fakecode import Const
from ..fakecode.inst import Call, Malloc, Alloca, Branch, Jump
from ..fakecode.inst import Arith, Logic, Load, Store, Phi
from ..fakecode.types import Type, cast

from ..types import StringType, NullType, BoolType, PointerType, ArrayType
from ..parser.operators import arith, logic

from .utils import do_build
from .context import ctx

def build_unary(bd, unary:Unary):
    op = unary.oper.text
    val = do_build(bd, unary.expr)
    if op == '+':
        return val
    
    reg = ctx.get_var(val.type)
    if op == '-':
        ctx.add(Arith(reg, '-', Const(val.type, 0), val))
    if op == '~':
        ctx.add(Arith(reg, '^', Const(val.type, -1), val))
    if op == '!':
        ctx.add(Arith(reg, '^', Const(val.type, 1), val))
    return reg

def build_self(bd, self:Self):
    addr = do_build(bd, self.expr)
    before = ctx.get_var(cast(self.type))
    after  = ctx.get_var(cast(self.type))

    op = self.oper.text[:1]
    ctx.add(Load(addr, before))
    ctx.add(Arith(after, op, before, Const(self.type, 1)))
    ctx.add(Store(after, addr))

    return after if self.direct else before

def build_binary(bd, binary:Binary):
    
    op  = binary.oper.text
    this_type = cast(binary.type)

    if op in arith:
        lhs = do_build(bd, binary.left)
        rhs = do_build(bd, binary.right)
        if binary.left.type == StringType():
            reg = ctx.get_var(this_type)
            ctx.add(Call(reg, "_string_add", [lhs, rhs]))
            return reg
        else:            
            reg = ctx.get_var(this_type)
            ctx.add(Arith(reg, op, lhs, rhs))
            return reg
    
    if op in logic:
        this_type.bit = 8
        lhs = do_build(bd, binary.left)
        rhs = do_build(bd, binary.right)            
        reg = ctx.get_var(this_type)
        ctx.add(Logic(reg, op, lhs, rhs))
        return reg
    
    const_true = Const(Type(8, 1), 1)
    const_false = Const(Type(8, 1), 0)
    
    left = ctx.get_label()        
    right = ctx.get_label()
    end = ctx.pop_br() if ctx.have_br() else ctx.get_label()
            
    if is_logic(binary.left):
        ctx.push_br(left)
    else:        
        ctx.add(left)

    lhs = do_build(bd, binary.left)
    
    if op == '&&':                    
        ctx.add(Branch(lhs, right, end))
        
        if is_logic(binary.right):
            ctx.push_br(right)
        else:
            ctx.add(right)
        rhs = do_build(bd, binary.right)        
        ctx.add(Jump(end))

        ctx.add(end)
        reg = ctx.get_var(rhs.type)
        ctx.add(Phi(reg, [(const_false, left), (rhs, right)]))
    if op == '||':
        ctx.add(Branch(lhs, end, right))
        
        if is_logic(binary.right):
            ctx.push_br(right)
        else:
            ctx.add(right)
        rhs = do_build(bd, binary.right)        
        ctx.add(Jump(end))

        ctx.add(end)
        reg = ctx.get_var(rhs.type)
        ctx.add(Phi(reg, [(const_true, left), (rhs, right)]))

    return reg

def is_logic(obj):
    return type(obj) is Binary and obj.oper.text in ['&&', '||']

def build_assign(bd, assign:Assign):
    reg = do_build(bd, assign.left)
    val = do_build(bd, assign.right)
    ctx.add(Store(val, reg))

def build_dot(bd, dot:Dot):
    body = do_build(bd, dot.left)
    offset = ctx.struct[dot.left.type.kind].offset[dot.right.text]

    ptr = ctx.get_var(cast(dot.left.type))
    ctx.add(Arith(ptr, '+', body, Const(Type(32, 4), offset)))

    if dot.lhs:
        return ptr
    else:
        reg = ctx.get_var(cast(dot.type))
        ctx.add(Load(ptr, reg))
        return reg

def build_constant(bd, constant:Constant):
    if constant.type == StringType():
        return ctx.add_string_const(constant.expr.content)
    if constant.type == NullType():
        return Const(cast(constant.type), 0)
    return Const(cast(constant.type), constant.expr.content.__int__())

def build_this(bd, this:This):
    addr = ctx.find_var('_this')
    if this.lhs:        
        return addr
    else:
        reg = ctx.get_var(addr.type)
        ctx.add(Load(addr, reg))
        return reg

def build_var(bd, var:Var):
    addr = ctx.find_var(var.name.text)
    if var.lhs:        
        return addr
    else:
        reg = ctx.get_var(addr.type)
        ctx.add(Load(addr, reg))
        return reg

def build_creator(bd, creator:Creator):
    if creator.scale:
        return malloc(bd, creator, 0)
    
    ## new ideniifier ();
    struct = ctx.struct[creator.basetype.kind]
    ptr = ctx.get_var(Type(32, 4))
    ctx.add(Malloc(ptr, Const(Type(32, 4), struct.size)))
    if struct.exist:
        ctx.add(Call(None, f'_{struct.name}', [ptr]))
    return ptr

def malloc(bd, creator:Creator, d:int):
    flag = (d + 1 == len(creator.scale) or 
                creator.scale[d + 1] is None)

    cap = do_build(bd, creator.scale[d])
    
    tmp = ctx.get_var(Type(32, 4))
    reg = ctx.get_var(Type(32, 4))

    if creator.basetype == BoolType():
        ctx.add(Arith(tmp, '*', cap, Const(Type(32, 4), 1)))
    else:
        ctx.add(Arith(tmp, '*', cap, Const(Type(32, 4), 4)))
    ctx.add(Arith(reg, '+', tmp, Const(Type(32, 4), 4)))

    ptr = ctx.get_var(Type(32, 4))
    ctx.add(Malloc(ptr, reg))

    res = ctx.get_var(Type(32, 4))
    ctx.add(Arith(res, '+', ptr, Const(Type(32, 4), 4)))
    ctx.add(Store(cap, ptr)) 

    if flag: return res
    
    it = ctx.get_var(Type(32, 4))
    ctx.add(Alloca(it))
    ctx.add(Store(Const(Type(32, 4), 1), it))

    true = ctx.get_label()
    start, end = ctx.enter_loop()
    cmp = ctx.get_var(Type(8, 1))
    
    ctx.add(start)
    ctx.add(Logic(cmp, '<=', it, cap))
    ctx.add(Branch(cmp, true, end))
    
    ctx.add(true)
    ext = malloc(bd, creator, d + 1)
    
    off = ctx.get_var(Type(32, 4))
    ctx.add(Arith(off, '+', ptr, it))
    ctx.add(Store(ext, off))

    ctx.add(end)
    ctx.exit_loop()
    return res

def build_access(bd, access:Access):
    ptr = do_build(bd, access.expr)
    for count, expr in enumerate(access.scale):
        reg = do_build(bd, expr)
        four = Const(Type(32, 4), 4)
        addr = ctx.get_var(Type(32, 4))
        if access.type != BoolType():
            tmp = ctx.get_var(Type(32, 4))
            ctx.add(Arith(tmp, '*', reg, four))            
            ctx.add(Arith(addr, '+', ptr, tmp))
        else:
            ctx.add(Arith(addr, '+', ptr, reg))

        if count + 1 == len(access.scale) and access.lhs:
            return addr
        nptr = ctx.get_var(Type(32, 4))
        ctx.add(Load(addr, nptr))
        ptr = nptr
    return ptr

def build_funccall(bd, funcall:FuncCall):
    func = funcall.expr
    if type(func) is Var:
        if func.name == 'println':
            par = funcall.params[0]
            if (type(par) is FuncCall and 
                    type(par.expr) is Var and 
                        par.expr.name == 'toString'):                
                func.name.text = 'printInt'
                funcall.params = par.params

        regs = []
        for expr in funcall.params:
            regs.append(do_build(bd, expr))
        reg = ctx.get_var(cast(funcall.type))
        ctx.add(Call(reg, func.name.text, regs))
        return reg
    else:
        regs = [do_build(bd, func.left)]
        for expr in funcall.params:
            regs.append(do_build(bd, expr))
        reg = ctx.get_var(cast(funcall.type))
        if func.left.type == StringType():
            if func.right.text == 'length':
                ptr = ctx.get_var(regs[0].type)                
                ctx.add(Arith(ptr, '+', regs[0], Const(Type(32, 4), -4)))
                ctx.add(Load(ptr, reg))
            else:
                ctx.add(Call(reg, f'_string_{func.right.text}', regs))
        elif func.left.type == ArrayType():
            if func.right.text == 'size':
                ptr = ctx.get_var(regs[0].type)                
                ctx.add(Arith(ptr, '+', regs[0], Const(Type(32, 4), -4)))
                ctx.add(Load(ptr, reg))
            else:
                ctx.add(Call(reg, f'__array_{func.right.text}', regs))
        else:
            ctx.add(Call(reg, f'_{func.left.type.kind}_{func.right.text}', regs))
        return reg
    