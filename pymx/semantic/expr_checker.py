from ..tree.expr import *
from ..tree.stmt import Decl
from ..tree.prog import Function
from ..errors import CompilerError
from ..types import IntegerType, BoolType, StringType, NullType, VoidType, PointerType, ArrayType

from .context import ctx
from .utils import do_check, type_check, type_equal_check

def check_unary(chk, unary:Unary):
    unary.expr = do_check(chk, unary.expr)
    oper = unary.oper.text

    desc = f'No match for {oper} to {unary.expr.type}'
    ce = CompilerError(desc, range=unary.oper.range)

    unary.type = unary.expr.type
    if unary.type == IntegerType():
        if oper not in ['+', '-', '~']:
            raise ce
        unary.type = IntegerType()
    elif unary.type == BoolType():
        if oper != '!':
            raise ce
        unary.type = BoolType()
    else:
        raise ce
    return unary    

def check_self(chk, self:Self):
    self.expr = do_check(chk, self.expr)
    
    if not self.expr.lval:
        desc = f'Left value required as {self.oper.text} operand'
        raise CompilerError(desc, range=self.oper.range)
    elif self.expr.type != IntegerType():
        desc = f'No match for {self.oper.text} (type is {self.expr.type})'
        raise CompilerError(desc, range=self.oper.range)

    self.lval = self.direct
    self.type = IntegerType()

    return self

def check_binary(chk, binary:Binary):
    binary.left = do_check(chk, binary.left)
    binary.right = do_check(chk, binary.right)

    lhs, rhs, oper = binary.left.type, binary.right.type, binary.oper.text

    diff = ['==', '!=']
    logic = ['&&', '||']
    compare = ['>', '>=', '<', '<=', '==', '!=']

    ce = CompilerError(f'No such operator {lhs} {oper} {rhs}', range=binary.oper.range)
    
    if lhs != rhs or lhs == VoidType():
        raise ce
                            
    if lhs == BoolType() and oper in (logic + diff):
        binary.type = BoolType()
    elif lhs == IntegerType() and not oper in logic:
        binary.type = BoolType() if oper in compare else IntegerType()
    elif lhs == StringType() and oper in compare:
        binary.type = BoolType()
    elif lhs == StringType() and oper == '+':
        binary.type = StringType()            
    elif oper in diff:
        binary.type = BoolType()        
    else:
        raise ce
    
    return binary

def check_assign(chk, assign:Assign):
    do_check(chk, assign.left)
    assign.right = do_check(chk, assign.right)
    assign.type = VoidType()
    
    if not assign.left.lval:
        raise CompilerError(f'lvalue request', range=assign.oper.range)
    
    lhs, rhs = assign.left.type, assign.right.type
    
    if lhs != rhs:
        raise CompilerError(f'Can not assign {rhs} to {lhs}', range=assign.oper.range)
                
    return assign

def check_dot(chk, dot:Dot):
    dot.lval = True
    dot.left = do_check(chk, dot.left)

    vtype = dot.left.type
    name  = dot.right
    
    if not vtype.is_base():
        for var in ctx.cur_prog.structs[vtype.kind].variables:
            if var.var_name.text == name.text:
                dot.type = var.var_type
                return dot

    raise CompilerError(f'Invalid operator {vtype}.{name.text}',
                        range=dot.oper.range)

def check_constant(chk, constant:Constant):
    this_type = type(constant.expr.content)
    
    if this_type == str: constant.type = StringType()
    if this_type == int: constant.type = IntegerType()
    if this_type == bool: constant.type = BoolType()
    if this_type == type(None): constant.type = NullType()
    
    return constant

def check_creator(chk, creator:Creator):
    ce = CompilerError(f'Wrong Creator "new {creator.basetype}"', range=creator.sign.range)    
        
    if creator.basetype.is_void():
        raise ce
    type_check(creator.basetype, creator.sign)
    if creator.scale:
        creator.type = ArrayType(dim = len(creator.scale), kind=creator.basetype)
    else:
        if creator.basetype.is_base():
            raise ce
        creator.type = creator.basetype

    flags = False
    for expr in creator.scale:
        if expr is None:
            flags = True
        elif flags:
            raise ce
        else:
            expr = expr.check(chk)
            type_equal_check(creator.sign, expr.type, IntegerType())
    return creator

def check_this(chk, this:This):
    if not ctx.cur_struct:
        raise CompilerError('Invalid This', range=this.sign)
    this.lval = True
    this.type = PointerType(kind=ctx.cur_struct.name.text)
    return this

def check_var(chk, var:Var):
    scope_var = ctx.find_variable(var.name.text)
    if scope_var is None:
        raise CompilerError('{} has not been define'.format(var.name.text), range=var.name.range)
    var.name.text = scope_var.var_name.text
    var.type = scope_var.var_type
    return var

def check_access(chk, access:Access):
    access.expr.check(chk)
    if access.expr.type != ArrayType():
        raise CompilerError('{} is not array'.format(access.expr.type), range=access.sign.range)
        
    for expr in access.scale:
        expr.check(chk)
        type_equal_check(access.sign, expr.type, IntegerType())

    if access.expr.type:
        vtype = access.expr.type
        offset = vtype.dim - len(access.scale)
        if offset >= 0:
            access.lval = True
            vtype = vtype.kind            
            if offset == 0:
                access.type = vtype
            else:
                access.type = ArrayType(dim=offset, kind=vtype)
        else:
            raise CompilerError('Invalid array access', range=access.sign.range)
    return access

def check_funccall(chk, funcall:FuncCall):        
    funcall.params = [expr.check(chk) for expr in funcall.params]

    if type(funcall.expr) is Var:    
        token = funcall.expr.name
        if (ctx.cur_struct and token.text in ctx.cur_struct.functions):
            func = ctx.cur_struct.functions[token.text]
        elif token.text in ctx.cur_prog.functions:
            func = ctx.cur_prog.functions[token.text]
        elif token.text in ctx.cur_prog.builtin:
            func = ctx.cur_prog.builtin[token.text]
        else:
            raise CompilerError(f'Invalid Function Call {token.text}', range=token.range)
    else:
        token = funcall.expr.oper
        func = fetch_function(chk, funcall.expr)

    if len(funcall.params) != len(func.params):
        raise CompilerError(f'Invalid Function call', range=token.range)

    for x, y in zip(funcall.params, func.params):
        type_equal_check(token, x.type, y.var_type)

    funcall.type = func.rtype
    return funcall

def fetch_function(chk, dot:Dot):
    dot.left = do_check(chk, dot.left)
    
    vtype = dot.left.type
    name  = dot.right
    
    ce = CompilerError(f'Invalid operator {type}.{name}', range=dot.oper.range)
    if vtype.is_array():
        if name.text == 'size':
            return Function(IntegerType(), None, [])
    elif vtype.is_string():
        if name.text == 'length':
            return Function(IntegerType(), None, [])
        if name.text == 'parseInt':
            return Function(IntegerType(), None, [])
        if name.text == 'ord':
            return Function(IntegerType(), None, [Decl(None, IntegerType(), None)])
        if name.text == 'substring':
            return Function(StringType() , None, 
                            [Decl(None, IntegerType(), None), Decl(None, IntegerType(), None)])
    else:
        funcs = ctx.cur_prog.structs[vtype.kind].functions
        if name.text in funcs:
            return funcs[name.text]
        
        raise ce