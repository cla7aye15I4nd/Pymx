import sys
from .debug import print_info, print_graph
from .isa import J, Ret, Branch, MV
from .shader import color

sys.setrecursionlimit(1000000)

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

        def add_link(set_a, set_b):
            for x in set_a: set_default(x)
            for x in set_b: set_default(x)

            for x in set_a:
                for y in set_b:
                    if x != y and (x.virtual or y.virtual):
                        graph[x.abi].edge.add(y.abi)
                        graph[y.abi].edge.add(x.abi)

        moves = set()
        for info in self.seq:
            if type(info.inst) is MV:
                rd, rs = info.inst.rd, info.inst.rs
                moves.add((rd, rs))
        
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
                add_link(info.defs, info.out_set)

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
    change = [set() for i in range(len(code.seq))]  
    def _live_analysis(i):
        inst = code.seq[i]

        for succ in inst.succ:
            if i in change[succ]:
                change[succ].remove(i)
                inst.out_set |= code.seq[succ].in_set        

        in_set = inst.uses | (inst.out_set - inst.defs)
        if in_set != inst.in_set:                
            inst.in_set = in_set  
            change[i] = set(inst.pred)
            for u in inst.pred:
                _live_analysis(u)

    for i in range(len(code.seq)):
        _live_analysis(i)
                
    # for info in code.seq:
    #     text = f'{info.inst}'
    #     text += '  [D] ' + ','.join([r.__str__() for r in info.defs]) + '\n'
    #     text += '  [U] ' + ','.join([r.__str__() for r in info.uses]) + '\n'
    #     text += '  [I] ' + ','.join([r.__str__() for r in info.in_set]) + '\n'
    #     text += '  [O] ' + ','.join([r.__str__() for r in info.out_set]) + '\n'
    #     print(text)

def live_analysis_worklist(code, args):    
    worklist = {i for i in range(len(code.seq))}
    while worklist:
        i = worklist.pop()
        inst = code.seq[i]

        out_set = set()
        for succ in inst.succ:
            out_set |= code.seq[succ].in_set
        if len(out_set) != len(inst.out_set):
            inst.out_set = out_set

        in_set = inst.uses | (inst.out_set - inst.defs)
        if in_set != inst.in_set:                
            inst.in_set = in_set  
            for u in inst.pred:
                worklist.add(u)
                