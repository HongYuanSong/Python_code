__author__ = 'shy'
__date__ = '2018/3/22 22:45'

from 节点类 import LNode


class LList:
    def __init__(self):
        self.head = None

    def isEmpty(self):
        return self.head is None

    def prepend(self, elem):
        self.head = LNode(elem, self.head)

    def pop(self):
        if self.head is None:
            raise ValueError
        e = self.head.elem
        self.head = self.head.next
        return e

    def append(self, elem):
        if self.head is None:
            self.head = LNode(elem, None)
            return
        p = self.head
        while p.next is not None:
            p = p.next
        p.next = LNode(elem, None)

    def poplast(self):
        if self.head is None:  # empty list
            raise ValueError
        p = self.head
        if p.next is None:  # list with only one element
            e = p.elem
            self.head = None
            return e
        while p.next.next is not None:  # till p.next be last node
            p = p.next
        e = p.next.elem
        p.next = None
        return e

    def find(self, pred):
        p = self.head
        while p is not None:
            if pred(p.elem):
                return p.elem
            p = p.next
        return None

    def printall(self):
        p = self.head
        while p is not None:
            print(p.elem)
            p = p.next


if __name__ == '__main__':
    mlist1 = LList()

    for i in range(10):
        mlist1.prepend(i)

    for i in range(11, 20):
        mlist1.append(i)

    mlist1.printall()


# 带尾节点引用的链表
class LList1(LList):
    def __init__(self):
        LList.__init__(self)
        self.rear = None

    def prepend(self, elem):
        self.head = LNode(elem, self.head)
        if self.rear is None:  # empty list
            self.rear = self.head

    def append(self, elem):
        if self.rear is None:  # empty list
            self.prepend(elem)
        else:
            self.rear.next = LNode(elem, None)
            self.rear = self.rear.next

    def pop(self):
        if self.head is None:
            raise ValueError
        e = self.head.elem
        if self.rear is self.head:  # list with one node
            self.rear = None
        self.head = self.head.next
        return e

    def poplast(self):
        return None  # to be implemented


if __name__ == '__main__':
    mlist1 = LList1()
    for i in range(10):
        mlist1.prepend(i)

    for i in range(11, 20):
        mlist1.append(i)

    mlist1.printall()