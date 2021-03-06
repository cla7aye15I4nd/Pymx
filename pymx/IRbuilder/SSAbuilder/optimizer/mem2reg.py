from copy import deepcopy
from pymx.fakecode import Const, Label
from pymx.fakecode.inst import Load, Store, Phi, Call, Malloc
from ..cfg import jump_block
from .heap import Heap

def place_phi_node(cfg, domin):
    cfg.compute_graph()
    cfg.compute_alloc_ref()

    values = {}
    phi_map = {}
    for var in cfg.defs.values():
        name = var.dst.name
        values[name] = 0        
        phi_map[name] = _place_phi_node(var, cfg, domin)            
            
    rename_pass(cfg, phi_map, domin)    
    
    cfg.defs.clear()

def rename_pass(cfg, phi_map, domin):
    visited = set()
    work_list = []
    block_phi = {}
    
    for alloc in phi_map:
        for blk in phi_map[alloc]:
            if blk not in block_phi:
                block_phi[blk] = [alloc]
            else:
                block_phi[blk].append(alloc)

    def handle_phi(u, pred):
        if u in block_phi:
            for alloc in block_phi[u]:
                phi = phi_map[alloc][u]
                phi.units.append((deepcopy(incoming_vals[alloc]), Label(pred)))
    
    def handle_inst(block, incoming_vals):
        if block.label in block_phi:
            for name in block_phi[block.label]:
                phi = phi_map[name][block.label]
                incoming_vals[name] = phi.dest()                

        for inst in list(block.code):
            if type(inst) is Load:
                src = inst.src.name
                if src in incoming_vals:                                        
                    val = incoming_vals[src]
                    block.code.remove(inst)                
                    for body, attr in inst.user:
                        if type(body) in [Call, Malloc]:
                            body.params[attr] = deepcopy(val)
                        elif type(body) is Phi:
                            body.units[attr] = (deepcopy(val), body.units[attr][1])
                        else:                            
                            setattr(body, attr, deepcopy(val))                

            if type(inst) is Store:
                dst = inst.dst.name
                if dst not in phi_map:
                    continue

                incoming_vals[dst] = inst.src
                block.code.remove(inst)
    
    def _rename_pass(u, pred, incoming_vals):        
        while True:
            visit_succ = set()
            handle_phi(u, pred)
            if u in visited:
                return
            
            visited.add(u)
            handle_inst(cfg.block[u], incoming_vals)

            next_node = None            
            for i, v in enumerate(cfg.block[u].edges):
                if i == 0:
                    next_node = v
                elif v not in visit_succ:
                    visit_succ.add(v)
                    work_list.append((v, u, deepcopy(incoming_vals)))
            
            if next_node is None:
                return
            
            pred = u
            u = next_node            
    
    cfg.compte_load_ref()
    incoming_vals = {key : Const(cfg.defs[key].dst.type, 0) for key in phi_map}
    work_list.append((0, None, deepcopy(incoming_vals)))

    while work_list:
        u, pred, incoming_vals = work_list.pop()
        _rename_pass(u, pred, incoming_vals)

    for alloc in phi_map:
        for blk in phi_map[alloc]:
            phi = phi_map[alloc][blk]
            cfg.block[blk].code.insert(0, phi)

def _place_phi_node(var, cfg, domin):
    var_defs = [x for x, _ in var.store]    
    live_blks = livein_blocks(var, cfg, var_defs)    
    phi_block = calculate_phi(cfg, domin, var_defs, live_blks)

    phi_inst = {}
    for blk in phi_block:
        phi = Phi(cfg.get_var(var.dst), [])
        phi_inst[blk] = phi
    
    return phi_inst

def livein_blocks(var, cfg, var_defs):
    used_blks = list(set(x for x, _ in (var.load + var.store)))
    live_blk_list = [blk for blk in used_blks if live_in_block(var, cfg.block[blk])]
    live_blks = set()
    while live_blk_list:
        u = live_blk_list.pop()        
        if u in live_blks:
            continue
        live_blks.add(u)

        for pred in cfg.block[u].preds:
            if pred in var_defs:
                continue
            live_blk_list.append(pred)

    return live_blks

def calculate_phi(cfg, domin, var_defs, live_blks):
    phi_block = []
    work_list = list(deepcopy(var_defs))
    while work_list:
        u = work_list.pop(0)        
        for v in cfg.block[u].df:
            if v not in phi_block:
                phi_block.append(v)
                if v not in var_defs:
                    work_list.append(v)

    return phi_block

def calculate_phi_linear(cfg, domin, var_defs, live_blks):
    pq = Heap()
    phi_block = []
    for blk in var_defs:
        node = domin.get(blk)
        if node:
            pq.push(node)

    visit_pq = set()
    visit_wk = set()
    while not pq.empty():        
        root = pq.pop()

        rt = root.x
        visit_wk.add(rt)
        work_list = [rt]

        while work_list:
            node = work_list.pop()
            block = cfg.block[node]

            def do_work(succ):
                succ = domin.get(succ)
                if succ.level > root.level:
                    return
                if succ.x in visit_pq:
                    return                
                visit_pq.add(succ.x)
                
                if succ.x not in live_blks:
                    return
                phi_block.append(succ.x)
                if succ.x not in var_defs:                    
                    pq.push(domin.get(succ.x))

            for succ in block.edges:
                do_work(succ)
            for ch in domin.df[node]:
                if ch not in visit_wk:
                    visit_wk.add(ch)
                    work_list.append(ch)
    return phi_block

def live_in_block(var, block):
    for inst in block.code:
        if type(inst) is Load and inst.src == var.dst:
            return True
        if type(inst) is Store and inst.dst == var.dst:
            return False
    return False

def split_edge(cfg):
    cfg.compute_graph()
    for block in list(cfg.block.values()):
        if len(block.edges) <= 1:
            continue
        for succ in list(block.edges):
            if len(cfg.block[succ].preds) > 1:                
                cfg.count += 1
                label = cfg.count                
                middle_block = jump_block(label, block.label, succ)

                block.edges.remove(succ)
                block.edges.append(label)

                cfg.block[succ].preds.append(label)
                cfg.block[succ].preds.remove(block.label)      

                br = block.code[-1]

                if br.true.label == succ:
                    br.true.label = label
                if br.false.label == succ:
                    br.false.label = label
                for phi in cfg.block[succ].code:
                    if type(phi) is not Phi:
                        break
                    for unit in phi.units:
                        if unit[1].label == block.label:
                            unit[1].label = label

                cfg.add_block(middle_block)                
