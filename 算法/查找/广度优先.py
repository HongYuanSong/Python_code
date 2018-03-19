author = 'shy'
date = '2018/3/19 11:53'


class Node:
    def __int__(self, value, left, right):
        self.value = value
        self.left = left
        self.right = right
        

def level_depth(root):
    if root is not None:
        q = []
        node = root
        q.append(node)
        while q:
            node = q.pop(0)
            if node.left is not None:
                q.append(node.left)
            if node.right is not None:
                q.append(node.right)
            