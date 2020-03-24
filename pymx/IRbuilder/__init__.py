""" IRbuilder """

from .context import ctx
from . import builder

def IRbuild(tree):
    ctx.clear()
    return tree.build(builder)