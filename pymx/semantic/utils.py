from ..errors import CompilerError, ErrorManager
from ..types import BoolType, PointerType, ArrayType
from .context import ctx

def empty_check(what, obj, token):
    with ErrorManager():
        if obj is None:
            desc = '{} conditon can not be empty'.format(what)
            raise CompilerError(desc, range=token.range)

def condition_check(what, obj, token):
    with ErrorManager():
        if obj.type != BoolType():
            desc = '{} conditon type must be boolean'.format(what)
            raise CompilerError(desc, range=token.range)

def type_equal_check(token, type_x, type_y):
    with ErrorManager():
        if type_x != type_y:
            desc = 'Connot convert {} to {}'.format(type_x, type_y)
            raise CompilerError(desc, range=token.range)

def do_check(chk, obj):
    if obj:
        return obj.check(chk)
    return None

def type_check(var_type, tk):
    if var_type == PointerType():
        kind = var_type.kind
        if kind not in ctx.cur_prog.structs:
            raise CompilerError('No such type {}'.format(kind), range=tk.range)
    if var_type == ArrayType() and  var_type.kind == PointerType():
        kind = var_type.kind.kind
        if kind not in ctx.cur_prog.structs:
            raise CompilerError('No such type {}'.format(kind), range=tk.range)