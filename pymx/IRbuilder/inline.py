from copy import deepcopy

from pymx.IRbuilder.SSAbuilder.cfg import build_CFG
from pymx.IRbuilder.SSAbuilder import optimizer

from pymx.fakecode import Label, Reg, Const
from pymx.fakecode.inst import (
    Store, Branch, Ret, Phi, Jump,
    Load, Call, Malloc, Arith, Logic
)

def try_inline(prog, func, args):    
    flag = False
    mask = True
    function = deepcopy(func)
    count = max(len(func.name) // 5, 1)
    
    while count > 0 and mask:        
        function, mask = _try_inline(prog, function, args)
        
        count -= 1
        flag |= mask

    if flag:
        func.code = function.code
        cfg = build_CFG(func, args)    
        
        optimizer.peephole.optimize(cfg)
        optimizer.constant_fold(cfg)
        optimizer.dce.optimize(cfg)
        optimizer.peephole.optimize(cfg)            
                
        func.code = cfg.serial()           

def _try_inline(prog, func, args):
    inline_threshold = 50

    max_id = 0
    replace_map = {}
    label_map = {}

    def replace_hook(obj):        
        if type(obj) is Label:
            if obj.label not in replace_map:
                replace_map['max_id'] += 1
                replace_map[obj.label] = replace_map['max_id']
            obj.label = replace_map[obj.label]
            return obj

        if type(obj) is Reg:
            if obj.name[0] == '@':
                return obj
            if obj.name not in replace_map:
                replace_map['max_id'] += 1
                new_name = f"%{replace_map['max_id']}"
                replace_map[obj.name] = new_name
            
            val = replace_map[obj.name]
            if type(val) is int:
                return Const(obj.type, val)
            obj.name = val
            return obj

        return obj

    for inst in func.code:
        if type(inst) is Label:
            max_id = max(max_id, inst.label)
        elif inst.dest():
            max_id = max(max_id, int(inst.dest().name[1:]))
    replace_map['max_id'] = max_id

    code = []
    do_inline = False

    last_label = -1
    for inst in func.code:
        if type(inst) is Label:
            last_label = inst.label
        if type(inst) is Call and prog[inst.name]:            
            call_func = prog[inst.name]
            if len(call_func.code) > inline_threshold:
                code.append(inst)
            elif inst.dest() is None:   
                do_inline = True       

                inner_code = deepcopy(call_func.code)
                max_id = replace_map['max_id']
                replace_map.clear()

                max_id += 1
                end_call = Label(max_id)
                label_map[last_label] = max_id

                replace_map['max_id'] = max_id
                for idx, par in enumerate(inst.params):
                    replace_map[f'%{idx}'] = par.name                
                for cmd in inner_code:
                    if type(cmd) is Ret:
                        code.append(Jump(end_call))
                    else:
                        replace(cmd, replace_hook)
                        if type(cmd) is Label and type(code[-1]) is Label:
                            code.append(Jump(cmd))
                        code.append(cmd)

                code.append(end_call)
            else:
                inner_code = deepcopy(call_func.code)
                ret_count = 0

                for _ in inner_code:
                    if type(_) is Ret:                        
                        ret_count += 1
                
                if ret_count == 1:             
                    do_inline = True       
                    max_id = replace_map['max_id']
                    replace_map.clear()

                    max_id += 1
                    end_call = Label(max_id)
                    label_map[last_label] = max_id

                    replace_map['max_id'] = max_id                    
                    for idx, par in enumerate(inst.params):
                        replace_map[f'%{idx}'] = par.name                
                    for cmd in inner_code:
                        if type(cmd) is Ret:
                            replace(cmd, replace_hook)
                            code.append(Arith(inst.dst, '+', cmd.reg, Const(inst.dst.type, 0)))
                            code.append(Jump(end_call))
                        else:
                            replace(cmd, replace_hook)
                            if type(cmd) is Label and type(code[-1]) is Label:
                                code.append(Jump(cmd))
                            code.append(cmd)

                    code.append(end_call)
                else:
                    code.append(inst)
        else:
            code.append(inst)            

    for inst in code:
        if type(inst) is Phi:
            for unit in inst.units:
                if unit[1].label in label_map:
                    unit[1].label = label_map[unit[1].label]
    
    if do_inline:
        func.code = code
             

    return func, do_inline

def replace(inst, replace_hook):
    if type(inst) is Store:
        inst.src = replace_hook(inst.src)
        inst.dst = replace_hook(inst.dst)

    if type(inst) is Load:
        inst.dst = replace_hook(inst.dst)
        inst.src = replace_hook(inst.src)

    if type(inst) is Branch:
        inst.var = replace_hook(inst.var)
        inst.true = replace_hook(inst.true)
        inst.false = replace_hook(inst.false)

    if type(inst) is Jump:
        inst.label = replace_hook(inst.label)

    if type(inst) is Ret:
        inst.reg = replace_hook(inst.reg)
    
    if type(inst) in [Arith, Logic]:
        inst.dst = replace_hook(inst.dst)
        inst.lhs = replace_hook(inst.lhs) 
        inst.rhs = replace_hook(inst.rhs)

    if type(inst) in [Call, Malloc]:
        inst.dst = replace_hook(inst.dst)
        inst.params = [replace_hook(par) for par in inst.params]
    
    if type(inst) is Phi:
        inst.dst = replace_hook(inst.dst)
        inst.units = [(replace_hook(unit[0]), replace_hook(unit[1])) for unit in inst.units]

    if type(inst) is Label:
        replace_hook(inst)