from pymx.IRbuilder.SSAbuilder.cfg import build_CFG
from pymx.IRbuilder.SSAbuilder.optimizer.debug import print_cfg

from . import generator, phi

from .context import ctx
from .simpify import simpify
from .register import register
from .allocator import allocate

class FunctionBlock:
    def __init__(self, name):
        self.name = f'{name}:\n'
        self.blocks = {}
        self.block = []

    def add_block(self, block):
        self.blocks[block.label] = block
        self.block.append(block)

    def simpify(self):
        for bb in list(self.block):
            if bb.code:
                simpify(bb)
            else:
                self.block.remove(bb)
                self.blocks.pop(bb.label)

    def replace(self):
        for block in self.block:
            for inst in block.code:
                inst.replace(ctx.regfile)

    def __str__(self):
        return self.name + ''.join([bk.__str__() for bk in self.block])

class BasicBlock:
    def __init__(self, name, label):
        self.label = f'.{name}_L{label}'
        self.code = []                

    def add_inst(self, inst):
        if type(inst) is list:
            self.code += inst
        elif inst:
            self.code.append(inst)

    def __str__(self):
        return self.label + ':\n' + ''.join([inst.__str__() for inst in self.code])

def build_func(func, args):
    fun = FunctionBlock(func.name)
    cfg = build_CFG(func)
    ctx.clear()

    trans = phi.remove(cfg)
    if args.debug:
        cfg.compute_graph()
        print_cfg(cfg, 'cfg_rmv')

    for block in cfg.block.values():
        for inst in block.code:
            ctx.add_vr(inst)

    ctx.parnum = len(func.params)
    for i in range(ctx.parnum):
        name = f'%{i}'
        vname = f'v{i}'
        if name in trans:
            vname = trans[name]
            vname = vname.replace('%', 'v')            
        ctx.regfile[vname] = register[i + 10]

    ctx.name = func.name
    size = len(cfg.order)
    for i, blk in enumerate(cfg.order):
        block = cfg.block[blk]
        next_block = -1
        if i + 1 != size:
            next_block = cfg.order[i + 1]
        
        fun.add_block(build_block(func.name, block, next_block))
    
    fun.replace()
    fun.simpify()
    allocate(fun, args)

    return fun

def build_block(name, block, next_blk):
    bb = BasicBlock(name, block.label)

    ctx.code = block.code
    ctx.next_block = next_blk
    while ctx.code:
        inst = ctx.pop_front()
        bb.add_inst(inst.generate(generator))

    return bb