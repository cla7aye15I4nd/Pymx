from ..tree.prog import Program, Function, Struct
from ..tree.stmt import Decl

from ..errors import ErrorManager, InvalidType, IdentifierError, CharacterMiss
from ..lexer.tokens import identifier

from .context import Context
from .stmt import parse_block, parse_decl
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
            var_type = parse_type(ctx)
            if var_type is None:
                raise InvalidType(ctx.top())

            var_name = ctx.pop()
            if var_name.kind is not identifier:
                raise IdentifierError(var_name)

            params.append(Decl(var_type, var_name))
            
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
        raise InvalidType(ctx.top())
    
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
    if ctx.top() != 'class':
        return None
    ctx.pop()
        
    name = ctx.pop()
    if name.kind != identifier:
        raise IdentifierError(name)
    char_check(ctx, '{')

    # while ctx.top() != '}':
    #     if parse_construct(tokens):
    #         continue
    #     if obj.add_function(Function.parse(tokens)):
    #         continue
    #     if obj.add_variable(Var.parse(tokens)):
    #         continue
    #     raise TypeDeclareError(tokens[0])            
        
    #     tokens.pop(0)
    #     SymbolForget.test(tokens, ';')

    #     return obj