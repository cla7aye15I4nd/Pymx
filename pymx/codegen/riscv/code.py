from pymx.IRbuilder.SSAbuilder.cfg import build_CFG
from pymx.IRbuilder.SSAbuilder.optimizer.debug import print_cfg

from . import generator, phi

from .context import ctx
from .simpify import simpify
from .register import register, ra, x6, sp, VirtualRegister, temporary
from .allocator import allocate
from .isa import CALL, TAIL, Ret, MV, ADDI, SW, LW, J

class FunctionBlock:
    def __init__(self, name):
        self.name = f'{name}:\n'
        self.blocks = {}
        self.block = []
        self.setup = []
        self.return_block = []
        self.start_block = BasicBlock(name, 'S')
        self.ra = None        

        self.add_block(self.start_block)     

    def add_block(self, block):        
        for idx, inst in enumerate(list(block.code)):
            if type(inst) is Ret:
                block.code.insert(idx, MV(ra, self.ra))                
                self.return_block.append(block)
                break
        self.blocks[block.label] = block
        self.block.append(block)

    def simpify(self):
        for bb in list(self.block):
            if bb.code:
                simpify(bb)            

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

        self.succ = set()
        self.pred = set()

        self.defs = set()
        self.uses = set()
        self.livein = set()
        self.liveout = set()           

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

    redirect_main(func)
    cfg = build_CFG(func)
    fun = FunctionBlock(func.name)
    
    cfg.count += 1
    fun.ra = VirtualRegister(cfg.count)
    fun.start_block.code.append(MV(fun.ra, ra))
    
    for i in range(len(func.params)):
        ctx.params.append(VirtualRegister(i))
        if i < 8:
            fun.start_block.code.append(MV(ctx.params[i], register[i + 10]))
        elif i < 18:
            load = LW(ctx.params[i], sp, (i - 8) * 4)
            ctx.loads.append(load)
            fun.start_block.code.append(load)
        else:
            ctx.stack[ctx.params[i]] = (i - 8) * 4            
            
    
    phi.remove(cfg)
    ctx.regcount = cfg.count + 2
    if args.debug:
        cfg.compute_graph()
        print_cfg(cfg, f'cfg_{func.name}_rmv')        

    for block in cfg.block.values():
        for inst in block.code:
            ctx.add_vr(inst)
    
    ctx.name = func.name
    size = len(cfg.order)
    
    for i, blk in enumerate(cfg.order):
        block = cfg.block[blk]
        next_block = -1
        if i + 1 != size:
            next_block = cfg.order[i + 1]
        
        fun.add_block(build_block(func.name, block, next_block))

    build_block_link(fun)
    fun.replace()
    allocate(fun, args)
    
    fun.replace()
    save_callee_register(fun, func.name)
    for load in ctx.loads:        
        load.offset = ctx.current_offset + load.offset
    for store in ctx.stores:
        store.offset = ctx.current_offset + store.offset
        
    hook_main(fun)
    fun.simpify()

    return fun

def build_block_link(fun):
    def addedge(u, v):
        fun.blocks[u].succ.add(v)
        fun.blocks[v].pred.add(u)

    last = None
    for bb in fun.block:
        if last: 
            addedge(last, bb.label)
        last = bb.label
        for i in bb.code:
            bb.defs |= i.def_set()
            for u in i.use_set():
                if u not in bb.defs:
                    bb.uses.add(u)
            if type(i) is J:
                addedge(bb.label, i.offset)
            if i.is_branch():
                addedge(bb.label, i.offset)

def save_callee_register(fun, name):
    modify = {ra, x6}
    preserve = set()

    if name not in ['main', '__main']:        
        for block in fun.block:
            for inst in block.code:
                modify |= inst.def_set()
                for reg in inst.preserve():
                    if reg not in ctx.spill_offset:
                        ctx.spill(reg)
                        preserve.add(reg)
    
    ctx.modify[name] = modify & temporary

    if ctx.current_offset:
        offset = ctx.current_offset
        
        setup = [ADDI(sp, sp, -offset)]
        uninstall = [ADDI(sp, sp, +offset)]
        for r in preserve:
            setup.append(SW(r, sp, ctx.spill_offset[r]))
            uninstall.insert(0, LW(r, sp, ctx.spill_offset[r]))
        
        for rb in fun.return_block:
            rb.code = rb.code[:-1] + uninstall + rb.code[-1:]
        fun.start_block.code = setup + fun.start_block.code

def redirect_main(func):
    if ctx.flip:
        if func.name == 'main':
            func.name = '__main'        
        elif func.name == '__main':
            func.name = 'main'  

def hook_main(fun):
    if ctx.flip and fun.name == 'main:\n':
        for block in fun.block:
            if type(block.code[-1]) is Ret:
                block.code[-1] = TAIL('__main', 0)
                break

def build_block(name, block, next_blk):
    bb = BasicBlock(name, block.label)

    ctx.code = block.code
    ctx.next_block = next_blk
    while ctx.code:
        inst = ctx.pop_front()
        bb.add_inst(inst.generate(generator))

    return bb