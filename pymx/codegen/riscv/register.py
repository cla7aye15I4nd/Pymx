class Register:
    def __init__(self, idx, abi, preserved, virtual=False):
        self.idx = idx
        self.abi = abi
        self.preserved = preserved
        self.virtual = virtual

    def __str__(self):
        return self.abi

    def __eq__(self, other):
        if type(other) != type(self):
            return False
        return self.abi == other.abi

    def __hash__(self):
        return hash(self.abi)

class VirtualRegister(Register):
    def __init__(self, reg):
        if type(reg) == int:
            idx = reg
            abi = 'v' + str(reg)
        else:
            idx = int(reg.name[1:])
            abi = 'v' + reg.name[1:]
        super().__init__(idx, abi, True, True)

register = [        
    Register( 0, 'zero', True),
    Register( 1, 'ra', False),
    Register( 2, 'sp', True),
    Register( 3, 'gp', False),
    Register( 4, 'yp', False),
    Register( 5, 't0', False),
    Register( 6, 't1', False),
    Register( 7, 't2', False),
    Register( 8, 's0', True),  
    Register( 9, 's1', True),
    Register(10, 'a0', False),
    Register(11, 'a1', False),
    Register(12, 'a2', False),
    Register(13, 'a3', False),
    Register(14, 'a4', False),
    Register(15, 'a5', False),
    Register(16, 'a6', False),
    Register(17, 'a7', False),
    Register(18, 's2', True),
    Register(19, 's3', True),
    Register(20, 's4', True),
    Register(21, 's5', True),
    Register(22, 's6', True),
    Register(23, 's7', True),
    Register(24, 's8', True),
    Register(25, 's9', True),
    Register(26, 's10', True),
    Register(27, 's11', True),
    Register(28, 't3', False),
    Register(29, 't4', False),
    Register(30, 't5', False),
    Register(31, 't6', False),
]

zero = register[0]
ra = register[1]
sp = register[2]
x6 = register[6]
fp = register[9]
a0 = register[10]
