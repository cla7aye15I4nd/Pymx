""" fake code like llvm """

import string

class Prog:
    def __init__(self):
        self.vars = []
        self.func = []
        self.struct = []        

    def add_function(self, func):
        self.func.append(func)

    def add_struct(self, struct):
        self.struct.append(struct)

    def __str__(self):
        code = (
            "declare i32 @getInt()\n"
            "declare void @print(i8*)\n"
            "declare i32 @__malloc(i32)\n"
            "\n"
        )

        for var in self.vars:
            code += var.__str__()
        code += '\n'

        for fun in self.func:
            code += fun.__str__()

        return code

class Func:
    def __init__(self, rtype, name):
        self.rtype = rtype
        self.name  = name
        self.params = []
        self.code = []

    def add(self, var):
        self.params.append(var)
    
    def append(self, code):
        if type(code) is list:
            self.code += code
        else:
            self.code.append(code)

    def __str__(self):
        params = ', '.join([str(x) for x in self.params])
        code = 'define {} @{}({}) {{\n'.format(self.rtype, self.name, params)
        
        code += ''.join([str(x) for x in self.code])

        return code + '}\n\n'

class Union:
    def __init__(self, name, size, offset, exist):
        self.name = name
        self.size = size
        self.offset = offset
        self.func = []
        self.exist = exist

    def add_function(self, func):
        self.func.append(func)

class Global:
    def __init__(self, vtype, name, align=4, value=0):
        self.vtype = vtype
        self.name  = name
        self.align = align
        self.value = value

    def __str__(self):
        if type(self.value) is str:
            return '@{} = private unnamed_addr constant [{} x i8] c"{}", align 1\n'.format(self.name, len(self.value), self.value)
        return '@{} = global {} {}, align {}\n'.format(self.name, self.vtype, self.value, self.align)

class Reg:
    def __init__(self, type, name):
        self.type = type
        self.name = name

    def __str__(self):
        return '{} {}'.format(self.type, self.name)

    def __eq__(self, other):
        if type(other) is not Reg:
            return False
        return self.name == other.name

    def is_value(self, value):
        return False

class Label:
    def __init__(self, label):
        self.label = label

    def __str__(self):
        return '\n; <label>:{}:\n'.format(self.label)

    def standard(self, table, count, first):
        if first:
            table[f'%{self.label}'] = count
        else:
            if f'%{self.label}' in table:
                self.label = table[f'%{self.label}']
        return 1

    def __eq__(self, other):
        return self.label == other.label
    
    def __ne__(self, other):
        return not self.__eq__(other)

class Const:
    def __init__(self, type, name):
        self.type = type
        self.name = name

    def __str__(self):
        return '{} {}'.format(self.type, self.name)

    def __eq__(self, other):
        return False

    def is_value(self, value):
        return self.name == value