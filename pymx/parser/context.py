from ..errors import CompilerError

class Context:
    def __init__(self, tokens):        
        self.tokens = tokens
        self.current = 0
        self.savepoint = []

    def empty(self):
        return self.current == len(self.tokens)

    def save(self):
        self.savepoint.append(self.current)

    def restore(self):
        self.current = self.savepoint[-1]
        self.savepoint.pop()

    def prev(self):
        return self.tokens[self.current-1]
        
    def top(self):
        if self.empty():
            raise CompilerError('Unexpected EOF', range=self.prev().range)
        return self.tokens[self.current]

    def pop(self):
        top = self.top()
        self.current += 1
        return top
