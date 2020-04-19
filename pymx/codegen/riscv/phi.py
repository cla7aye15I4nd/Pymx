from pymx.fakecode.inst import Phi, Move, Logic, Branch
from .context import ctx

def remove(cfg):
    trans = {}
    
    users = cfg.compute_users()
    ctx.users = users

    moves = {b : [] for b in cfg.block}    
    
    for block in cfg.block.values():
        code = block.code
        while type(code[0]) is Phi:
            phi = code[0]
            for src, label in phi.units:
                # if users.get(src.name, 0) == 1:                    
                #     trans[src.name] = phi.dst.name
                moves[label.label].append((phi.dst, src))
            code.pop(0)

    for label, move in moves.items():
        mv = topsort(cfg, move)
        seq, pos = cfg.block[label].code, -1
        if (len(seq) > 1 and 
                type(seq[-1]) is Branch and 
                    type(seq[-2]) is Logic):
            dst = seq[-2].dest()
            var = seq[-1].var
            if var == dst and users[var.name] == 1:
                pos = -2
        cfg.block[label].code = seq[:pos] + mv + seq[pos:]
            
    ## Copy propagation
    # for name in trans:
    #     while trans[name] in trans:
    #         trans[name] = trans[trans[name]]
    
    # for block in cfg.block.values():
    #     for inst in block.code:
    #         name = inst.dest().name if inst.dest() else None
    #         if name in trans:
    #             inst.dst.name = trans[name]

    return trans

def topsort(cfg, edges):
    deg_in, graph = {}, {}    
    for u, v in edges:        
        deg_in[v] = deg_in.get(v, 0) + 1
        deg_in[u] = deg_in.get(u, 0)
        graph[u] = graph.get(u, []) + [v]
        graph[v] = graph.get(v, [])
    mv = []
    flag = True    

    while flag:
        node_list = [u for u in graph if graph[u] and deg_in[u] == 0]        
                
        if node_list:
            while node_list:
                u = node_list.pop()
                for v in list(graph[u]):
                    graph[u].remove(v)
                    mv.append(Move(u, v))
                    deg_in[v] -= 1                    
                    if deg_in[v] == 0 and graph[v]:
                        node_list.append(v)                        
                        
        else:
            flag = False
            for a in list(graph):
                if graph[a]:                    
                    flag = True                    
                    b = graph[a].pop(0)
                    t = cfg.get_var(b)
                    mv.append(Move(t, b))
                    
                    graph[t] = []
                    graph[a].append(t)
                    deg_in[t] = 1
                    deg_in[b] -= 1                    
                    break

    return mv
        