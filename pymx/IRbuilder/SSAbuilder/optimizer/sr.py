""" Strength reduction """
from pymx.fakecode import Const
from pymx.fakecode.inst import Branch, Logic, Arith

def optimize(cfg):
    for block in cfg.block.values():
        code = block.code
        if len(code) > 2 and type(code[-1]) is Branch and type(code[-2]) is Logic:        
            cond = code[-1].var

            logic = code[-2]
            dest = logic.dst

            if cond == dest:
                var = None
                if type(logic.rhs) is Const:
                    var =logic.lhs
                for inst in code:
                    if (inst.dest() == var and type(inst) is Arith and
                            inst.oper == 'and' and type(inst.rhs) is Const and
                                bin(inst.rhs.name).count('1') == 1):
                        if logic.oper == 'eq' and logic.rhs.name == inst.rhs.name:
                           logic.oper = 'ne'
                           logic.rhs.name = 0
                            