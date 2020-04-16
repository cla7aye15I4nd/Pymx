from pymx.IRbuilder.SSAbuilder.cfg import build_CFG
from pymx.IRbuilder.SSAbuilder.optimizer.debug import print_cfg

from . import generator, phi
from .register import register
from .isa import (MV)
from .context import ctx

class FunctionBlock:
    def __init__(self, name):
        self.name = f'{name}:\n'
        self.block = []

    def add_block(self, block):
        self.block.append(block)

    def clear(self):
        for bb in self.block:
            bb.clear()

    def __str__(self):
        return self.name + ''.join([bk.__str__() for bk in self.block])

class BasicBlock:
    def __init__(self, name, label):
        self.label = f'.{name}_L{label}:\n'
        self.code = []

    def add_inst(self, inst):
        if type(inst) is list:
            self.code += inst
        elif inst:
            self.code.append(inst)

    def clear(self):
        code, self.code = self.code, []
        for inst in code:
            if type(inst) is MV and inst.rd == inst.rs:            
                continue
            self.code.append(inst)

    def __str__(self):
        return self.label + ''.join([inst.__str__() for inst in self.code])

def build_func(func, args):
    fun = FunctionBlock(func.name)
    cfg = build_CFG(func)
    ctx.clear()

    phi.remove(cfg)
    if args.debug:
        cfg.compute_graph()
        print_cfg(cfg, 'cfg_rmv')

    
    for block in cfg.block.values():
        for inst in block.code:
            ctx.add_vr(inst)

    for i in range(len(func.params)):
        ctx.regfile[f'v{i}'] = register[i + 10]

    ctx.name = func.name
    size = len(cfg.order)
    for i, blk in enumerate(cfg.order):
        block = cfg.block[blk]
        next_block = -1
        if i + 1 != size:
            next_block = cfg.order[i + 1]
        
        fun.add_block(build_block(func.name, block, next_block))
    
    for block in fun.block:
        for inst in block.code:
            inst.replace(ctx.regfile)
    
    fun.clear()
    return fun

def build_block(name, block, next_blk):
    bb = BasicBlock(name, block.label)

    ctx.code = block.code
    ctx.next_block = next_blk
    while ctx.code:
        inst = ctx.pop_front()
        bb.add_inst(inst.generate(generator))

    return bb