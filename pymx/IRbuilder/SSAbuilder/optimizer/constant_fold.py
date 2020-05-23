from copy import deepcopy

from pymx.fakecode.inst import (
    Store, Branch, Ret, Phi, Jump,
    Load, Call, Malloc, Arith, Logic
)

def constant_fold(cfg):
    cfg.compute_graph()
    flag = True
    while flag:        
        flag = False
        flag |= elim_constant(cfg)
        flag |= elim_branch(cfg)
        flag |= elim_phi(cfg)

def elim_constant(cfg):
    flag = False
    table = {}

    def replace_hook(var):
        if hasattr(var, 'name') and var.name in table:
            return deepcopy(table[var.name])
        return var
    
    for block in cfg.block.values():
        for inst in list(block.code):
            replace(inst, replace_hook)
            retval = inst.compute()
            if retval is not None:
                flag = True
                table[inst.dest().name] = retval
                block.code.remove(inst)            
    
    for block in cfg.block.values():
        for inst in block.code:
            replace(inst, replace_hook)

    return flag

def elim_branch(cfg):
    flag = False
    for block in cfg.block.values():
        inst = block.code[-1]
        label = inst.to_jump()
        if label:
            flag = True            
            block.code[-1] = Jump(label)            

    if flag:
        cfg.compute_graph()
    return flag

def elim_phi(cfg):
    flag = False
    table = {}
    for block in list(cfg.block.values()):
        if not block.preds and block.label:
            for u in block.edges:
                cfg.block[u].preds.remove(block.label)
            flag = True
            cfg.remove_block(block.label)
    
    
    for block in cfg.block.values():
        for inst in list(block.code):
            if type(inst) is not Phi:
                continue
            for src in list(inst.units):
                label = int(src[1].label)
                if label not in block.preds:
                    inst.units.remove(src)
            if len(inst.units) == 1:
                table[inst.dest().name] = inst.units[0][0]
                block.code.remove(inst)

    def replace_hook(var):
        global flag
        while hasattr(var, 'name') and var.name in table:
            flag = True
            var = deepcopy(table[var.name])
        return var
    
    for block in cfg.block.values():
        for inst in list(block.code):
            replace(inst, replace_hook)            
    
    if flag:
        cfg.compute_graph()
    return flag

def replace(inst, replace_hook):
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
