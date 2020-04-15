def alloc_register(cfg, reg_count):
    v2p = {}

    offset = 0
    for block in cfg.block.values():
        for inst in block.code:
            dest = inst.dest()
            if dest and type(dest.name) is str:
                if reg_count > 0:
                    reg_count -= 1
                    v2p[dest.name] = reg_count
                else:
                    offset -= 4
                    v2p[dest.name] = offset

    return v2p