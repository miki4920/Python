class Node(object):
    def __init__(self, value, next_node=None):
        self.value = value
        self.next = next_node

    def __str__(self):
        return str(self.value)


class LinkedList(object):
    def __init__(self, head):
        self.head = Node(head)
        self.length = 1

    def get_tail(self):
        current_node = self.head
        while current_node.next:
            current_node = current_node.next
        return current_node

    def search_list(self, key):
        current_node = self.head
        current_index = 0
        while current_node.next:
            if current_node.value == key:
                return current_index
            current_node = current_node.next
            current_index += 1
        if current_node.value == key:
            return current_index
        return -1

    def print_list(self):
        current_node = self.head
        while current_node:
            print(current_node)
            current_node = current_node.next

    def add_item_to_start(self, value):
        current_node = Node(value)
        current_node.next = self.head
        self.head = current_node
        self.length += 1

    def add_item_to_end(self, value):
        end_node = self.get_tail()
        end_node.next = Node(value)
        self.length += 1

    def add_item_to_index(self, value, index):
        if index >= self.length:
            self.add_item_to_end(value)
        elif index == 0:
            self.add_item_to_start(value)
        else:
            current_node = self.head
            current_index = 0
            while current_node.next:
                if current_index == index:
                    node = Node(value)
                    node.next = current_node.next
                    current_node.next = node
                    break
                current_index += 1
                current_node = current_node.next
            self.length += 1

    def delete_start(self):
        self.head = self.head.next
        self.length -= 1

    def delete_end(self):
        current_node = self.head
        while current_node.next.next:
            current_node = current_node.next
        current_node.next = None
        self.length -= 1

    def delete_index(self, index):
        if index >= self.length:
            self.delete_end()
        elif index == 0:
            self.delete_start()
        else:
            current_node = self.head
            current_index = 0
            while current_node.next:
                if current_index+1 == index:
                    current_node.next = current_node.next.next
                    break
                current_index += 1
                current_node = current_node.next
            self.length -= 1

    def delete_value(self, value):
        index = self.search_list(value)
        if index >= 0:
            self.delete_index(index)
        else:
            print(f"Value: {value} is not in the linked list")
