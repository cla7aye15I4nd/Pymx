from ..types import PointerType, ArrayType

class Type:
    def __init__(self, bit, align):
        self.bit = bit
        self.align = align

    def __str__(self):
        if self.bit == 0:
            return 'void'
        return 'i{}'.format(self.bit)

def cast(mtype):
    return Type(mtype.size * 8, mtype.size)
