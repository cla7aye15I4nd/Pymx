import os

def print_info(code):
    for i, info in enumerate(code.seq):
        errno = '{}: {}\n'.format(i, str(info.inst).strip())
        errno += f"  [use]: {' '.join([r.__str__() for r in info.uses])}\n"
        errno += f"  [def]: {' '.join([r.__str__() for r in info.defs])}\n"
        errno += f"  [in ]: {' '.join([r.__str__() for r in info.in_set])}\n"
        errno += f"  [out]: {' '.join([r.__str__() for r in info.out_set])}\n"
        print(errno)

def print_graph(graph, filename):
    with open(f'{filename}_register.dot', 'w') as f:
        f.write('graph {\nremincross=false\n')
        for u in graph:
            if graph[u].color is not None:
                color = hex(0xffff00 - 0x012033 * graph[u].color)[2:].rjust(6, '0')
                f.write(f'{u}[color="#{color}", style=filled]\n')
        for u in graph:
            for v in graph[u].edge:
                if u > v:
                    f.write(f'{u}--{v}\n')
            for v in graph[u].move:
                if u > v:
                    f.write(f'{u}--{v}[style=dashed]\n')
        f.write('}\n')
    os.system(f'dot -Tpng {filename}_register.dot -o {filename}_regster.png')