from .debug import print_info, print_graph
from .isa import J, Ret, Branch, MV
from .shader import color

class InstInfo:
    def __init__(self, inst):
        self.inst = inst
        self.uses = inst.use_set()
        self.defs = inst.def_set()
        self.in_set = set()
        self.out_set = set()
        self.pred = []
        self.succ = []

class Node:
    def __init__(self, reg):
        self.edge = set()
        self.move = set()
        self.name = reg.abi        
        if reg.abi[0] == 'v':
            self.color = None
        else:
            self.color = reg.idx

    def __hash__(self):
        return self.name

class InstSeq:
    def __init__(self):
        self.tagid = {}
        self.seq = []

    def length(self):
        return len(self.seq)

    def add_inst(self, inst):
        self.seq.append(InstInfo(inst))

    def add_edge(self, u, v):
        self.seq[u].succ.append(v)
        self.seq[v].pred.append(u)

    def compute_graph(self):
        graph = {}
        def set_default(r):
            if r.abi not in graph:
                graph[r.abi] = Node(r)

        def add_link(node_set):
            for x in node_set:
                set_default(x)

            for x in node_set:
                for y in node_set:
                    if x != y and (x.virtual or y.virtual):
                        graph[x.abi].edge.add(y.abi)
                        graph[y.abi].edge.add(x.abi)

        for info in self.seq:
            if type(info.inst) is MV:
                rd, rs = info.inst.rd, info.inst.rs 
                set_default(rd)
                set_default(rs)                
                graph[rd.abi].move.add(rs.abi)
                graph[rs.abi].move.add(rd.abi)
                for x in info.out_set:
                    set_default(x)
                    if x != rs:
                        graph[rd.abi].edge.add(x.abi)
                        graph[x.abi].edge.add(rd.abi)
            else:
                add_link(info.out_set)

        return graph

def allocate(fun, args):
    code = InstSeq()
    for i, bb in enumerate(fun.block):
        code.tagid[bb.label] = code.length()
        for inst in bb.code:
            code.add_inst(inst)
            
    for i, inst_info in enumerate(code.seq):
        inst = inst_info.inst
        if type(inst) is Ret:
            continue
        if type(inst) is J:
            code.add_edge(i, code.tagid[inst.offset])
            continue
        if inst.is_branch():
            code.add_edge(i, code.tagid[inst.offset])
        if i + 1 < len(code.seq):
            code.add_edge(i, i + 1)
        
    live_analysis(code, args)   
    graph = code.compute_graph()
    graph = color(graph)

    if args.debug:
        print_graph(graph, fun.name.rstrip().rstrip(':'))

    uses = set()
    for node in graph.values():
        if node.color:
            uses.add(node.color)
    return uses

def live_analysis(code, args):
    flag = True
    while flag:
        flag = False
        i = 0
        while i < len(code.seq):
            inst = code.seq[i]
            in_set = inst.uses | (inst.out_set - inst.defs)
            out_set = set()
            for succ in inst.succ:
                out_set |= code.seq[succ].in_set
            if in_set != inst.in_set:
                flag = True
                inst.in_set = in_set
            if out_set != inst.out_set:
                flag = True
                inst.out_set = out_set            
            i += 1
