from pymx.IRbuilder.SSAbuilder.cfg import build_CFG
from pymx.IRbuilder.SSAbuilder.optimizer.debug import print_cfg

from . import generator, phi

from .context import ctx
from .simpify import simpify
from .register import register, ra, sp, VirtualRegister
from .allocator import allocate
from .isa import CALL, TAIL, Ret, MV, ADDI, SW, LW

class FunctionBlock:
    def __init__(self, name):
        self.name = f'{name}:\n'
        self.blocks = {}
        self.block = []
        self.setup = []
        self.start_block = None
        self.return_block = None
        self.return_adderss = None

    def add_block(self, block):
        for idx, inst in enumerate(list(block.code)):
            if type(inst) is Ret:
                block.code.insert(idx, MV(ra, self.return_adderss))
                assert(self.return_block is None)
                self.return_block = block
                break
        if not self.block:
            block.code.insert(0, MV(self.return_adderss, ra))
        self.blocks[block.label] = block

        if not self.block:
            self.start_block = block
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
        text = self.name
        text += ''.join([cm.__str__() for cm in self.setup])
        text += ''.join([bk.__str__() for bk in self.block])
        return text

class BasicBlock:
    def __init__(self, name, label):
        self.label = f'.{name}_L{label}'
        self.code = []    
        self.call = False
        self.ret  = False            

    def add_inst(self, inst):
        if type(inst) is list:
            self.code += inst
        elif inst:
            self.code.append(inst)

    def test(self):
        for inst in self.code:
            if type(inst) is CALL:
                self.call = True
            if type(inst) in [Ret, TAIL]:
                self.call = True

    def __str__(self):
        return self.label + ':\n' + ''.join([inst.__str__() for inst in self.code])

def build_func(func, args):
    ctx.clear()
    cfg = build_CFG(func)

    if func.name == 'main':
        func.name = '__main'        
    elif func.name == '__main':
        func.name = 'main'    
    
    fun = FunctionBlock(func.name)
        
    fun.return_adderss = VirtualRegister(cfg.count + 1)
    ctx.regcount = cfg.count + 2    

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
    allocate(fun, args)
    
    fun.replace()
    preserve = set()
    for block in fun.block:
        for inst in block.code:
            for reg in inst.preserve():
                if reg not in ctx.spill_offset:
                    ctx.spill(reg)
                    preserve.add(reg)
    
    if ctx.spill_offset:
        offset = max(ctx.spill_offset.values()) + 4
        
        setup = [ADDI(sp, sp, -offset)]
        uninstall = [ADDI(sp, sp, +offset)]
        for r in preserve:
            setup.append(SW(r, sp, ctx.spill_offset[r]))
            uninstall.insert(0, LW(r, sp, ctx.spill_offset[r]))
        
        fun.return_block.code = fun.return_block.code[:-1] + uninstall + fun.return_block.code[-1:]
        fun.start_block.code = setup + fun.start_block.code
        
    if fun.name == 'main:\n':
        for block in fun.block:
            if type(block.code[-1]) is Ret:
                block.code[-1] = TAIL('__main', 0)
                break
    fun.simpify()

    return fun

def build_block(name, block, next_blk):
    bb = BasicBlock(name, block.label)

    ctx.code = block.code
    ctx.next_block = next_blk
    while ctx.code:
        inst = ctx.pop_front()
        bb.add_inst(inst.generate(generator))

    return bb