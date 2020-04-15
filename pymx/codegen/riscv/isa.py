from .register import zero, ra, x6

# Instruction Base Object
class Instruction:
    def __str__(self):
        return 'unknown'

# Instruction Type Object
class Branch(Instruction):
    def __init__(self, mask, rs1, rs2, offset):
        self.mask = mask
        self.rs1 = rs1
        self.rs2 = rs2
        self.offset = offset

    def __str__(self):
        return f'  b{self.mask} {self.rs1}, {self.rs2}, {self.offset}\n'

class Load(Instruction):
    def __init__(self, mask, rd, rs, offset):
        self.mask = mask
        self.rd = rd
        self.rs = rs
        self.offset = offset

    def __str__(self):
        return f'  l{self.mask} {self.rd}, {self.offset}({self.rs})\n'

class Store(Instruction):
    def __init__(self, mask, rs2, rs1, offset):
        self.mask = mask
        self.rs2 = rs2
        self.rs1 = rs1
        self.offset = offset

    def __str__(self):
        return f'  s{self.mask} {self.rs2}, {self.offset}({self.rs1})\n'

class OPi(Instruction):
    def __init__(self, oper, rd, rs, imm):
        self.oper = oper
        self.rd = rd
        self.rs = rs
        self.imm = imm
    
    def __str__(self):
        return f'  {self.oper} {self.rd}, {self.rs}, {self.imm}\n'

class OPr(Instruction):
    def __init__(self, oper, rd, rs1, rs2):
        self.oper = oper
        self.rd = rd
        self.rs1 = rs1
        self.rs2 = rs2

    def __str__(self):
        return f'  {self.oper} {self.rd}, {self.rs1}, {self.rs2}\n'

# RV32I Base Integer Instruction Set
class LUI(Instruction):
    def __init__(self, rd, imm):
        self.rd = rd
        self.imm = imm

    def __str__(self):
        return f'  lui {self.rd}, {self.imm}\n'

class AUIPC(Instruction):
    def __init__(self, rd, offset):
        self.rd = rd
        self.offset = offset

    def __str__(self):
        return f'  auipc {self.rd}, {self.offset}\n'

class JAL(Instruction):
    def __init__(self, rd, offset):
        self.rd = rd
        self.offset = offset

    def __str__(self):
        return f'  jal {self.rd}, {self.offset}'

class JALR(Instruction):
    def __init__(self, rd, rs, offset):
        self.rd = rd
        self.rs = rs
        self.offset = offset

    def __str__(self):
        return f'  jalr {self.rd}, {self.rs}, {self.offset}\n'

class BEQ(Branch):
    def __init__(self, rs1, rs2, offset):
        super().__init__('eq', rs1, rs2, offset)

class BNE(Branch):
    def __init__(self, rs1, rs2, offset):
        super().__init__('ne', rs1, rs2, offset)

class BLT(Branch):
    def __init__(self, rs1, rs2, offset):
        super().__init__('lt', rs1, rs2, offset)

class BGE(Branch):
    def __init__(self, rs1, rs2, offset):
        super().__init__('ge', rs1, rs2, offset)

class BLTU(Branch):
    def __init__(self, rs1, rs2, offset):
        super().__init__('ltu', rs1, rs2, offset)

class BGEU(Branch):
    def __init__(self, rs1, rs2, offset):
        super().__init__('geu', rs1, rs2, offset)

class LB(Load):
    def __init__(self, rd, rs, offset):
        super().__init__('b', rd, rs, offset)

class LH(Load):
    def __init__(self, rd, rs, offset):
        super().__init__('h', rd, rs, offset)

class LW(Load):
    def __init__(self, rd, rs, offset):
        super().__init__('w', rd, rs, offset)

class LBU(Load):
    def __init__(self, rd, rs, offset):
        super().__init__('bu', rd, rs, offset)

class LHU(Load):
    def __init__(self, rd, rs, offset):
        super().__init__('hu', rd, rs, offset)

class SB(Store):
    def __init__(self, rs2, rs1, offset):
        super().__init__('b', rs2, rs1, offset)

class SH(Store):
    def __init__(self, rs2, rs1, offset):
        super().__init__('h', rs2, rs1, offset)

