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

class Expr:
    def __init__(self, oper, left, right):
        self.oper = oper
        if oper in swap_able:
            self.args = []
            if (type(left) is Expr and left.oper == oper):
                self.args += left.args
            else:
                self.args.append(left)

            if (type(right) is Expr and right.oper == oper):
                self.args += right.args
            else:
                self.args.append(right)

            arg_int = [e for e in self.args if type(e) is int]
            arg_other = [e for e in self.args if type(e) is not int]

            if oper == 'add':
                res = sum(arg_int)
                if res != 0 or not arg_other:
                    arg_other.append(res)
                self.args = arg_other                
        else:
            self.args = [left, right]
            
        self.hash = hash((self.oper, hash_args(self.args, self.oper)))

    def __str__(self):
        return '( {} {} )'.format(self.oper, [x.__str__() for x in self.args])

    def __hash__(self):
        return self.hash

    def __eq__(self, other):
        if type(other) is not Expr:
            return False
        return self.oper == other.oper and self.args == other.args

    def get(self):
        if len(self.args) > 1:
            return self
        return self.args[0]

def hash_args(args, oper):
    if type(args) is list:
        if oper in swap_able:
            return hash(tuple(sorted([hash(x) for x in args])))
        else:
            return hash(tuple(args))
    return hash(args)

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
        if obj and obj.name in tb and tb[obj.name] in vn:
            return deepcopy(vn[tb[obj.name]])
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

    value = value_number(inst, tb)
    if inst.dest():     
        vn[inst.dst.name] = inst.dst
    if value is not None:           
        tb[inst.dst.name] = value
        if value in vn:            
            return True        
        vn[value] = inst.dest()
    
    return False

def value_number(obj, tb):
    if type(obj) is Const:
        return obj.name
    if type(obj) is Reg:
        if obj.name in tb:
            return tb[obj.name]
        else:    
            return obj.name
    if type(obj) is Arith:
        lhs = value_number(obj.lhs, tb)
        rhs = value_number(obj.rhs, tb)
        return Expr(obj.oper, lhs, rhs).get()
    if type(obj) is Logic:
        lhs = value_number(obj.lhs, tb)
        rhs = value_number(obj.rhs, tb)
        return Expr(obj.oper, lhs, rhs).get()

    return None
