from .tree.prog import Function
from .tree.stmt import Decl

from .lexer.tokens import Token
from .types import IntegerType, StringType, VoidType

builtin = {}

def add_builtin_function(rtype, name, params):
    _name = Token('', name, name)
    _params = [Decl(None, vtype, None) for vtype in params]
    builtin[name] = Function(rtype, _name, _params)

add_builtin_function(VoidType(), 'print', [StringType()])
add_builtin_function(VoidType(), 'println', [StringType()])
add_builtin_function(VoidType(), 'printInt', [IntegerType()])
add_builtin_function(VoidType(), 'printlnInt', [IntegerType()])
add_builtin_function(StringType(), 'getString', [])
add_builtin_function(IntegerType(), 'getInt', [])
add_builtin_function(StringType(), 'toString', [IntegerType()])