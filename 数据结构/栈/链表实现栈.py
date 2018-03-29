__author__ = 'shy'
__date__ = '2018/3/23 12:59'


from 节点类 import LNode


class StackUnderflow(ValueError):  # 栈下溢（空栈访问）
    pass


class LStack: # stack implemented as a linked node list
    def __init__(self):
        self.top = None
        self.elems = []

    def is_empty(self):
        return self.top is None

    def top(self):
        if self.elems == []:
            raise StackUnderflow
        return self.top.elem

    def push(self, elem):
        self.top = LNode(elem, self.top)

    def pop(self):
        if self.top is None:
            raise StackUnderflow
        p = self.top
        self.top = p.next
        return p.elem