"""" build SSA """

from .cfg import build_CFG
from .optimizer import optimize

def build_SSA(func, args):
    cfg = build_CFG(func, args)    
    func.code = optimize(cfg, args)
