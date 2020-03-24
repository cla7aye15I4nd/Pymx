import traceback
from ..fakecode import Reg, Label

class Context:
    count = 0
    label_stack = []

    var_id = 0
    var_map = {}

    cur_prog = None
    cur_func = None
    cur_struct = None

    code = []
    branch = [] ## use for &&, ||

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
        self.count += 1
        new = '%{}'.format(self.count)
        reg = Reg(type, new)
        if name:
            self.var_map[name] = reg
        return reg

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

    def push_br(self, true, false):
        self.branch.append((true, false))
    
    def pop_br(self):
        self.branch.pop()

    def true_br(self):
        return self.branch[-1][0]
    
    def false_br(self):
        return self.branch[-1][1]

ctx = Context()