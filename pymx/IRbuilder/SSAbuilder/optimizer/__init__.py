""" optimize cfg """

from . import peephole
from .debug import print_cfg, print_domin
from .dominator import build_tree

def optimize(cfg, args):
    cfg = peephole.optimize(cfg)
    domin = build_tree(cfg)
    
    if args.debug:
        print_cfg(cfg)
        print_domin(domin)
    
    return cfg
