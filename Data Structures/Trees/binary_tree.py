class Node(object):
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


class Tree(object):
    def __init__(self, root):
        self.root = Node(root)

    def add_node(self, value):
        current_node = self.root
        while current_node:
            if value > current_node.value:
                if current_node.right:
                    current_node = current_node.right
                else:
                    current_node.right = Node(value)
                    break
            else:
                if current_node.left:
                    current_node = current_node.left
                else:
                    current_node.left = Node(value)
                    break

    def add_node_recursively(self, value, node=None):
        if not node:
            node = self.root
        if value > node.value and node.right:
            self.add_node_recursively(value, node.right)
        elif value > node.value and not node.right:
            node.right = Node(value)
        elif value <= node.value and node.left:
            self.add_node_recursively(value, node.left)
        elif value <= node.value and not node.left:
            node.left = Node(value)

    def breadth_first_traversal(self):
        queue = [self.root]
        values = []
        while len(queue) != 0:
            first_item = queue.pop(0)
            values.append(first_item.value)
            if first_item.left:
                queue.append(first_item.left)
            if first_item.right:
                queue.append(first_item.right)
        return values

    def depth_first_traversal(self):
        stack = [self.root]
        values = []
        while len(stack) != 0:
            first_item = stack.pop()
            values.append(first_item.value)
            if first_item.right:
                stack.append(first_item.right)
            if first_item.left:
                stack.append(first_item.left)
        return values
