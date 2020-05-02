from copy import deepcopy

from .debug import print_info, print_graph
from .isa import J, Ret, Branch, MV
from .register import register
from .context import ctx

class Node:
    def __init__(self, reg):
        self.edge = set()
        self.move = set()
        self.name = reg.abi        
        self.color = None if reg.abi[0] == 'v' else reg.idx        

    def adjust(self, graph):
        return {graph[_].color for _ in self.edge if graph[_].color}

    def __hash__(self):
        return hash(self.name)

def allocate(fun, args):    
    live_analysis(fun)
    graph = build_graph(fun)

    colored = greedy_shader(graph)

    if args.debug:
        print_graph(graph, fun.name.rstrip().rstrip(':'))

    return colored

def build_graph(fun):
    def addedge(u, v):
        if u not in graph:
            graph[u] = Node(u)
        if v not in graph:
            graph[v] = Node(v)
        graph[u].edge.add(v)
        graph[v].edge.add(u)
    
    def add_move_edge(u, v):
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
            live |= i.def_set()
            for u in i.def_set():
                for v in live:
                    addedge(u, v)
            live = i.use_set() | (live - i.def_set())
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

def greedy_shader(const_graph):
    def get_complete(graph):
        return {register[node.color] for node in graph.values() if node.color}

    def search(node, mvc = []):
        adjust = node.adjust(graph)
        for r in mvc + complete + register[3:]:
            if r.idx not in adjust:
                node.color = r.idx
                ctx.regfile[node.name] = r
                return True
        return False
    
    graph = deepcopy(const_graph)
    complete = list(get_complete(graph))
    simpify_set = set()
    large_node = []
    K = 29
    for node in graph.values():
        if len(node.edge) < K:
            simpify_set.add(node)
        elif node.color is None:
            large_node.append(node)
    
    large_node.sort(key = lambda node: len(node.edge))
    for node in large_node:
        if node.color is None:
            if not search(node):
                return None
    
    for node in graph.values():
        if node.color is None:
            mv_col = [register[graph[r].color] for r in node.move if graph[r].color]
            search(node, mvc=mv_col)
    
    return graph
