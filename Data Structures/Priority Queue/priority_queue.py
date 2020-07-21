class PriorityQueue(object):
    def __init__(self, *args):
        self.queue = []
        [self.add_element(item) for item in args]

    def add_element(self, element):
        for index in range(0, len(self.queue)):
            if element[0] < self.queue[index][0]:
                self.queue.insert(index, element)
                break
        else:
            self.queue.append(element)

    def check_element(self, element):
        for index in range(0, len(self.queue)):
            if element == self.queue[index][1]:
                return index
        return -1

    def pop_element(self, index):
        return self.queue.pop(index)

    def delete_element(self, element):
        del self.queue[self.check_element(element)]

    def delete_at(self, index):
        del self.queue[index]