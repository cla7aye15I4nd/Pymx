"""" build SSA """

from .cfg import build_CFG
from .optimizer import optimize

def build_SSA(func):
    cfg = optimize(build_CFG(func.code))
    func.code = cfg.serial()
