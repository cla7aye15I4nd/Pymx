from random import choice
from .context import ctx
from .register import register

def color(graph):
    complete = get_complete(graph)
    sample_shader(graph, complete)

    return graph

def get_complete(graph):
    return list({register[node.color] for node in graph.values() if node.color})

def sample_shader(graph, complete):
    def shader(node):
        if node.color is not None:
            return
        name = node.name
        adjust = {graph[n].color for n in node.edge if graph[n].color}
        for r in complete + register[5:]:
            if r.idx not in adjust:
                ctx.regfile[name] = r
                node.color = r.idx                
                break

    for node in graph.values():
        shader(node)
