from ..fakecode import Prog, Func, Union, Global, Reg
from ..fakecode.types import cast
from ..fakecode.inst import Alloca, Store

from ..lexer.tokens import Token
from ..tree.prog import Program, Function, Struct

from .context import ctx
from .stmt_builder import *
from .expr_builder import *

def build(bd, obj):
    name = 'build_{}'.format(obj.__class__.__name__.lower())
    return getattr(bd, name)(bd, obj)

def build_program(bd, prog:Program) -> Prog:
    obj = Prog()

    obj.vars = build_global_variable(prog)
    for struct in prog.structs.values():
        struct = struct.build(bd)
        obj.add_struct(struct)
        ctx.add_struct(struct)
    
    for struct in prog.structs.values():
        union = ctx.struct[struct.name.text]        
        for func in struct.functions.values():
            func.name.text = f'_{union.name}_{func.name.text}'
            ptype = PointerType(kind=struct.name.text)
            func.params = [Decl(None, ptype, Token(None, '_this'))] + func.params
            obj.add_function(func.build(bd))


    for func in prog.functions.values():
        obj.add_function(func.build(bd))
    

    obj.vars += ctx.gvar
    return obj

def build_global_variable(prog:Program):
    variables = []
    for var in prog.variables:
        name = var.var_name.text
        vtype = cast(var.var_type)
        
        gvar = Global(vtype, name, vtype.align)
        variables.append(gvar)
        ctx.global_var[name] = Reg(vtype, '@' + name)
        if var.var_expr:
            pass # TODO
    return variables

def build_function(bd, func:Function) -> Func:
    obj = Func(cast(func.rtype), func.name.text)

    ctx.clear()
    ctx.count = len(func.params)
    for var in func.params:
        obj.add(cast(var.var_type))
    
    for var in func.params:
        type = cast(var.var_type)
        obj.append(Alloca(ctx.get_var(type, var.var_name.text)))
    
    for i, v in enumerate(func.params):
        src = ctx.var_map[v.var_name.text]
        dest = Reg(cast(v.var_type), f'%{i + 1}')
        obj.append(Store(src, dest))
    
    func.body.build(bd)
    obj.append(ctx.code)

    return obj

def build_struct(bd, struct:Struct):
    """ The function just handle offset """
    size = 0
    offset = {}
    name = struct.name.text

    for var in struct.variables:
        vtype = cast(var.var_type)
        vname = var.var_name.text
                
        if size % vtype.align != 0:
            size += vtype.align - size % vtype.align
        
        offset[vname] = size
        size += vtype.bit // 8

    if size % 4 > 0:
        size += 4 - size % 4
    
    union = Union(name, size, offset, struct.construct is not None)

    return union
