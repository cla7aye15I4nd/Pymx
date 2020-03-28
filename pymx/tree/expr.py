from .stmt import Stmt

class Expr(Stmt):
    def __init__(self, type=None, lval=False, lhs=False):
        super().__init__()
        self.type = type
        self.lval = lval
        self.lhs = lhs

class Unary(Expr):
    def __init__(self, oper, expr):
        super().__init__()
        self.oper = oper
        self.expr = expr

class Self(Unary):
    def __init__(self, oper, expr, direct):
        super().__init__(oper, expr)
        self.expr.lhs = True
        self.direct = direct

class Binary(Expr):
    def __init__(self, oper, left, right):
        super().__init__()
        self.oper = oper
        self.left = left
        self.right = right

class Assign(Binary):
    def __init__(self, oper, left, right):        
        super().__init__(oper, left, right)        
        self.left.lhs = True

class Dot(Binary):
    def __init__(self, oper, left, right):
        super().__init__(oper, left, right.name)

class Constant(Expr):
    def __init__(self, expr):
        super().__init__()
        self.expr = expr

class Creator(Expr):
    def __init__(self, sign, basetype):
        super().__init__()
        self.sign = sign        
        self.basetype = basetype
        self.scale = []

    def add(self, expr):
        self.scale.append(expr)

class This(Expr):
    def __init__(self, sign):
        super().__init__()
        self.sign = sign

class Var(Expr):
    def __init__(self, name):
        super().__init__(lval=True)
        self.name = name        

class Access(Expr):
    def __init__(self, expr, sign):
        super().__init__()
        self.expr = expr
        self.scale = []
        self.sign = sign
    
    def add(self, expr):
        self.scale.append(expr)

class FuncCall(Expr):
    def __init__(self, expr):
        super().__init__()
        self.expr = expr
        self.params = []

    def add(self, decl):
        self.params.append(decl)