class SW(Store):
    def __init__(self, rs2, rs1, offset):
        super().__init__('w', rs2, rs1, offset)

class ADDI(OPi):
    def __init__(self, rd, rs, imm):
        super().__init__('addi', rd, rs, imm)

class SLTI(OPi):
    def __init__(self, rd, rs, imm):
        super().__init__('slti', rd, rs, imm)

class SLTIU(OPi):
    def __init__(self, rd, rs, imm):
        super().__init__('sltiu', rd, rs, imm)

class XORI(OPi):
    def __init__(self, rd, rs, imm):
        super().__init__('xori', rd, rs, imm)

class ORI(OPi):
    def __init__(self, rd, rs, imm):
        super().__init__('ori', rd, rs, imm)

class ANDI(OPi):
    def __init__(self, rd, rs, imm):
        super().__init__('andi', rd, rs, imm)

class SLLI(OPi):
    def __init__(self, rd, rs, imm):
        super().__init__('slli', rd, rs, imm)

class SRLI(OPi):
    def __init__(self, rd, rs, imm):
        super().__init__('srli', rd, rs, imm)

class SRAI(OPi):
    def __init__(self, rd, rs, imm):
        super().__init__('srai', rd, rs, imm)

class ADD(OPr):
    def __init__(self, rd, rs1, rs2):
        super().__init__('add', rd, rs1, rs2)

class SUB(OPr):
    def __init__(self, rd, rs1, rs2):
        super().__init__('sub', rd, rs1, rs2)

class SLL(OPr):
    def __init__(self, rd, rs1, rs2):
        super().__init__('sll', rd, rs1, rs2)

class SLT(OPr):
    def __init__(self, rd, rs1, rs2):
        super().__init__('slt', rd, rs1, rs2)

class SLTU(OPr):
    def __init__(self, rd, rs1, rs2):
        super().__init__('sltu', rd, rs1, rs2)

class XOR(OPr):
    def __init__(self, rd, rs1, rs2):
        super().__init__('xor', rd, rs1, rs2)

class SRL(OPr):
    def __init__(self, rd, rs1, rs2):
        super().__init__('srl', rd, rs1, rs2)

class SRA(OPr):
    def __init__(self, rd, rs1, rs2):
        super().__init__('sra', rd, rs1, rs2)

class OR(OPr):
    def __init__(self, rd, rs1, rs2):
        super().__init__('or', rd, rs1, rs2)

class AND(OPr):
    def __init__(self, rd, rs1, rs2):
        super().__init__('and', rd, rs1, rs2)

# RV32M Standard Extension for Integer Multiply and Divide
class MUL(OPr):
    def __init__(self, rd, rs1, rs2):
        super().__init__('mul', rd, rs1, rs2)

class MULH(OPr):
    def __init__(self, rd, rs1, rs2):
        super().__init__('mulh', rd, rs1, rs2)

class MULHSU(OPr):
    def __init__(self, rd, rs1, rs2):
        super().__init__('mulhsu', rd, rs1, rs2)

class MULHU(OPr):
    def __init__(self, rd, rs1, rs2):
        super().__init__('mulhu', rd, rs1, rs2)

class DIV(OPr):
    def __init__(self, rd, rs1, rs2):
        super().__init__('div', rd, rs1, rs2)

class DIVU(OPr):
    def __init__(self, rd, rs1, rs2):
        super().__init__('divu', rd, rs1, rs2)

class REM(OPr):
    def __init__(self, rd, rs1, rs2):
        super().__init__('rem', rd, rs1, rs2)

class REMU(OPr):
    def __init__(self, rd, rs1, rs2):
        super().__init__('remu', rd, rs1, rs2)

# Pseudo-instruction
class LI(LUI):
    def __init__(self, rd, expr):
        super().__init__(rd, expr)

    def __str__(self):
        return f'  li {self.rd}, {self.imm}\n'

class LA(LUI):
    def __init__(self, rd, addr):
        super().__init__(rd, addr)

    def __str__(self):
        return f'  la {self.rd}, {self.imm}\n'

