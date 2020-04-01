import heapq

class Heap:
    def __init__(self):
        self.data = []

    def push(self, val):
        heapq.heappush(self.data, val)

    def pop(self):
        return heapq.heappop(self.data)
    
    def top(self):        
        return self.data[0] if self.data else None

    def empty(self):
        return len(self.data) == 0
