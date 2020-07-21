class Graph(object):
    def __init__(self):
        self.graph = {}

    def check_existence(self, node):
        return node in self.graph

    def check_adjacency(self, first_node, second_node):
        if self.check_existence(first_node) and self.check_existence(second_node):
            return first_node in self.graph[second_node]

    def add_node(self, node):
        self.graph[node] = []

    def remove_node(self, node):
        if self.check_existence(node):
            [self.remove_edge(node, other_node) for other_node in self.graph if other_node != node and self.check_adjacency(node, other_node)]
        del self.graph[node]

    def add_edge(self, first_node, second_node):
        if self.check_existence(first_node) and self.check_existence(second_node) and not self.check_adjacency(first_node, second_node):
            self.graph[first_node].append(second_node)
            self.graph[second_node].append(first_node)

    def remove_edge(self, first_node, second_node):
        if self.check_existence(first_node) and self.check_existence(second_node) and self.check_adjacency(first_node, second_node):
            self.graph[first_node].remove(second_node)
            self.graph[second_node].remove(first_node)

    def return_neighbours(self, node):
        return self.graph[node]

    def return_graph(self):
        return self.graph

    def return_nodes(self):
        return list(self.graph.keys())