class MV(ADDI):
    def __init__(self, rd, rs):
        super().__init__(rd, rs, 0)
    
    def __str__(self):
        return f'  mv {self.rd}, {self.rs}\n'

class NOT(XORI):
    def __init__(self, rd, rs):
        super().__init__(rd, rs, -1)

    def __str__(self):
        return f'  not {self.rd}, {self.rs}\n'

class NEG(SUB):
    def __init__(self, rd, rs):
        super().__init__(rd, zero, rs)

    def __str__(self):
        return f'  neg {self.rd}, {self.rs2}\n'

class SEQZ(SLTIU):
    def __init__(self, rd, rs):
        super().__init__(rd, rs, 1)

    def __str__(self):
        return f'  seqz {self.rd}, {self.rs}\n'

class SNEZ(SLTU):
    def __init__(self, rd, rs):
        super().__init__(rd, zero, rs)

    def __str__(self):
        return f'  snez {self.rd}, {self.rs2}\n'

class SLTZ(SLT):
    def __init__(self, rd, rs):
        super().__init__(rd, rs, zero)

    def __str__(self):
        return f' sltz {self.rd}, {self.rs1}\n'

class SGTZ(SLT):
    def __init__(self, rd, rs):
        super().__init__(rd, rs, zero)

    def __str__(self):
        return f' sgtz {self.rd}, {self.rs1}\n'

class BEQZ(BEQ):
    def __init__(self, rs, offset):
        super().__init__(rs, zero, offset)

    def __str__(self):
        return f'  beqz {self.rs1}, {self.offset}\n'

class BNEZ(BNE):
    def __init__(self, rs, offset):
        super().__init__(rs, zero, offset)

    def __str__(self):
        return f'  bnez {self.rs1}, {self.offset}\n'

class BLEZ(BGE):
    def __init__(self, rs, offset):
        super().__init__(zero, rs, offset)

    def __str__(self):
        return f'  bge {self.rs2}, {self.offset}\n'

class BGEZ(BGE):
    def __init__(self, rs, offset):
        super().__init__(rs, zero, offset)

    def __str__(self):
        return f'  bge {self.rs1}, {self.offset}\n'

class BLTZ(BLT):
    def __init__(self, rs, offset):
        super().__init__(rs, zero, offset)

    def __str__(self):
        return f'  bltz {self.rs1}, {self.offset}\n'

class BGTZ(BLT):
    def __init__(self, rs, offset):
        super().__init__(zero, rs, offset)

    def __str__(self):
        return f'  bgtz {self.rs2}, {self.offset}\n'

class BGT(BLT):
    def __init__(self, rs, rt, offset):
        super().__init__(rt, rs, offset)

    def __str__(self):
        return f'  bgt {self.rs2}, {self.rs1}, {self.offset}\n'

class BLE(BGE):
    def __init__(self, rs, rt, offset):
        super().__init__(rt, rs, offset)

    def __str__(self):
        return f'  ble {self.rs2}, {self.rs1}, {self.offset}\n'

class BGTU(BLTU):
    def __init__(self, rs, rt, offset):
        super().__init__(rt, rs, offset)

    def __str__(self):
        return f'  bgtu {self.rs2}, {self.rs1}, {self.offset}\n'

class BLEU(BGEU):
    def __init__(self, rs, offset):
        super().__init__(zero, rs, offset)

    def __str__(self):
        return f'  bgtu {self.rs2}, {self.offset}\n'

class J(JAL):
    def __init__(self, offset):
        super().__init__(zero, offset)

    def __str__(self):
        return f'  j {self.offset}\n'

class JR(JAL):
    def __init__(self, offset):
        super().__init__(zero, ra)

    def __str__(self):
        return f'  j {self.offset}\n'

class Ret(JALR):
    def __init__(self):
        super().__init__(zero, ra, 0)

    def __str__(self):
        return '  ret\n'

class CALL(JALR):
    def __init__(self, offset):
        super().__init__(ra, x6, offset)

    def __str__(self):
        return f'  call {self.offset}\n'

class TAIL(JALR):
    def __init__(self, offset):
        super().__init__(zero, x6, offset)

    def __str__(self):
        return f'  tail {self.offset}\n'
