""" static checker """

from .context import ctx
from . import checker

def semantic_check(tree):    
    ctx.clear()
    tree.check(checker)