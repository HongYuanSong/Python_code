__author__ = 'shy'
__date__ = '2018/3/23 12:58'


class StackUnderflow(ValueError): # 栈下溢（空栈访问）
    pass


class SStack:
    def __init__(self):
        self.elems = []

    def is_empty(self):
        return self.elems == []

    def top(self):
        if self.elems == []:
            raise StackUnderflow
        return self.elems[len(self.elems) - 1]

    def push(self, elem):
        self.elems.append(elem)

    def pop(self):
        if self.elems == []:
            raise StackUnderflow
        return self.elems.pop()
