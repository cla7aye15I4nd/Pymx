import traceback
from copy import deepcopy
from ..fakecode.types import Type
from ..fakecode import Reg, Label, Global
from ..fakecode.inst import Branch, Jump, Ret

class Context:
    count = 0
    string_count = 0
    label_stack = []

    var_id = 0
    var_map = {}
    global_var = {}

    cur_prog = None
    cur_func = None
    cur_struct = None

    gvar = []
    code = []
    branch = [] ## use for &&, ||
    struct = {}

    def clear(self):
        self.count = 0
        self.var_map.clear()
        self.label_stack.clear()
        self.code.clear()

    def get_label(self):
        self.count += 1
        label = Label(self.count)
        return label

    def get_var(self, type, name=None):
        if type.bit == 0:
            return None
        self.count += 1
        new = '%{}'.format(self.count)
        reg = Reg(type, new)
        if name:
            self.var_map[name] = reg
        return reg

    def find_var(self, name):
        if name in self.var_map:
            return self.var_map[name]
        return self.global_var[name]

    def break_label(self):
        if not self.label_stack:
            return None        
        return self.label_stack[-1][0]

    def continue_label(self):
        if not self.label_stack:
            return None        
        return self.label_stack[-1][1]

    def enter_loop(self):
        start, end = self.get_label(), self.get_label()
        self.label_stack.append((start, end))
        return start, end

    def exit_loop(self):
        self.label_stack.pop()

    def add(self, code):
        if type(code) is list:
            self.code += code
        else:
            self.code.append(code)

    def add_string_const(self, string_const):        
        self.string_count += 1
        name = f'.str.{self.string_count}'
        self.gvar.append(Global(Type(32, 4), name, 1, string_const))
        return Reg(Type(32, 4), '@' + name)

    def have_br(self):
        return len(self.branch) > 0

    def push_br(self, end):
        self.branch.append(end)
    
    def pop_br(self):
        res = self.branch[-1]
        self.branch.pop()
        return res
    
    def last_label(self):
        for inst in self.code[::-1]:
            if type(inst) is Label:
                return inst
            if type(inst) in [Branch, Jump, Ret]:
                return self.get_label()           
        return Label(0)
    
    def add_struct(self, struct):
        self.struct[struct.name] = struct

ctx = Context()