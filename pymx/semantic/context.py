import traceback

class Context:
    label_id = 0
    var_stack = []
    label_stack = []

    cur_prog = None
    cur_func = None
    cur_struct = None

    def clear(self):
        self.label_id = 0
        self.var_stack.clear()
        self.label_stack.clear()

    def get_label(self):
        label = f'L{self.label_id}:'
        self.label_id = self.label_id + 1
        return label

    def break_label(self):
        if not self.label_stack:
            return None        
        return self.label_stack[-1][0]

    def continue_label(self):
        if not self.label_stack:
            return None        
        return self.label_stack[-1][1]

    def add_variable(self, decl):
        depth = len(self.var_stack) 
        name = decl.var_name.text
        if depth == 1:
            new_name = name
        else:
            new_name = '{}_{}'.format(name, depth)
        
        self.var_stack[-1][name] = decl
        self.var_stack[-1][name].var_name.text = new_name
        return new_name

    def find_variable(self, name):
        for scope in self.var_stack[::-1]:
            if name in scope:
                return scope[name]
        return None

    def enter_scope(self):
        self.var_stack.append({})
    
    def exit_scope(self):
        self.var_stack.pop()

    def enter_loop(self):
        start, end = self.get_label(), self.get_label()
        self.label_stack.append((start, end))
        return start, end

    def exit_loop(self):
        self.label_stack.pop()

ctx = Context()

class Scope:
    def __enter__(self):
        ctx.enter_scope()
        return self
    
    def __exit__(self, exc_type, exc_value, exc_tb):
        if exc_tb:
            traceback.print_tb(exc_tb)
        ctx.exit_scope()
        return True