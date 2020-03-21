class Object:
    def check(self, checker):        
        return checker.check(checker, self)

    def build(self, builder):
        return builder.build(builder, self)

class Program(Object):
    def __init__(self):
        super().__init__()
        self.objects = []

        self.variables = []
        self.structs   = {}
        self.functions = {}
        self.builtin   = {}

    def add(self, obj):
        if obj is None:
            return False

        if type(obj) is list:
            self.objects += obj    
        else:
            self.objects.append(obj)

        from ..errors import CompilerError
        if type(obj) is Function:
            if obj.name.text in self.functions:
                desc = 'Redefinition function name {}'.format(obj.name.text)
                raise CompilerError(desc, range=obj.name.range)

            self.functions[obj.name.text] = obj
        elif type(obj) is Struct:
            if obj.name.text in self.structs:
                desc = 'Redefinition class name {}'.format(obj.name.text)
                raise CompilerError(desc, range=obj.name.range)

            self.structs[obj.name.text] = obj

        return True

    def push(self, obj):
        if type(obj) is Function:
            self.functions[obj.name.text] = obj
        elif type(obj) is Struct:
            self.structs[obj.name.text] = obj
        else:
            self.variables.append(obj)

class Function(Object):
    """ Functoin node
        rtype (Type) - type of function retval
        name  (str)  - function name
        params(list) - paramaters
        body  (Block) - body
    """
    def __init__(self, rtype, name, params, body=None):
        super().__init__()
        self.rtype  = rtype
        self.name   = name
        self.params = params
        self.body   = body

class Struct(Object):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.variables = []
        self.functions = {}
        self.construct = None

    def add_var(self, var):
        if var:
            self.variables += var
        return var

    def add_func(self, func):
        if func:
            self.functions[func.name.text] = func
        return func is not None