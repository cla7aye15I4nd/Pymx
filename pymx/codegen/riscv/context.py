from .register import VirtualRegister

class Context:
    def __init__(self):
        self.modify = {}
        self.clear()

    def clear(self):
        self.cur = 0
        self.name = ''
        self.code = []        
        self.users = {}        
        self.params = []
        self.regfile = {}
        self.loads = []
        self.stores = []
        self.stack = {}
        self.regcount = 0        
        self.current_offset = 0
        self.spill_offset = {}
        self.next_block = -1

    def get_offset(self):
        self.current_offset += 4
        return self.current_offset - 4

    def add_vr(self, inst):
        if inst.dest():
            name = 'v' + inst.dest().name[1:]
            self.regfile[name] = None

    def get_vr(self):
        while f'v{self.regcount}' in self.regfile:
            self.regcount += 1
        self.regfile[f'v{self.regcount}'] = None
        return VirtualRegister(self.regcount)

    def book_reg(self, reg, pv):
        name = 'v' + reg.name[1:]
        self.regfile[name] = pv

    def spill(self, reg):
        if reg in self.spill_offset:
            return self.spill_offset[reg]
        
        offset = self.get_offset()
        self.spill_offset[reg] = offset
        return offset

    def pop_front(self):
        self.cur = 0
        inst = self.code.pop(0)
        return inst

    def next_inst(self):
        if self.cur == len(self.code):
            return None
        
        inst = self.code[self.cur]
        self.cur = self.cur + 1
        return inst

    def fmt_label(self, idx):
        return f'.{self.name}_L{idx}'

ctx = Context()