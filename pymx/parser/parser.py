from ..tree.prog import Program, Function, Struct
from ..tree.stmt import Decl

from ..errors import ErrorManager, InvalidType, IdentifierError, CharacterMiss
from ..lexer.tokens import identifier

from .context import Context
from .stmt_parser import parse_block, parse_decl
from .utils import parse_type, char_check

def parse(tokens):
    return parse_program(Context(tokens))

def parse_program(ctx:Context) -> Program:
    prog = Program()
    with ErrorManager():
        while not ctx.empty():
            if prog.add(parse_function(ctx)):
                continue            
            if prog.add(parse_structs(ctx)):
                continue
            if prog.add(parse_decl(ctx)):
                continue
            raise InvalidType(ctx.top())
    return prog

def parse_function(ctx:Context) -> Function:
    def parse_params(ctx):
        params = []
        if ctx.top() == ')':
            ctx.pop()
            return params

        while True:
            token = ctx.top()
            var_type = parse_type(ctx)
            if var_type is None:
                raise InvalidType(ctx.top())

            var_name = ctx.pop()
            if var_name.kind is not identifier:
                raise IdentifierError(var_name)

            params.append(Decl(token, var_type, var_name))
            
            if ctx.top() == ')':
                break
            if ctx.top() != ',':
                raise CharacterMiss(',', ctx.prev())
            ctx.pop()

        ctx.pop()
        return params

    ctx.save()
    rtype = parse_type(ctx)
    if rtype is None:
        ctx.restore()
        return None    
    
    name  = ctx.pop()
    if (name.kind != identifier or
            ctx.top() != '('):
        ctx.restore()
        return None    
    ctx.pop()

    with ErrorManager():        
        params = parse_params(ctx)
        body = parse_block(ctx)

    return Function(rtype, name, params, body)

def parse_structs(ctx:Context) -> Struct:
    def parse_construct(ctx:Context, struct:Struct):
        ctx.save()
        if (ctx.pop() != struct.name.text or 
                ctx.pop() != '(' or ctx.pop() != ')'):
            ctx.restore()
            return None
        struct.construct = parse_block(ctx)
        return struct
        

    if ctx.top() != 'class':
        return None
    ctx.pop()
        
    name = ctx.pop()
    if name.kind != identifier:
        raise IdentifierError(name)
    char_check(ctx, '{')

    obj = Struct(name)
    while ctx.top() != '}':
        if parse_construct(ctx, obj):
            continue
        if obj.add_func(parse_function(ctx)):
            continue
        if obj.add_var(parse_decl(ctx)):
            continue
        raise InvalidType(ctx.top())
        
    ctx.pop()
    char_check(ctx, ';')

    return obj