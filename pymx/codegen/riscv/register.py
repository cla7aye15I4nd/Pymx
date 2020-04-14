class Register:
    def __init__(self, idx, abi, preserved):
        self.idx = idx
        self.abi = abi
        self.preserved = preserved

    def __str__(self):
        return self.abi

class VirtualRegister(Register):
    def __init__(self, idx):
        super().__init__(idx, f'%{idx}', f'%{idx}', True)

register = [        
    Register( 0, 'zero', False),
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
    Register(28, 't3', True),
    Register(29, 't4', True),
    Register(30, 't5', False),
    Register(31, 't6', False),
]

zero = register[0]
ra = register[1]
sp = register[2]
x6 = register[6]
fp = register[9]
