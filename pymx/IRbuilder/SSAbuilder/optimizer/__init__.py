""" optimize cfg """

from . import peephole

def optimize(cfg):
    cfg = peephole.optimize(cfg)
    return cfg