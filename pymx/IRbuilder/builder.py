from ..fakecode import Prog, Func, Global, Reg
from ..fakecode.types import cast
from ..fakecode.inst import Alloca, Store

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
