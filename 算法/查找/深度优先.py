__author__ = 'shy'
__date__ = '2018/3/19 11:53'


class Node:
    def __int__(self):
        self.root = None
        self._left = None
        self._right = None


def dept_tree(node):
    if node is not None:
        if node._left is not None:
            return dept_tree(node._left)
        if node._right is not None:
            return dept_tree(node._right)
