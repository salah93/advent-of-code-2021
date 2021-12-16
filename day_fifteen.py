from collections import defaultdict
from typing import Dict, List, NamedTuple, Set, Tuple


class Node(NamedTuple):
    x: int
    y: int


class Edge(NamedTuple):
    weight: int
    node_a: Node
    node_b: Node


class MissingNode(Exception):
    pass


class PathNotFound(Exception):
    pass


class Network(object):
    def __init__(self):
        self._nodes = set()  # type: Set[Node]
        self._edges = defaultdict(list)  # type: Dict[Node, List[Edge]]

    def add_node(self, node: Node):
        self._nodes.add(node)

    def add_edge(self, node_a: Node, node_b: Node, weight: int):
        if node_a not in self._nodes or node_b not in self._nodes:
            raise MissingNode
        self._edges[node_a].append(Edge(weight, node_a, node_b))

    def display(self) -> str:
        display = ""
        for node in sorted(self._edges):
            for edge in self._edges[node]:
                display += f"{node} -> {edge}"
                display += "\n"
        return display

    def get_shortest_path(self, start: Node, end: Node) -> Tuple[int, List[Edge]]:
        distances = {}  # type: Dict[Node, Tuple[float, List[Edge]]]
        for node in self._nodes:
            distances[node] = (float("inf"), [])
        distances[start] = (0, [])
        unvisited_nodes = self._nodes
        while unvisited_nodes:
            node_with_min_distance = self._get_node_with_min_distance(
                distances, unvisited_nodes
            )
            if node_with_min_distance == end:
                return distances[node_with_min_distance]
            unvisited_nodes = unvisited_nodes - {node_with_min_distance}
            self._explore_node(node_with_min_distance, distances)
        raise PathNotFound

    def _get_node_with_min_distance(
        self,
        distances: Dict[Node, Tuple[float, List[Edge]]],
        unvisited_nodes: Set[Node],
    ) -> Node:
        min_node = (float("inf"), None)
        for node, (distance, path) in distances.items():
            if node in unvisited_nodes:
                if distance < min_node[0]:
                    min_node = (distance, node)
        return min_node[1]

    def get_cost_of_path(self, path: List[Edge]) -> int:
        return sum([e.weight for e in path])

    def _explore_node(self, node: Node, distances: Dict[Node, float]):
        for edge in self._edges[node]:
            if (distances[node][0] + edge.weight) < distances[edge.node_b][0]:
                distances[edge.node_b] = (
                    (distances[node][0] + edge.weight),
                    distances[node][1] + [edge],
                )


class Grid(object):
    def __init__(self):
        self._grid = []  # type: List[List[int]]

    def add_row(self, row: List[int]):
        self._grid.append(row)

    def get_dimensions(self) -> Tuple[int, int]:
        length = len(self._grid)
        width = len(self._grid[0]) if length else 0
        return (length, width)

    def get_network(self) -> Network:
        network = Network()
        for i, row in enumerate(self._grid):
            for j, weight in enumerate(row):
                network.add_node(Node(x=i, y=j))
        for i, row in enumerate(self._grid):
            for j, weight in enumerate(row):
                this_node = Node(x=i, y=j)

                if j - 1 >= 0:
                    left_node = Node(x=i, y=j - 1)
                    network.add_edge(left_node, this_node, weight)

                if j + 1 < len(row):
                    right_node = Node(x=i, y=j + 1)
                    network.add_edge(right_node, this_node, weight)

                if i - 1 >= 0:
                    top_node = Node(x=i - 1, y=j)
                    network.add_edge(top_node, this_node, weight)

                if i + 1 < len(self._grid):
                    bottom_node = Node(x=i + 1, y=j)
                    network.add_edge(bottom_node, this_node, weight)
        return network


def main():
    grid = Grid()
    with open("data/path_test.txt") as f:
        for i, line in enumerate(f):
            grid.add_row([int(weight) for weight in line.strip()])

    # part 1
    network = grid.get_network()
    START = Node(0, 0)
    length, width = grid.get_dimensions()
    END = Node(length - 1, width - 1)
    distance, shortest_path = network.get_shortest_path(START, END)
    print(distance)

    # part 2
    # expand grid to be 5 times larger
    # length = len(grid)
    # width = len(grid[0])
    # for m_i in range(1, 5):
    #    for m_j in range(1, 5):
    #        for i in range(len(grid)):
    #            row = grid[i]
    #            for j in range(len(row)):
    #                grid[i].append(max((grid[i][j] + m_j) % 10, 1))
    # length_size = len(grid) * 5
    # width_size = len(grid[0]) * 5
    # for i in range(length_size):
    #    try:
    #        grid[i] = grid[i]
    #    except IndexError:
    #        grid[i] = []
    #    for j in range(width_size):
    #        try:
    #            grid[i][j] = grid[i][j]
    #        except IndexError:
    #            grid[i].append()
    #    try:
    #        row_size = width_size - len(grid[i])
    #        grid[i].extend([0] * row_size)
    #    except IndexError:
    #        grid.append([0] * width_size)

    # for i in range(5):
    #    for j in range(5):
    #        if i == j == 0:
    #            continue


main()
