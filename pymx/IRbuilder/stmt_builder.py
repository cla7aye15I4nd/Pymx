from ..tree.stmt import Block, If, For, While
from ..tree.stmt import Break, Continue, Return, Decl

from ..fakecode.types import cast
from ..fakecode.inst import Branch, Jump, Ret, Alloca, Store

from .utils import do_build
from .context import ctx

def build_block(bd, block:Block):
    for stmt in block.stmts:
        stmt.build(bd)

def build_if(bd, if_:If):
    then_label = ctx.get_label()
    else_label = ctx.get_label()
    ctx.push_br(then_label, else_label)

    reg = do_build(bd, if_.cond)
    ctx.pop_br()

    ctx.add(Branch(reg, then_label, else_label))
    ctx.add(then_label)
    do_build(bd, if_.if_body)
    ctx.add(else_label)
    do_build(bd, if_.else_body)

def build_for(bd, for_:For):
    do_build(bd, for_.init)

    start, end = ctx.enter_loop()
    then = ctx.get_label()
    tail = ctx.get_label()

    ctx.add(start)
    
    if for_.cond:
        reg = do_build(bd, for_.cond)
        ctx.add(Branch(reg, then, tail))
    else:
        ctx.add(Jump(end))

    ctx.add(then)
    do_build(bd, for_.body)
    ctx.add(end)

    do_build(bd, for_.iter)
    ctx.add(Jump(start))
    ctx.add(tail)

    ctx.exit_loop()

def build_while(bd, while_:While):
    start, end = ctx.enter_loop()
    then = ctx.get_label()

    ctx.add(start)
    reg = do_build(bd, while_.cond)
    ctx.add(Branch(reg, then, end))

    ctx.add(then)
    do_build(bd, while_.body)
    
    ctx.add(Jump(start))
    ctx.add(end)
    
    ctx.exit_loop()

def build_break(bd, break_:Break):
    ctx.add(Jump(ctx.break_label()))

def build_continue(bd, continue_:Continue):
    ctx.add(Jump(ctx.continue_label()))

def build_return(bd, return_:Return):
    if return_.expr:
        ctx.push_br(None, None)
        reg = do_build(bd, return_.expr)
        ctx.pop_br()
        ctx.add(Ret(reg))
    else:
        ctx.add(Ret())

def build_decl(bd, decl:Decl):
    name = decl.var_name.text
    type = cast(decl.var_type)
    var = ctx.get_var(type, name)
    
    ctx.add(Alloca(var))

    if decl.var_expr:
        reg = do_build(bd, decl.var_expr)
        ctx.add(Store(reg, var))
