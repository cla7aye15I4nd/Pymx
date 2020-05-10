""" optimize cfg """

from . import peephole, gvn, dce, fmt, glo, sr, mem2reg
from .dominator import build_tree
from .constant_fold import constant_fold

from .debug import print_cfg, print_domin, print_df

def optimize(cfg, args):
    fmt.optimize(cfg)
    glo.optimize(cfg)

    peephole.optimize(cfg)
    domin = build_tree(cfg)
    
    mem2reg.place_phi_node(cfg, domin)
    peephole.optimize(cfg)

    gvn.optimize(cfg)
    constant_fold(cfg)
    peephole.optimize(cfg)
    
    sr.optimize(cfg)
    dce.optimize(cfg)    

    cfg._serial()
    
    code = cfg.serial()
    if args.debug:
        try:
            print_cfg(cfg, f'cfg_{cfg.name}')
            print_domin(domin, f'domin_{cfg.name}')
        except Exception as err:
            print('[ERROR] debug fail at optimizer', err)            
    
    return code
