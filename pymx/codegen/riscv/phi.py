from pymx.fakecode.inst import Phi, Move

def remove(cfg):
    trans = {}
    
    users = cfg.compute_users()
    for block in cfg.block.values():
        code = block.code
        while type(code[0]) is Phi:
            phi = code[0]
            for src, label in phi.units:
                if users.get(src.name, 0) == 1:
                    trans[src.name] = phi.dst.name
                else:
                    seq = cfg.block[label.label].code
                    seq.insert(-1, Move(phi.dst, src))
            code.pop(0)    

    for block in cfg.block.values():
        for inst in block.code:
            name = inst.dest().name if inst.dest() else None
            if name in trans:
                inst.dst.name = trans[name]
