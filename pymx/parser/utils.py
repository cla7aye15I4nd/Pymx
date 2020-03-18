from ..types import IntegerType, BoolType, StringType, VoidType
from ..types import PointerType, ArrayType

from ..errors import ErrorManager, error_collector
from ..errors import CharacterMiss

from ..lexer.tokens import identifier
from .context import Context

def parse_type(ctx:Context, no_array=False):
    ctx.save()

    tag = ctx.pop()
    if tag == 'void':
        return VoidType()

    this_type = None
    if tag == 'int':      this_type = IntegerType()
    elif tag == 'bool':   this_type = BoolType()
    elif tag == 'string': this_type = StringType()    
    elif tag.kind == identifier:
        this_type = PointerType(tag.text)
    else:
        ctx.restore()
        return None

    if no_array:
        return this_type
    if ctx.top() == '[':
        this_type = ArrayType(0, tag)
        while ctx.top() == '[':
            left = ctx.pop()
            with ErrorManager():
                if ctx.top() != ']':
                    raise CharacterMiss(']', left)
                ctx.pop()
            this_type.dim += 1

    return this_type

def char_check(ctx, char):
    if ctx.top() != char:
        error_collector.add(CharacterMiss(char, ctx.prev()))
    else:
        ctx.pop()