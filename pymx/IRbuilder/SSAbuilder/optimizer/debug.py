import os

def print_cfg(cfg, filename='cfg'):
    with open(f'{filename}.dot', 'w') as f:
        f.write('digraph cfg{\n')
        for block in cfg.block.values():            
            f.write(f'  node{block.label}[label="{{ label %{block.label} | {block}}}", fontsize="25" fontname="Ubuntu Mono", fillcolor="#fdf6e4", style=filled, shape="record"]\n')

        f.write('\n')
        for block in cfg.block.values():            
            if len(block.edges) == 1:
                f.write(f'  node{block.label}->node{block.edges[0]}\n')
            if len(block.edges) == 2:
                f.write(f'  node{block.label}->node{block.edges[0]}[color=red]\n')
                f.write(f'  node{block.label}->node{block.edges[1]}[color=blue]\n')
                
        f.write('}')
    
    os.system(f'dot -Tpng {filename}.dot -o {filename}.png')

def print_domin(domin, filename):
    with open(f'{filename}.dot', 'w') as f:
        f.write('digraph cfg{\n')
        for u in domin.succ:
            for v in domin.succ[u]:
                f.write(f'  {u}->{v}\n')
        f.write('}')
    os.system(f'dot -Tpng {filename}.dot -o {filename}.png')

def print_df(cfg):
    for block in cfg.block.values():
        print(block.label, block.df)