""" IRbuilder """

from . import builder
from .context import ctx
from .SSAbuilder import build_SSA

def IRbuild(tree, args):
    ctx.clear()
    obj = tree.build(builder)
    for func in obj.func:
        build_SSA(func, args)
    return obj