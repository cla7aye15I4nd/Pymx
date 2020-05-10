from copy import deepcopy
from pymx.fakecode.inst import Load, Store, Alloca, Ret, Call, Malloc

def optimize(cfg):
    if cfg.name == '__main':
        return

    malloc_count = 0
    for block in cfg.block.values():
        for inst in block.code:
            if type(inst) is Call:
                return            
            if type(inst) is Malloc:
                malloc_count += 1
    if malloc_count > 20:
        return
    
    read_set = {}
    write_set = {}

    head_block = cfg.block[0]
    return_block = []

    for block in cfg.block.values():
        for inst in block.code:
            if type(inst) is Ret:
                return_block.append(block)
            elif type(inst) is Load and inst.src.is_global():
                old = inst.src
                if old in read_set:
                    inst.src = deepcopy(read_set[old])
                elif old in write_set:
                    read_set[old] = write_set[old]
                    inst.src = deepcopy(write_set[old])
                else:
                    reg = cfg.get_var(inst.src)
                    cfg.add_defs(Alloca(reg))
                    read_set[old] = reg
                    inst.src = deepcopy(reg)
            elif type(inst) is Store and inst.dst.is_global():                
                old = inst.dst
                if old in write_set:
                    inst.dst = deepcopy(write_set[old])
                elif old in read_set:
                    write_set[old] = read_set[old]
                    inst.dst = deepcopy(read_set[old])
                else:
                    reg = cfg.get_var(inst.dst)
                    cfg.add_defs(Alloca(reg))
                    write_set[old] = reg
                    read_set[old] = reg
                    inst.dst  = deepcopy(reg)

    for glo, reg in read_set.items():
        r = cfg.get_var(reg)
        head_block.code = [Load(glo, r), Store(r, reg)] + head_block.code
    
    for glo, reg in write_set.items():
        for retb in return_block:
            r = cfg.get_var(reg)
            retb.code.insert(-1, Load(reg, r))            
            retb.code.insert(-1, Store(r, glo))

    