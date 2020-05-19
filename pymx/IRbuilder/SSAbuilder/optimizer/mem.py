from copy import deepcopy
from pymx.fakecode.inst import (
    Load, Store, Branch, Ret, Phi,
    Arith, Logic, Call, Malloc
)

class MemoryAdderss:
    def __init__(self, base, offset=0):
        self.base = base
        self.offset = offset

    def __eq__(self, other):
        if type(other) is not MemoryAdderss:
            return False        
        return self.base, self.offset == other.base, other.offset

    def is_global(self):
        return self.base[0] == '@'

    def __hash__(self):
        return hash(f'{self.base}_{self.offset}')

def optimize(cfg):
    for block in cfg.block.values():
        optimize_block(cfg, block)

def optimize_block(cfg, block):
    memory = {}
    trans = {}

    code = []
    for inst in block.code:
        replace(inst, trans)
        if type(inst) is Load:
            ma = MemoryAdderss(inst.src.name)
            if ma in memory:
                trans[inst.dst.name] = memory[ma]
            else:
                code.append(inst)
                memory[ma] = inst.dst
        elif type(inst) is Store:
            ma = MemoryAdderss(inst.dst.name)
            memory[ma] = inst.src
            code.append(inst)
        else:
            code.append(inst)
    
    block.code = code
    for block in cfg.block.values():
        for inst in block.code:
            replace(inst, trans)

def replace(inst, trans):
    def replace_hook(reg):
        if reg and reg.name in trans:
            return deepcopy(trans[reg.name])
        return reg
        
    if type(inst) is Store:
        inst.src = replace_hook(inst.src)
        inst.dst = replace_hook(inst.dst)

    if type(inst) is Load:
        inst.src = replace_hook(inst.src)                    

    if type(inst) is Branch:
        inst.var = replace_hook(inst.var)        
    
    if type(inst) is Ret:
        inst.reg = replace_hook(inst.reg)                
    
    if type(inst) in [Arith, Logic]:
        inst.lhs = replace_hook(inst.lhs) 
        inst.rhs = replace_hook(inst.rhs)

    if type(inst) in [Call, Malloc]:
        inst.params = [replace_hook(par) for par in inst.params]
    
    if type(inst) is Phi:
        inst.units = [(replace_hook(unit[0]), unit[1]) for unit in inst.units]