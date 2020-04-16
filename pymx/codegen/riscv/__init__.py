""" riscv """

from .code import build_func

class AsmCode:
    def __init__(self):
        self.text = []

    def add_text(self, text):
        self.text.append(text)

    def __str__(self):
        code = ".text\n.globl main\n"
        code += '\n'.join(text.__str__() for text in self.text)
        return code

def build(ir, args):

    asm_code = AsmCode()
    for func in ir.func:
        asm_code.add_text(build_func(func, args))

    return asm_code
