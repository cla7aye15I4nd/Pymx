from pymx.fakecode.inst import Phi, Move, Logic, Branch
from .context import ctx

def remove(cfg):
    trans = {}
    
    users = cfg.compute_users()
    ctx.users = users
    
    for block in cfg.block.values():
        code = block.code
        while type(code[0]) is Phi:
            phi = code[0]
            for src, label in phi.units:
                if users.get(src.name, 0) == 1:                    
                    trans[src.name] = phi.dst.name
                else:
                    seq, pos = cfg.block[label.label].code, -1
                    if (len(seq) > 1 and 
                            type(seq[-1]) is Branch and 
                                type(seq[-2]) is Logic):
                        dest = seq[-2].dest()
                        var = seq[-1].var
                        if var == dest and users[var.name] == 1:
                            pos = -2
                    seq.insert(pos, Move(phi.dst, src))
            code.pop(0)        

    ## May be bug
    for name in trans:
        while trans[name] in trans:
            trans[name] = trans[trans[name]]
    
    for block in cfg.block.values():
        for inst in block.code:
            name = inst.dest().name if inst.dest() else None
            if name in trans:
                inst.dst.name = trans[name]

    return trans