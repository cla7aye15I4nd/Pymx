""" fake code like llvm """

class Prog:
    def __init__(self):
        self.vars = []
        self.func = []

    def add_function(self, func):
        self.func.append(func)

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

    def __str__(self):
        params = ', '.join([str(x) for x in self.params])
        code = 'define {} @{}({}) {{\n'.format(self.rtype, self.name, params)
        
        code += ''.join([str(x) for x in self.code])

        return code + '}\n\n'

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

class Label:
    def __init__(self, label):
        self.label = label

    def __str__(self):
        return '\n; <label>:{}:\n'.format(self.label)

class Const:
    def __init__(self, type, name):
        self.type = type
        self.name = name

    def __str__(self):
        return '{} {}'.format(self.type, self.name)

class Phi:
    def __init__(self, reg, units):
        self.reg = reg
        self.units = units

    def __str__(self):
        br = ', '.join([f'[ {w[0].name}, @{w[1].label} ]' for w in self.units])
        return '  {} = phi {} {}\n'.format(self.reg.name, self.reg.type, br)