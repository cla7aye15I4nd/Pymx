from ..tree.expr import Binary, Assign, Dot
from ..tree.expr import Unary, Self
from ..tree.expr import Constant, This, Var
from ..tree.expr import Access, Creator, FuncCall

from ..fakecode import Const
from ..fakecode.inst import Arith, Logic
from ..fakecode.types import cast

from ..types import StringType, NullType
from ..parser.operators import arith, logic

from .utils import do_build
from .context import ctx

def build_unary(bd, unary:Unary):
    pass

def build_self(bd, self:Self):
    pass

def build_binary(bd, binary:Binary):
    lhs = do_build(bd, binary.left)
    rhs = do_build(bd, binary.right)    
    op  = binary.oper.text
    this_type = cast(binary.type)

    if op in arith:
        reg = ctx.get_var(this_type)
        ctx.add(Arith(reg, op, lhs, rhs))
    elif op in logic:
        this_type.bit = 8
        reg = ctx.get_var(this_type)
        ctx.add(Logic(reg, op, lhs, rhs))
    elif op == '&&':
        pass
    else:
        pass

    return reg

def build_assign(bd, assign:Assign):
    pass

def build_dot(bd, dot:Dot):
    pass

def build_constant(bd, constant:Constant):
    if constant.type == StringType():
        pass
    if constant.type == NullType():
        return Const(cast(constant.type), 0)
    return Const(cast(constant.type), constant.expr.content.__int__())

def build_this(bd, this:This):
    pass

def build_var(bd, var:Var):
    pass

def build_access(bd, access:Access):
    pass

def build_funccall(bd, funcall:FuncCall):
    pass


