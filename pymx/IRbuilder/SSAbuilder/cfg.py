from copy import deepcopy
from pymx.fakecode import Label
from pymx.fakecode.inst import Alloca, Ret, Load, Store
from pymx.fakecode.inst import Branch, Jump, Phi

class CFG:
    def __init__(self):
        self.defs = {}
        self.block = {}
        self.order = []

    def add_defs(self, defs):
        self.defs[defs.dst.name] = defs
    
    def add_block(self, block):        
        self.order.append(block.label)
        self.block[block.label] = block

    def compute_label_ref(self):        
        for block in self.block.values():
            block.load_edge()
            block.user.clear()            
        
        self.block[0].add_user(-1)
        for label, block in self.block.items():
            for inst in block.code:
                if type(inst) is Phi:
                    for unit in inst.units:
                        self.add_label_ref(label, unit[1].label)
                
                if type(inst) is Branch:
                    self.add_label_ref(label, inst.true.label)
                    self.add_label_ref(label, inst.false.label)

                if type(inst) is Jump:
                    self.add_label_ref(label, inst.label.label)

    def compute_alloc_ref(self):
        """ Do not handle global variable """
        for key in self.defs:
            self.defs[key].load.clear()
            self.defs[key].store.clear()
        
        for block in self.block.values():
            for inst in block.code:
                if type(inst) is Store:
                    name = inst.dst.name
                    if name in self.defs: # global
                        self.defs[name].add_store((block.label, inst))
                
                if type(inst) is Load:
                    name = inst.src.name
                    if name in self.defs: # global
                        self.defs[name].add_load((block.label, inst))

    def add_label_ref(self, user, label):
        self.block[label].add_user(user)
    
    def remove_block(self, block):
        self.block.pop(block)
        self.order.remove(block)

    def remove_alloc(self, alloc):
        self.defs.pop(alloc.dst.name)

    def serial(self):
        code = list(self.defs.values())
        for label in self.order:
            code.append(Label(label))
            code += self.block[label].code
        
        return code

class Block:
    def __init__(self, label):
        self.label = label
        self.code = []
        self.user = []
        
        self.edges = []
        self.head_jump = None
        self.tail_jump = None

    def load_edge(self):
        head = self.code[0]
        tail = self.code[-1]
        self.edges = []
        self.head_jump = None
        self.tail_jump = None

        if type(head) is Jump:
            self.head_jump = head.label.label
        if type(tail) is Jump:
            self.edges = [tail.label.label]
            self.tail_jump = tail.label.label
        elif type(tail) is Branch:
            self.edges = [tail.true.label, tail.false.label]

    def __str__(self):
        return '|'.join([inst.__str__() for inst in self.code])        
                 
    def add_user(self, user):
        self.user.append(user)

    def add_inst(self, inst):
        self.code.append(deepcopy(inst))

    def last_inst(self):
        if self.code:
            return self.code[-1]
        return None

def build_CFG(code, args):
    cfg = CFG()
    block = Block(0)
    for inst in code:
        if type(inst) is Alloca:
            cfg.add_defs(inst)
        elif type(inst) is Label:
            if (type(block.last_inst()) not in
                    [Branch, Jump, Ret]):
                block.add_inst(Jump(inst))
            cfg.add_block(block)
            block = Block(inst.label)
        else:
            block.add_inst(inst)
    
    cfg.add_block(block)
    return cfg
