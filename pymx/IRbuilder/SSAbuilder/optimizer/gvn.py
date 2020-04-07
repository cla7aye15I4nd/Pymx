"""
    DVNT_GVN(block b):
    for each phi node in b:
        remove and continue if meaningless or redundant
        set the value number for the remaining phi node to be the assigned variable name
        add phi node to the hash table

    for each assignment:
        get value numbers for each operand
        simplify the expression if possible
        if the expression has been computed before:
        set the value number for the assigned variable to the expression's value number
        else:
        set the value number for the expression to be the assigned variable name
        add the expression to the hash table

    for each child c of b in the control flow graph:
        replace all phi node operands in c that were computed in this block with their value numbers

    for each child c of b in the dominator tree:
        DVNT_GVN(c)

    remove all values hashed during this function call
"""

from copy import deepcopy
from pymx.parser.operators import swap_able

from pymx.fakecode import Const, Reg
from pymx.fakecode.inst import (
    Alloca, Ret, Load, Store, Call, Malloc,
    Branch, Jump, Phi, Arith, Logic
)

from .dominator import build_tree

class VExpr:
    def __init__(self, oper, left, right):
        self.oper = oper
        self.left = left
        self.right = right

    def __hash__(self):
        if self.oper in swap_able:
            hash_x = hash((self.oper, (self.left, self.right)))
            hash_y = hash((self.oper, (self.right, self.left)))
            return min(hash_x, hash_y)
        else:
            return hash((self.oper, (self.left, self.right)))

    def __eq__(self, other):
        if self.oper != other.oper:
            return False
        if self.oper in swap_able:
            return {self.left, self.right} == {other.left, other.right}
        else:
            return (self.left, self.right) == (other.left, other.right)

def optimize(cfg):
    cfg.compute_graph()
    domin = build_tree(cfg)
    gvn_pass(cfg, domin, 0, {}, {})

def replace_phi_operands(block, vn, tb):
    for inst in list(block.code):
        if type(inst) is not Phi:
            break
        if try_replace(inst, vn, tb):
            block.code.remove(inst)
    
def gvn_pass(cfg, domin, bid, vn, tb):
    block = cfg.block[bid]
    for inst in list(block.code):
        if try_replace(inst, vn, tb):
            block.code.remove(inst)

    for succ in block.edges:
        replace_phi_operands(cfg.block[succ], vn, tb)
    for succ in domin.succ[bid]:
        gvn_pass(cfg, domin, succ, deepcopy(vn), deepcopy(tb))

def try_replace(inst, vn, tb):
    def replace_hook(obj):
        if obj and obj.name in tb:
            return deepcopy(tb[obj.name])
        return obj
    
    if type(inst) is Store:
        inst.src = replace_hook(inst.src)
        inst.dst = replace_hook(inst.dst)

    if type(inst) is Load:
        inst.src = replace_hook(inst.src)                    

    if type(inst) is Branch:
        inst.var = replace_hook(inst.var)        
    
    if type(inst) is Ret:
        inst.reg = replace_hook(inst.reg)                
    
    if type(inst) in [Arith, Logic]:
        inst.lhs = replace_hook(inst.lhs) 
        inst.rhs = replace_hook(inst.rhs)

    if type(inst) in [Call, Malloc]:
        inst.params = [replace_hook(par) for par in inst.params]
    
    if type(inst) is Phi:
        inst.units = [(replace_hook(unit[0]), unit[1]) for unit in inst.units]

    value = value_number(inst, vn)
    if value is not None:
        if value in vn:            
            tb[inst.dest().name] = vn[value]
            return True        
        vn[value] = inst.dest()
    
    return False

def value_number(obj, vn):
    if type(obj) is Const:
        return obj.name
    if type(obj) is Reg:
        if obj.name in vn:
            return vn[obj.name]
        else:    
            return None    
    if type(obj) is Arith:        
        return VExpr(obj.oper, obj.lhs.name, obj.rhs.name)

    return None
