from ..tree.stmt import *
from ..errors import ErrorManager, CompilerError
from ..types import VoidType, IntegerType, BoolType, StringType, ArrayType, PointerType

from .utils import do_check, type_check
from .utils import empty_check, condition_check, type_equal_check

from .context import ctx, Scope

def check_block(chk, block:Block):
    with Scope():
        with ErrorManager():        
            new_stmts = []
            for stmt in block.stmts:
                new_stmts.append(stmt.check(chk))
            block.stmts = new_stmts
    return block

def check_if(chk, if_:If):
    with ErrorManager():
        empty_check('if', if_.cond, if_.sign)
        if_.cond = do_check(chk, if_.cond)
        condition_check('if', if_.cond, if_.sign)
        
        if_.if_body   = do_check(chk, if_.if_body)
        if_.else_body = do_check(chk, if_.else_body)
    
    return if_

def check_for(chk, for_:For):
    with ErrorManager():
        for_.init = do_check(chk, for_.init)
            
        ctx.enter_loop()
        for_.cond = do_check(chk, for_.cond)    
        for_.body = do_check(chk, for_.body)
        for_.iter = do_check(chk, for_.iter)

        if for_.cond:
            condition_check('for', for_.cond, for_.sign)

        ctx.exit_loop()
    return for_

def check_while(chk, while_:While):
    with ErrorManager():
        ctx.enter_loop()

        empty_check('while', while_.cond, while_.sign)
        while_.cond = do_check(chk, while_.cond)
        while_.body = do_check(chk, while_.body)
        condition_check('while', while_.cond, while_.sign)
        
        ctx.exit_loop()
    return while_

def check_break(chk, break_:Break):
    label = ctx.break_label()

    with ErrorManager():
        if not label:
            desc = 'break statement not within loop'            
            raise CompilerError(desc, range=break_.sign.range)

    return break_

def check_continue(chk, continue_:Continue):
    label = ctx.continue_label()

    with ErrorManager():
        if not label:
            desc = 'continue statement not within loop'
            raise CompilerError(desc, range=continue_.sign.range)

    return continue_

def check_return(chk, return_:Return):
    with ErrorManager():
        if return_.expr:
            return_.expr = do_check(chk, return_.expr)
            return_type = return_.expr.type
        else:
            return_type = VoidType()

        if ctx.cur_func:
            type_equal_check(return_.sign, return_type, ctx.cur_func.rtype)            
        elif return_.expr:
            raise CompilerError('Invalid return statement in construct', range=return_.sign.range)
        
    return return_

def check_decl(chk, decl:Decl):
    with ErrorManager():
        type_check(decl.var_type, decl.token)
        check_var_name(decl.var_name)
    
        if decl.var_expr:
            decl.expr = do_check(chk, decl.var_expr)
            if decl.var_expr.type:
                type_equal_check(decl.sign, decl.var_expr.type, decl.var_type)
        
        old_name = decl.var_name.text
        if ctx.cur_struct and len(ctx.var_stack) == 2:
            ctx.var_stack[-1][old_name] = decl
        else:
            new_name = ctx.add_variable(decl)
            decl.var_name.text = new_name        
    return decl

def check_var_name(name):
    text = name.text
    if text in ctx.var_stack[-1]:
        desc = 'Redefintion name {} in same scope'.format(text),
        raise CompilerError(desc, range=name.range)