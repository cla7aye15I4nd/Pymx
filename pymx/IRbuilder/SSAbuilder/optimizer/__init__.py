""" optimize cfg """

from . import peephole
from .dominator import build_tree
from .mem2reg import place_phi_node
from .constant_fold import constant_fold

from .debug import print_cfg, print_domin, print_df

def optimize(cfg, args):
    peephole.optimize(cfg)
    domin = build_tree(cfg)
    place_phi_node(cfg, domin)
    
    peephole.optimize(cfg)
    constant_fold(cfg)
    peephole.optimize(cfg)
    
    if args.debug:        
        print_cfg(cfg)
        print_domin(domin)
    
    return cfg
