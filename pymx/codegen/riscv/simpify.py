from .isa import (
    MV, 
    CALL, TAIL, Ret
)

def simpify(bb):
    erase_useless_move(bb)
    tail_call_optimize(bb)

def erase_useless_move(bb):
    last = None
    for inst in list(bb.code):
        if type(inst) is MV:
            if inst.rs == inst.rd:
                bb.code.remove(inst)
            elif type(last) is MV and inst.flag:
                bb.code.remove(inst)
            elif type(last) is MV and (inst.rs, inst.rd) == (last.rd, last.rs):
                bb.code.remove(inst)
        last = inst

def tail_call_optimize(bb):
    i = 1
    while i < len(bb.code):
        inst = bb.code[i]
        last = bb.code[i-1]
        if type(inst) is Ret and type(last) is CALL:
            bb.code[i-1] = TAIL(last.offset, inst.count)
            bb.code.remove(inst)
        else:
            i += 1