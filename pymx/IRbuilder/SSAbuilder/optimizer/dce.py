from pymx.fakecode.inst import Store, Ret, Call, Malloc, Branch
from . import peephole

def optimize(cfg):
    while _optimize(cfg):
        peephole.optimize(cfg)

def _optimize(cfg):
    imp = [Store, Ret, Call, Malloc]
    
    graph = build_depend_graph(cfg)

    work_list = []

    for block in cfg.block.values():
        flag = False
        for inst in block.code:
            if type(inst) in imp:
                flag = True
                work_list += inst.depend()

        if flag:
            work_list.append(block.label)
    
    visited = set()      
    while work_list:
        u = work_list.pop(0)

        if u in visited:
            continue
        visited.add(u)        
        if u in graph:            
            for v in graph[u]:
                work_list.append(v)
    
    flag = False
    for block in list(cfg.block.values()):
        for inst in list(block.code):
            if type(inst) in imp:
                continue
            if inst.dest() and inst.dest().name not in visited:  
                flag = True
                block.code.remove(inst)
            if type(inst) is Branch and inst.var.name not in visited:
                flag = True
                block.code.remove(inst)    
            if len(block.code) == 0:
                cfg.remove_block(block.label)        
    
    return flag

def build_depend_graph(cfg):
    cfg.compute_graph()
    graph = {}
    for block in cfg.block.values():
        graph[block.label] = block.preds
        for inst in block.code:
            dest = inst.dest()
            if dest:
                graph[dest.name] = inst.depend() + [block.label]
    
    for block in cfg.block.values():
        for inst in block.code:
            if type(inst) is Branch:
                graph[inst.true.label].append(inst.var.name)
                graph[inst.false.label].append(inst.var.name)

    return graph