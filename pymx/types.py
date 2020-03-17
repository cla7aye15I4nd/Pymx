class Type:
    def __init__(self, size):
        self.size = size

    def is_array(self):
        return False
    
    def is_void(self):
        return False

class IntegerType(Type):
    def __init__(self):
        super().__init__(4)
    
class BoolType(Type):
    def __init__(self):
        super().__init__(1)

class VoidType(Type):
    def __init__(self):
        super().__init__(0)
    
    def is_void(self):
        return True

class StringType(Type):
    def __init__(self):
        super().__init__(4)

class PointerType(Type):
    def __init__(self, kind):
        super().__init__(4)
        self.type = kind

class ArrayType(Type):
    def __init__(self, dim, kind):
        super().__init__(4)
        self.dim  = dim
        self.kind = kind

    def is_array(self):
        return True