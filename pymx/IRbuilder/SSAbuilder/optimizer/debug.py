import os

def print_cfg(cfg):
    with open('cfg.dot', 'w') as f:
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
    
    os.system('dot -Tpng cfg.dot -o cfg.png')

def print_domin(domin):
    with open('domin.dot', 'w') as f:
        f.write('digraph cfg{\n')
        for u in domin:
            for v in domin[u]:
                f.write(f'  {u}->{v}\n')
        f.write('}')
    os.system('dot -Tpng domin.dot -o domin.png')