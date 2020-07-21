class Node(object):
    def __init__(self, label):
        self.label = label
        self.neighbours = {}

class Graph(object):
    def __init__(self):
        self.graph = []

    def add_node(self, label):
        self.graph.append(Node(label))

    def find_node(self, label):
        for node in self.graph:
            if node.label == label:
                return node

    def return_nodes(self):
        return [node for node in self.graph]

    def add_edge(self, first_label, second_label, value):
        first_node = self.find_node(first_label)
        second_node = self.find_node(second_label)
        first_node.neighbours[second_node] = value
        second_node.neighbours[first_node] = value

    def find_shortest_path(self, first_label, second_label):
        first_node = self.find_node(first_label)
        second_node = self.find_node(second_label)
        unvisited = self.return_nodes()
        dictionary = {}
        current_node = first_node
        for node in unvisited:
            if node != first_node:
                dictionary[node.label] = [None, float("inf")]
            else:
                dictionary[node.label] = [first_label, 0]
        while len(unvisited) != 0:
            minimum_value = float("inf")
            minimum_node = None
            for node in current_node.neighbours:
                new_value = [current_node.label, current_node.neighbours[node] + dictionary[current_node.label][1]]
                if new_value[1] < dictionary[node.label][1]:
                    dictionary[node.label] = new_value
                if new_value[1] < minimum_value and node in unvisited:
                    minimum_node = node
            unvisited.remove(current_node)
            current_node = minimum_node
        path = ""
        current_node = second_node.label
        while current_node != first_node.label:
            path += dictionary[current_node][0]
            current_node = dictionary[current_node][0]
        return path[::-1] + second_node.label
