from pymx.fakecode import Label
from pymx.fakecode.inst import Ret, Phi, Jump
from ..cfg import Block

def optimize(cfg):
    ret_stmt = []
    for block in cfg.block.values():
        ret = block.code[-1]
        if type(ret) is Ret and ret.reg:
            ret_stmt.append((ret.reg, Label(block.label)))
    
    if len(ret_stmt) > 1:        
        cfg.count += 1
        block = Block(cfg.count)

        reg = cfg.get_var(ret_stmt[0][0])
        block.add_inst(Phi(reg, ret_stmt))
        block.add_inst(Ret(reg))
        cfg.add_block(block)

        for _, blk in ret_stmt:
            cfg.block[blk.label].code[-1] = Jump(Label(block.label))
            