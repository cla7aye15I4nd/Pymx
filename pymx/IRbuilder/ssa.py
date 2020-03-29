from ..fakecode.inst import Alloca, Store, Load

def ssa_build(func):
    func.standard()
    
    info = {}
    for inst in func.code:
        if type(inst) is Store:            
            dest = inst.dest.name
            if dest in info:
                info[dest].append(inst.src)
        if type(inst) is Alloca:
            info[inst.var.name] = []
    
    ## cut branch
    for alloc, store in info.items():
        if len(store) == 0:
            new_code = []            
            for inst in func.code:
                if (type(inst) is Alloca and 
                        inst.var.name == alloc):
                    continue                
                new_code.append(inst)
            func.code = new_code
        if len(store) == 1:
            new_code = []
            table = {}
            for inst in func.code:
                if (type(inst) is Store and 
                        inst.dest.name == alloc):
                    continue
                if (type(inst) is Alloca and 
                        inst.var.name == alloc):
                    continue
                if (type(inst) is Load and
                        inst.src.name == alloc):
                    table[inst.dest.name] = store[0]
                    continue
                inst.replace_reg(table)
                new_code.append(inst)
            func.code = new_code
    
    func.standard()
            
                