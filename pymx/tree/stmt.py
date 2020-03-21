class Stmt:
    def check(self, checker):        
        return checker.check(checker, self)

    def build(self, builder):
        return builder.build(builder, self)

class Decl(Stmt):
    def __init__(self, token, var_type, var_name, var_expr=None, sign=None):
        super().__init__()
        self.token = token
        self.var_type = var_type
        self.var_name = var_name
        self.var_expr = var_expr
        self.sign = sign

class Block(Stmt):
    def __init__(self):
        super().__init__()
        self.stmts = []
    
    def add(self, obj):
        if type(obj) is list:
            self.stmts += obj
        elif obj:
            self.stmts.append(obj)
        return obj is not None

class If(Stmt):
    def __init__(self, sign, cond, if_body, else_body=None):
        super().__init__()   
        self.sign = sign
        self.cond = cond
        self.if_body = if_body
        self.else_body = else_body

class For(Stmt):
    def __init__(self, sign, init, cond, iter, body=None):
        super().__init__()
        self.sign = sign
        self.init = init
        self.cond = cond
        self.iter = iter
        self.body = body

class While(Stmt):
    def __init__(self, sign, cond, body=None):
        super().__init__()
        self.sign = sign
        self.cond = cond
        self.body = body

class Break(Stmt):
    def __init__(self, sign):
        super().__init__()
        self.sign = sign

class Continue(Stmt):
    def __init__(self, sign):
        super().__init__()
        self.sign = sign

class Return(Stmt):
    def __init__(self, sign, expr=None):
        super().__init__()
        self.sign = sign
        self.expr = expr
