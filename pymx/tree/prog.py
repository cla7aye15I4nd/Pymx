class Program:
    def __init__(self):
        self.objects = []

        self.variables = {}
        self.structs   = {}
        self.functions = {}

    def add(self, obj):
        self.objects.append(obj)
        return obj is not None

class Function:
    """ Functoin node
        rtype (Type) - type of function retval
        name  (str)  - function name
        params(list) - paramaters
        body  (Block) - body
    """
    def __init__(self, rtype, name, params, body=None):
        self.rtype  = rtype
        self.name   = name
        self.params = params
        self.body   = body

class Struct:
    def __init__(self, name):
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