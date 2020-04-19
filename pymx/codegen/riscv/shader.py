from random import choice
from .context import ctx
from .register import register

def color(graph):
    complete = list({register[node.color] for node in graph.values() if node.color})
    
    restrict(graph)
    sample_shader(graph, complete)
    return graph

def sample_shader(graph, complete):
    def shader(node):
        if node.color is not None:
            return
        name = node.name
        adjust = {graph[n].color for n in node.edge if graph[n].color}
        for r in complete + register[5:]:
            if r.idx not in adjust and not r.preserved:
                ctx.regfile[name] = r
                node.color = r.idx
                break

    for node in graph.values():
        shader(node)

def restrict(graph):
    adjust = {}
    for name, node in graph.items():
        if node.color is None:
            adjust[name] = {graph[n].color for n in node.edge if graph[n].color}
    for name, node in graph.items():
        if name not in adjust:
            continue
        can = set()
        for u in node.edge:
            if u in adjust:
                can |= adjust[u]
        
        can -= adjust[name]
        if can:
            c = choice(list(can))
            graph[name].color = c
            ctx.regfile[name] = register[c]
