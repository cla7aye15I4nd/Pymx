from ..tree.expr import *
from ..errors import error_collector, IdentifierError, CompilerError
from ..lexer.tokens import Token, identifier, const_contents


from .operators import operators, unary, binary
from .context import Context
from .utils import char_check, parse_type

def parse_expr(ctx:Context):
    stack = []
    prefix = []
    elements = []
    
    oper = None
    fetch_expr = True

    def make_unary(oper, expr):
        if oper.text in ['++', '--']:
            return Self(oper, expr, True)
        return Unary(oper, expr)
    
    def make_binary(oper, left, right):
        if oper.text == '=':
            return Assign(oper, left, right)
        return Binary(oper, left, right)
    
    while not ctx.empty():        
        if fetch_expr:
            expr = parse_element(ctx)
            if expr is None:
                break
            if type(expr) is Token: # operator
                if expr.text not in unary:
                    error_collector.add(CompilerError('"{}" is not a valid unary operator'.format(expr.text), expr.range))
                else:                    
                    prefix.append(expr)
            else:
                while prefix:
                    expr = make_unary(prefix[-1], expr)
                    prefix.pop()

                fetch_expr = False                
                if oper is None:
                    elements.append(expr)
                else:
                    while stack and binary[stack[-1].text] <= binary[oper.text]:    
                        elements[-2] = make_binary(stack[-1], elements[-2], elements[-1])                        
                        stack.pop()
                        elements.pop()
                    
                    stack.append(oper)
                    elements.append(expr)

                    oper = None
        else:
            expr = ctx.top()
            if expr.text in ['++', '--']:
                ctx.pop()
                elements[-1] = Self(expr, elements[-1], False)
            else:
                if expr.text not in binary:
                    break
                ctx.pop()
                oper = expr
                fetch_expr = True
    
    if not elements:
        return None
    if fetch_expr or oper:
        raise CompilerError('Syntax after "{}"'.format(oper.text), oper.range)
    if prefix:
        tk = prefix[-1]
        raise CompilerError('Syntax after "{}"'.format(tk.text), tk.range)

    while stack:
        elements[-2] = make_binary(stack[-1], elements[-1], elements[-2])
        stack.pop()
        elements.pop()
    
    return elements[0]

def parse_element(ctx:Context):
    expr = parse_atom(ctx)
    if expr is None:
        return None
    if type(expr) is Token:
        return expr

    while not ctx.empty():
        if   ctx.top() == '(': expr = parse_call(ctx, expr)
        elif ctx.top() == '[': expr = parse_access(ctx, expr)
        elif ctx.top() == '.':
            expr = Dot(ctx.pop(), expr, parse_atom(ctx))
        else: break
    
    return expr

def parse_atom(ctx:Context):    
    if ctx.top() == 'new':
        return parse_creator(ctx)
    
    if ctx.top() == '(':
        ctx.pop()
        expr = parse_expr(ctx)
        char_check(ctx, ')')
        return expr

    if ctx.top().kind == identifier:
        return Var(ctx.pop())
    if ctx.top() == 'this':
        return This(ctx.pop())
    if ctx.top().kind in const_contents:
        return Constant(ctx.pop())
    
    if ctx.top() in operators:
        return ctx.pop()

    return None
    
def parse_creator(ctx:Context) -> Creator:
    ctx.pop()
    
    sign = ctx.top()
    basetype = parse_type(ctx, True)
    if not basetype:
        raise IdentifierError(sign)
    creator = Creator(sign, basetype)

    while ctx.top() == '[':
        ctx.pop()
        creator.add(parse_expr(ctx))
        char_check(ctx, ']')

    return creator

def parse_access(ctx:Context, expr) -> Access:
    access = Access(expr)
    while ctx.top() == '[':
        ctx.pop()
        access.scale.append(parse_expr(ctx))        
        char_check(ctx, ']')
    
    return access

def parse_call(ctx:Context, expr) -> FuncCall:
    func_call = FuncCall(expr)
    char_check(ctx, '(')

    if ctx.top() == ')':
        ctx.pop()
        return func_call

    while True:
        func_call.add(parse_expr(ctx))
        if ctx.top() == ')':
            break
        char_check(ctx, ',')
    ctx.pop()

    return func_call
