from copy import deepcopy

from .debug import print_info, print_graph
from .isa import J, Ret, Branch, MV, LW, SW
from .register import register, sp
from .context import ctx

class Node:
    def __init__(self, reg):
        self.edge = set()
        self.move = set()
        self.register = reg
        self.name = reg.abi        
        self.color = None if reg.abi[0] == 'v' else reg.idx        

    def adjust(self, graph):
        return {graph[_].color for _ in self.edge if graph[_].color}

    def __hash__(self):
        return hash(self.name)

def allocate(fun, args):    
    live_analysis(fun)
    graph = build_graph(fun)
    spill_node = greedy_shader(graph)

    if spill_node:
        for node in spill_node:
            ctx.spill(node)
        rewrite_program(fun, spill_node)
        return allocate(fun, args)

    if args.debug:
        print_graph(graph, fun.name.rstrip().rstrip(':'))

    return graph

def build_graph(fun):
    def add_move_edge(u, v):
        if u == v:
            return
        if u not in graph:
            graph[u] = Node(u)
        if v not in graph:
            graph[v] = Node(v)
        graph[u].move.add(v)
        graph[v].move.add(u)

    graph = {}
    for bb in fun.block:
        live = deepcopy(bb.liveout)
        for i in bb.code[::-1]:
            if type(i) is MV:
                live -= i.use_set()
                add_move_edge(i.rd, i.rs)
            idef = i.def_set()
            live |= idef
            for u in idef:
                if u not in graph:
                    graph[u] = Node(u)
                graph[u].edge |= live
            
            for u in live:
                if u not in graph:
                    graph[u] = Node(u)
                graph[u].edge |= idef

            live -= i.def_set()
            live |= i.use_set()            
    return graph

def live_analysis(fun):  
    flag = True
    while flag:
        flag = False        
        for bb in fun.block:
            livein = bb.uses | (bb.liveout - bb.defs)
            liveout = set()
            for s in bb.succ:
                liveout |= fun.blocks[s].livein
        
            if livein != bb.livein:
                bb.livein = livein
                flag = True
            
            if liveout != bb.liveout:
                bb.liveout = liveout
                flag = True

def greedy_shader(graph):
    def get_complete(graph):
        return {register[node.color] for node in graph.values() if node.color}

    def search(node, mvc = []):
        adjust = node.adjust(graph)
        for r in mvc + complete + register[3:]:
            if r.idx not in adjust and r.idx != 2:
                node.color = r.idx
                ctx.regfile[node.name] = r
                return True        
        for r in virtual_register:
            col = r.idx + 32
            if col not in adjust:
                node.color = col
                ctx.regfile[node.name] = r
                return False        
        
        spill_node.add(node.register)
        virtual_register.append(node.register)        
        node.color = node.register.idx + 32
        ctx.regfile[node.name] = node.register

        return False
    
    complete = list(get_complete(graph))
    virtual_register = []
    simpify_set = set()
    large_node = []
    K = 29
    for node in graph.values():
        if len(node.edge) < K:
            simpify_set.add(node)
        elif node.color is None:
            large_node.append(node)
    
    spill_node = set()
    large_node.sort(key = lambda node: len(node.edge))
    for node in large_node:
        if node.color is None:
            search(node)
    
    for node in graph.values():
        if node.color is None:
            mv_col = [register[graph[r].color] for r in node.move if graph[r].color]
            search(node, mvc=mv_col)

    return spill_node

def rewrite_program(fun, spill_node):
    fun.replace()
    for bb in fun.block:
        rewrite_block(bb, spill_node)

def rewrite_block(block, spill_node):
    code = []
    for inst in block.code:
        load_reg = inst.use_set() & spill_node
        store_reg = inst.def_set() & spill_node

        if type(inst) is MV:
            if load_reg and store_reg:
                for reg in load_reg:
                    code.append(LW(inst.rs, sp, ctx.spill_offset[reg]))
                for reg in store_reg:
                    code.append(SW(inst.rs, sp, ctx.spill_offset[reg]))
            elif load_reg:
                for reg in load_reg:
                    code.append(LW(inst.rd, sp, ctx.spill_offset[reg]))
            elif store_reg:
                for reg in store_reg:
                    code.append(SW(inst.rs, sp, ctx.spill_offset[reg]))
            else:
                code.append(inst)
        else:
            for reg in load_reg:
                code.append(LW(reg, sp, ctx.spill_offset[reg]))
            code.append(inst)
            for reg in store_reg:
                code.append(SW(reg, sp, ctx.spill_offset[reg]))

    block.code = code