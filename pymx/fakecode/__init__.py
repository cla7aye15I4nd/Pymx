""" fake code like llvm """

from .inst import Alloca

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
        code = ''
        
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

    def standard(self):
        count = len(self.params) + 1
        alloc_code = []
        other_code = []
        for inst in self.code:
            if type(inst) is Alloca:
                alloc_code.append(inst)
            else:
                other_code.append(inst)
        self.code = alloc_code + other_code

        table = {}
        for i in range(1, count):
            table[f'%{i}'] = i
        for inst in self.code:                
            count += inst.replace(table, count, True)
        for inst in self.code:
            inst.replace(table, count, False)  
        self.code = self.code

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

    def replace(self, table):
        if all(c in '0123456789' for c in self.name[1:]):
            self.name = f'%{table[self.name]}'

class Label:
    def __init__(self, label):
        self.label = label

    def __str__(self):
        return '\n; <label>:{}:\n'.format(self.label)

    def replace(self, table, count, first):
        if first:
            table[f'%{self.label}'] = count
        else:
            self.label = table[f'%{self.label}']
        return 1

class Const:
    def __init__(self, type, name):
        self.type = type
        self.name = name

    def __str__(self):
        return '{} {}'.format(self.type, self.name)

    def replace(self, table):
        pass
