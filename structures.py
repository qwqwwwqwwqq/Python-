class Stack:

    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        if self.is_empty():
            return None
        return self._items.pop()

    def peek(self):
        if self.is_empty():
            return None
        return self._items[-1]

    def is_empty(self):
        return len(self._items) == 0

    def size(self):
        return len(self._items)

    def __repr__(self):
        return f"Stack({self._items})"


class TreeNode:

    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

    def is_leaf(self):
        return self.left is None and self.right is None

    def insert(self, node):
        if self.left is None:
            self.left = node
            return True
        if self.right is None:
            self.right = node
            return True
        return False

    def __repr__(self):
        if self.is_leaf():
            return str(self.value)
        return f"({self.left} {self.value} {self.right})"