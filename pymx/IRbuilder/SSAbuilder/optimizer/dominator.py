def build_tree(cfg):
    domin = {}
    tree = {}
    prev = {}
    succ = {}
        
    dfn = {}
    idx = {}

    fa = {}
    anc = {}
    idom = {}
    semi = {}
    min_node = {}

    def tarjan(u, clk):        
        dfn[u] = clk
        idx[clk] = u        
        for v in succ[u]:
            if dfn[v] == 0:
                anc[v] = u
                clk = tarjan(v, clk + 1)
        return clk

    def find(u):
        if u == fa[u]:
            return u
        
        x = fa[u]
        fa[u] = find(fa[u])
        if dfn[semi[min_node[x]]] < dfn[semi[min_node[u]]]:
            min_node[u] = min_node[x]
        return fa[u]
                    

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

    return domin
