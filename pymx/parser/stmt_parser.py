from ..tree.stmt import (Block, If, For, While, Break, Continue, Return, Decl)
from ..lexer.tokens import identifier

from ..errors import ErrorManager, error_collector, CompilerError
from ..errors import CharacterMiss, IdentifierError

from ..types import VoidType

from .context import Context
from .expr_parser import parse_expr
from .utils import parse_type, char_check

def parse_statement(ctx:Context):
    if ctx.top() == ';': 
        ctx.pop()
        return None

    if ctx.top() == '{':      return parse_block(ctx)
    if ctx.top() == 'if':     return parse_if(ctx)
    if ctx.top() == 'for':    return parse_for(ctx)
    if ctx.top() == 'while':  return parse_while(ctx)
    if ctx.top() == 'return': return parse_return(ctx)
    
    if ctx.top() == 'break':    return parse_break(ctx)
    if ctx.top() == 'continue': return parse_continue(ctx)

    ctx.save()
    if parse_type(ctx) and ctx.top().kind == identifier:
        ctx.restore()
        return parse_decl(ctx)
    ctx.restore()

    expr = parse_expr(ctx)
    if expr is None:
        desc = 'Unrecognized token {}'.format(ctx.top().text)
        raise CompilerError(desc, range=ctx.top().range)
    char_check(ctx, ';')
    return expr

def parse_block(ctx:Context) -> Block:
    char_check(ctx, '{')
    obj = Block()
    while ctx.top() != '}':
        obj.add(parse_statement(ctx))
    ctx.pop()
    return obj

def pack_with_block(obj) -> Block:
    if type(obj) is Block:
        return obj
    block = Block()
    block.add(obj)
    return block

def parse_if(ctx:Context) -> If:
    sign = ctx.pop()
    
    char_check(ctx, '(')
    cond = parse_expr(ctx)
    char_check(ctx, ')')
    if_body = pack_with_block(parse_statement(ctx))

    if ctx.top() == 'else':
        ctx.pop()
        else_body = pack_with_block(parse_statement(ctx))
        return If(sign, cond, if_body, else_body)
    else:
        return If(sign, cond, if_body)
    
def parse_for(ctx:Context) -> For:
    sign = ctx.pop()
    with ErrorManager():
        char_check(ctx, '(')
        init = parse_expr(ctx)
        char_check(ctx, ';')
        cond = parse_expr(ctx)
        char_check(ctx, ';')
        iter = parse_expr(ctx)
        char_check(ctx, ')')
        body = pack_with_block(parse_statement(ctx))
        return For(sign, init, cond, iter, body)

def parse_while(ctx:Context) -> While:
    sign = ctx.pop()
    with ErrorManager():
        char_check(ctx, '(')
        cond = parse_expr(ctx)
        char_check(ctx, ')')
        body = pack_with_block(parse_statement(ctx))
        return While(sign, cond, body)

def parse_break(ctx:Context) -> Break:
    obj = Break(ctx.pop())
    char_check(ctx, ';')
    return obj

def parse_continue(ctx:Context) -> Continue:
    obj = Continue(ctx.pop())
    char_check(ctx, ';')
    return obj    

def parse_return(ctx:Context) -> Return:
    sign = ctx.pop()
    while ErrorManager():
        expr = parse_expr(ctx)
        char_check(ctx, ';')
        return Return(sign, expr)

def parse_decl(ctx:Context) -> Decl:
    token = ctx.top()
    var_type = parse_type(ctx)
    if var_type == VoidType():
        desc = 'Illegal void type variable'
        error_collector.add(CompilerError(desc, range=ctx.prev().range))
    decls = []

    while True:
        decl = Decl(token, var_type, ctx.top())
        if ctx.pop().kind != identifier:
            raise IdentifierError(ctx.prev())
        if ctx.top() == '=':
            decl.sign = ctx.pop()
            decl.var_expr = parse_expr(ctx)
            
        decls.append(decl)
        if ctx.top() == ',':
            ctx.pop()
            continue
        char_check(ctx, ';')
        break
    return decls