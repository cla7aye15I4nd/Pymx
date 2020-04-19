""" riscv """

from .code import build_func
from .data import build_data

class AsmCode:
    def __init__(self):
        self.text = []
        self.data = []

    def add_text(self, text):
        self.text.append(text)
    
    def add_data(self, data):
        self.data.append(data)

    def __str__(self):
        code = ".text\n.globl main\n"
        code += '\n'.join(text.__str__() for text in self.text) + '\n'

        code += '.data\n'
        code += '\n'.join(data.__str__() for data in self.data)
        return code

def build(ir, args):
    asm_code = AsmCode()
    for func in ir.func:
        asm_code.add_text(build_func(func, args))
    for data in ir.vars:
        asm_code.add_data(build_data(data, args))

    return asm_code
