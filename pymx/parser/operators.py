unary = ['++', '--', '!', '~', '+', '-']
binary = {
    '.' :  2,
    '*' :  5, '/' :  5, '%': 5,
    '+' :  6, '-' :  6,
    '<<':  7, '>>':  7,
    '<' :  9, '<=':  9, '>': 9, '>=': 9,
    '==': 10, '!=': 10,
    '&' : 11, 
    '^' : 12,
    '|' : 13,
    '&&': 14,
    '||': 15,
    '=' : 16
}

operators = unary + list(binary)

arith = {
    '+'  : 'add' , 
    '-'  : 'sub' ,
    '*'  : 'mul' ,
    '/'  : 'sdiv',
    '%'  : 'srem',
    '<<' : 'shl',
    '>>' : 'ashr',
    '|'  : 'or',
    '&'  : 'and',
    '^'  : 'xor',
}

logic = {
    '==' : 'eq',
    '!=' : 'ne',
    '<'  : 'slt',
    '<=' : 'sle',
    '>'  : 'sgt',
    '>=' : 'sge',
}

swap_able = {'add', 'mul', 'or', 'and', 'xor'}

def logic_compute(oper, x, y):
    calculator = {
        'eq'  : lambda x, y: x == y,
        'ne'  : lambda x, y: x != y,
        'slt' : lambda x, y: x <  y,
        'sle' : lambda x, y: x <= y,
        'sgt' : lambda x, y: x >  y,
        'sge' : lambda x, y: x >= y,
    }
    return int(calculator[oper](x, y))

def arith_compute(oper, x, y):
    uint_max = 0xffffffff
    int_max  = 0x7fffffff

    def uint32(x):
        return x & uint_max

    def int32(x):    
        x = uint32(x)
        if x > int_max:
            x = x - uint_max - 1
        return x

    calculator = {
        'add' : lambda x, y: x + y,
        'sub' : lambda x, y: x - y,
        'mul' : lambda x, y: x * y,
        'sdiv'    : lambda x, y: 0 if y == 0 else x // y,
        'srem'    : lambda x, y: 0 if y == 0 else x % y,
        'shl'     : lambda x, y: uint32(x) << uint32(y),
        'ashr'    : lambda x, y: uint32(x) >> uint32(y),
        'or'      : lambda x, y: uint32(x) | uint32(y),
        'and'     : lambda x, y: uint32(x) & uint32(y),
        'xor'     : lambda x, y: uint32(x) ^ uint32(y),
    }

    return int32(calculator[oper](x, y))