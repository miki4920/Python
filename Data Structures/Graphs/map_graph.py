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


class Map(object):
    def __init__(self, width, length, default_cost=1):
        self.width = width
        self.length = length
        self.walls = []
        self.cost_dictionary = {}
        self.default_cost = default_cost

    def return_map(self, path=()):
        readable_map = [[" ."] * self.width for _ in range(self.length)]
        for coord in self.walls:
            x, y = coord
            readable_map[y][x] = " #"
        for coord in path:
            x, y = coord
            readable_map[y][x] = " x"
        for row_index in range(0, self.length):
            readable_map[row_index] = "".join(readable_map[row_index])
        readable_map = " \n".join(readable_map)
        return readable_map

    def passable(self, coords):
        return coords not in self.walls

    def in_bounds(self, coords):
        x, y = coords
        return 0 <= x < self.width and 0 <= y < self.length

    def cost(self, coords):
        if coords in self.cost_dictionary:
            return self.cost_dictionary[coords]
        return self.default_cost

    def get_neighbours(self, coords):
        x, y = coords
        coord_pairs = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
        coords = [(coord_pair[0] + x, coord_pair[1] + y) for coord_pair in coord_pairs]
        coords = filter(self.in_bounds, coords)
        coords = filter(self.passable, coords)
        return coords

    @staticmethod
    def shortest_path_heuristic(point, destination):
        dx = abs(point[0] - destination[0])
        dy = abs(point[1] - destination[1])
        return max(dx, dy)

    @staticmethod
    def trace_back(came_from, origin, destination):
        path = []
        current = destination
        while current != origin:
            path.append(current)
            current = came_from[current]
        path.append(origin)
        return path[::-1]

    def path_astar(self, origin, destination):
        open_queue = PriorityQueue(((self.cost(origin) + self.shortest_path_heuristic(origin, destination)), origin))
        cost_dictionary = {}
        came_from = {}
        closed = []
        while open_queue.queue[0][1] != destination:
            current = open_queue.pop_element(0)[1]
            closed.append(current)
            for neighbour in self.get_neighbours(current):
                current_cost = cost_dictionary[current] if current in cost_dictionary else self.cost(current)
                neighbour_cost = cost_dictionary[neighbour] if neighbour in cost_dictionary else self.cost(neighbour)
                cost = current_cost + neighbour_cost
                if open_queue.check_element(neighbour) != -1 and cost < neighbour_cost:
                    open_queue.delete_element(neighbour)
                if neighbour in closed and cost < neighbour_cost:
                    closed.remove(neighbour)
                if open_queue.check_element(neighbour) == -1 and neighbour not in closed:
                    cost_dictionary[neighbour] = cost
                    open_queue.add_element(
                        (cost_dictionary[neighbour] + self.shortest_path_heuristic(neighbour, destination),
                         neighbour))
                    came_from[neighbour] = current
        return self.trace_back(came_from, origin, destination)

