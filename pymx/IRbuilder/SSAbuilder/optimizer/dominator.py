class DomTree:
    def __init__(self, succ):
        self.succ = succ
        self.analysis()
    
    def dfs(self, u, clk, level):
        self.dfn[u] = clk
        self.level[u] = level
        for v in self.succ[u]:
            if v not in self.dfn:
                clk = self.dfs(v, clk + 1, level + 1)
        return clk

    def analysis(self):        
        self.dfn  = {}
        self.level = {}
        self.dfs_clock = self.dfs(0, 1, 1)

    def get(self, x):
        if x in self.dfn:
            return Node(x, self.dfn[x], self.level[x])
        return None

class Node:
    def __init__(self, x, level, dfn):
        self.x = x
        self.dfn = dfn
        self.level = level

    def __lt__(self, other):
        if self.level > other.level:
            return True
        return self.dfn > other.dfn

def build_tree(cfg):
    dfn, end, idx = {}, {}, {}
    domin, tree, prev, succ = {}, {}, {}, {}
    fa, anc, idom, semi, min_node = {}, {}, {}, {}, {}

    def tarjan(u, clk):        
        dfn[u] = clk
        idx[clk] = u        
        for v in succ[u]:
            if dfn[v] == 0:
                anc[v] = u
                clk = tarjan(v, clk + 1)
        return clk

    def dfs(u, clk):
        dfn[u] = clk
        idx[clk] = u        
        for v in succ[u]:
            if v not in dfn:
                anc[v] = u
                clk = dfs(v, clk + 1)
        end[u] = clk
        return clk

    def find(u):
        if u == fa[u]:
            return u
        
        x = fa[u]
        fa[u] = find(fa[u])
        if dfn[semi[min_node[x]]] < dfn[semi[min_node[u]]]:
            min_node[u] = min_node[x]
        return fa[u]
                    
    def compute_df(u):
        df = set()
        for v in succ[u]:
            if idom[v] != u:
                df.add(v)
        for v in domin[u]:
            compute_df(v)
            for w in cfg.block[v].df:
                if not is_domin(u, w) or u == w:                        
                    df.add(w)
        
        cfg.block[u].df = list(df)

    def is_domin(u, v):
        return dfn[u] <= dfn[v] <= end[u]

    for block in cfg.block.values(): 
        u = block.label
        dfn[u] = 0
        tree[u] = []
        prev[u] = []
        succ[u] = []
        domin[u] = []

        fa[u] = u
        semi[u] = u
        min_node[u] = u

    for block in cfg.block.values():
        block.load_edge()
        succ[block.label] = block.edges
        for node in block.edges:
            prev[node].append(block.label)

    dfs_clock = tarjan(0, 1)
    for clk in range(dfs_clock, 1, -1):
        u = idx[clk]
        semi_clk = dfs_clock
        for v in prev[u]:
            if dfn[v] == 0:
                continue
            if dfn[v] < dfn[u]:
                semi_clk = min(semi_clk, dfn[v])
            else:
                find(v)
                semi_clk = min(semi_clk, dfn[semi[min_node[v]]])

        semi[u] = idx[semi_clk]
        fa[u] = anc[u]
        tree[semi[u]].append(u)

        u = idx[clk - 1]
        for v in tree[u]:
            find(v)
            if semi[min_node[v]] == semi[v]:
                idom[v] = semi[v]
            else:
                idom[v] = min_node[v]
    
    for clk in range(2, dfs_clock + 1):
        u = idx[clk]
        if idom[u] != semi[u]:
            idom[u] = idom[idom[u]]
        domin[idom[u]].append(u)

    dfn.clear()
    dfs(0, 1)
    compute_df(0)

    return DomTree(domin)
