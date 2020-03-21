from ..types import IntegerType
from ..errors import ErrorManager, CompilerError
from ..tree.prog import Program, Function, Struct

from .context import ctx, Scope
from .stmt_checker import *
from .expr_checker import *

def check(chk, obj):
    name = 'check_{}'.format(obj.__class__.__name__.lower())
    return getattr(chk, name)(chk, obj)    

def check_program(chk, prog:Program):
    ctx.cur_prog = prog
    with Scope():
        with ErrorManager():
            for obj in ctx.cur_prog.objects:
                ctx.cur_prog.push(obj.check(chk))
            if 'main' not in ctx.cur_prog.functions:
                raise CompilerError('no main function')
    return ctx.cur_prog

def check_function(chk, func:Function):
    ctx.cur_func = func

    with Scope():
        with ErrorManager():
            check_function_name(func.name)
            check_main(func)

            
            for decl in func.params:
                decl.check(chk)
            
            new_stmts = []
            for stmt in func.body.stmts:
                new_stmts.append(stmt.check(chk))
            func.body.stmts = new_stmts
            
    ctx.cur_func = None
    return func

def check_struct(chk, struct:Struct):    
    with Scope():
        ctx.cur_struct = struct
        for decl in struct.variables:
            ctx.var_stack[-1][decl.var_name.text] = decl.check(chk)
        for func in struct.functions.values():
            func.check(chk)
        if struct.construct:
            struct.construct.check(chk)
        ctx.cur_struct = None

def check_function_name(name):
    if name.text in ctx.cur_prog.structs:
        raise CompilerError('Redefinition name {}'.format(name.text), range=name.range)
    if not ctx.cur_struct and name.text in ctx.cur_prog.builtin:
        raise CompilerError('{} is builtin function name'.format(name.text), range=name.range)

def check_main(func):
    if func.name.text != 'main':
        return None
    if func.params or func.rtype != IntegerType():
        desc = 'main function should be "int main()"'
        raise CompilerError(desc, range=func.name.range)
