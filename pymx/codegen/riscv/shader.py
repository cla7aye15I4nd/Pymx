from random import choice
from .context import ctx
from .register import register

def color(graph):
    greedy_shader(graph)

    return graph

def get_complete(graph):
    return {register[node.color] for node in graph.values() if node.color}

def greedy_shader(graph):
    def search(node):
        adjust = node.adjust(graph)
        for r in complete + register[3:]:
            if r.idx not in adjust:
                node.color = r.idx
                ctx.regfile[node.name] = r
                return True
        print('FAIL', node.name)
        return False
    
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
            search(node)
    
    for node in graph.values():
        if node.color is None:
            search(node)

def sample_shader(graph):
    def shader(node):
        name = node.name
        adjust = {graph[n].color for n in node.edge if graph[n].color}
        for r in complete:
            if r.idx not in adjust:
                ctx.regfile[name] = r
                node.color = r.idx                
                return
        for r in register[3:]:
            if r.idx not in adjust:
                ctx.regfile[name] = r
                node.color = r.idx   
                complete.add(r)             
                return
    
    complete = get_complete(graph)
    for node in graph.values():
        if node.color is None:
            shader(node)
