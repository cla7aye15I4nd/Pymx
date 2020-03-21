class Type:
    def __init__(self, size):
        self.size = size

    def is_array(self):
        return False
    
    def is_void(self):
        return False

    def is_null(self):
        return False

    def is_base(self):
        return False

    def is_string(self):
        return False

    def __eq__(self, other):
        return type(self) == type(other)

    def __ne__(self, other):
        return not self.__eq__(other)

class IntegerType(Type):
    def __init__(self):
        super().__init__(4)
    
    def __str__(self):
        return 'int'
    
    def is_base(self):
        return True
    
class BoolType(Type):
    def __init__(self):
        super().__init__(1)

    def __str__(self):
        return 'bool'
    
    def is_base(self):
        return True

class VoidType(Type):
    def __init__(self):
        super().__init__(0)
    
    def is_void(self):
        return True
    
    def __str__(self):
        return 'void'

class StringType(Type):
    def __init__(self):
        super().__init__(4)

    def __str__(self):
        return 'string'

    def is_base(self):
        return True
    
    def is_string(self):
        return True

class PointerType(Type):
    def __init__(self, kind=None):
        super().__init__(4)
        self.kind = kind

    def __str__(self):
        return self.kind

    def __eq__(self, other):
        if type(other) is NullType:
            return True
        if type(other) is PointerType:
            if other.kind is None or self.kind is None:
                return True
            return self.kind == other.kind    
        return False

class ArrayType(Type):
    def __init__(self, dim=0, kind=None):
        super().__init__(4)
        self.dim  = dim
        self.kind = kind

    def is_array(self):
        return True
    
    def __str__(self):
        return str(self.kind) + '[]' * self.dim

    def __eq__(self, other):
        if type(other) is NullType:
            return True
        if type(other) is ArrayType:
            if other.kind is None or self.kind is None:
                return True
            return self.kind == other.kind and self.dim == other.dim
        return False

class NullType(Type):
    def __init__(self):
        super().__init__(0)

    def is_null(self):
        return True

    def __str__(self):
        return 'null'

    def __eq__(self, other):
        if type(other) is NullType:
            return True
        if type(other) is PointerType:
            return True
        if type(other) is ArrayType:
            return True
        return False