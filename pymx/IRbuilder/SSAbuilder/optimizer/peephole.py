from pymx.fakecode.inst import (
        Jump, Branch, Phi, Store, Load,
        Arith, Logic, Call, Malloc, Ret
    )

def optimize(cfg):
    control_flow_optimize(cfg)
    eliminate_alloc(cfg)
    return cfg

def control_flow_optimize(cfg):
    flag = True

    while flag:
        flag = False
        cfg.compute_label_ref()
 
        if not flag:
            flag = eliminate_useless_jump(cfg)
        if not flag:
            flag = erase_userless_block(cfg)
        if not flag:
            flag = combine_block(cfg)

def eliminate_alloc(cfg):
    flag = True
    while flag:
        cfg.compute_alloc_ref()

        for alloc in list(cfg.defs.values()):
            if not alloc.load:
                cfg.remove_alloc(alloc)
                for bk, inst in alloc.store:
                    cfg.block[bk].code.remove(inst)
                break
            if len(alloc.store) == 1:
                bk, store = alloc.store[0]            
                rewrite_single_store_alloc(cfg, alloc, bk, store)
                break

            bks = list(set(x for x, y in (alloc.store + alloc.load)))
            if len(bks) == 1:
                bk = bks[0]
                promote_single_store_alloc(cfg, alloc, bk)
                break
        else:
            flag = False

def eliminate_useless_jump(cfg):
    flag = False
    for block in cfg.block.values():
        for inst in block.code:
            if type(inst) is Branch:
                tar_t = cfg.block[inst.true.label].head_jump
                tar_f = cfg.block[inst.false.label].head_jump
                
                if tar_t is not None:
                    flag = True
                    inst.true.label = tar_t                    
                if tar_f is not None:
                    flag = True
                    inst.false.label = tar_f
            
            if type(inst) is Jump:
                tar = cfg.block[inst.label.label].head_jump
                
                if tar is not None:
                    flag = True
                    inst.label.label = tar
    return flag

def erase_userless_block(cfg):
    flag = False
    for block in list(cfg.block.values()):
        if not block.user:
            flag = True
            cfg.remove_block(block.label)
    return flag

def combine_block(cfg):
    flag = False
    for bk in list(cfg.order):        
        jp = cfg.block[bk].tail_jump
        if jp is None:
            continue
        if len(cfg.block[jp].user) == 1:
            flag = True            
            cfg.block[bk].code.pop()
            cfg.block[bk].code += cfg.block[jp].code
            cfg.remove_block(jp)
            break
    
    return flag

def rewrite_single_store_alloc(cfg, alloc, bk, store):
    """
        The function will not handle undefined behavior like
        int f() {
            int a;
            int b = a; // use before assign
            a = 1;
            return b;
        }

        It may cause the retval is 1.
    """
    cfg.remove_alloc(alloc)
    cfg.block[bk].code.remove(store)

    rp = []
    val = store.src

    def replace_hook(reg):
        return val if reg in rp else reg
    
    for bk, inst in alloc.load:
        rp.append(inst.dst)
        cfg.block[bk].code.remove(inst)

    for block in cfg.block.values():
        for inst in block.code:
            replace(inst, replace_hook)

def promote_single_store_alloc(cfg, alloc, bk):
    cfg.remove_alloc(alloc)

    rp = {}
    val = None
    def replace_hook(reg):
        return rp[reg.name] if reg.name in rp else reg
    
    code = cfg.block[bk].code
    for inst in code:
        if type(inst) is Store and inst.dst == alloc.dst:            
            val = inst.src
        elif type(inst) is Load  and inst.src == alloc.dst:            
            rp[inst.dst.name] = val
        else:
            replace(inst, replace_hook)
    
    for _, inst in alloc.load:
        cfg.block[bk].code.remove(inst)
    for _, inst in alloc.store:
        cfg.block[bk].code.remove(inst)

def replace(inst, replace_hook):
    if type(inst) is Store:
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
