from __future__ import annotations

from collections import defaultdict
from typing import Dict, List, NamedTuple, Optional, Set, Tuple

import copy
import heapq


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
        distances[start] = (0, [])
        heap = []
        heapq.heappush(heap, (0, start))
        visited_nodes = set()
        while heap:
            _, node_with_min_distance = heapq.heappop(heap)
            if node_with_min_distance == end:
                return distances[node_with_min_distance]
            visited_nodes.add(node_with_min_distance)
            self._explore_node(node_with_min_distance, distances, visited_nodes, heap)
        raise PathNotFound

    def _explore_node(
        self,
        node: Node,
        distances: Dict[Node, float],
        visited_nodes: Set[Node],
        heap: List[Tuple[int, Node]],
    ):
        for edge in self._edges[node]:
            if edge.node_b not in visited_nodes:
                if (distances[node][0] + edge.weight) < distances.get(
                    edge.node_b, (float("inf"), None)
                )[0]:
                    distances[edge.node_b] = (
                        (distances[node][0] + edge.weight),
                        distances[node][1] + [edge],
                    )
                    heapq.heappush(
                        heap, ((distances[node][0] + edge.weight), edge.node_b)
                    )


class Grid(object):
    def __init__(self, grid: Optional[List[List[int]]] = None):
        self._grid = grid or []  # type: List[List[int]]

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

    def display(self) -> str:
        display = ""
        for row in self._grid:
            for weight in row:
                display += f" {weight} "
            display += "\n"
        return display

    def get_expanded_grid(self, multiple: int) -> Grid:
        """expand grid to be `multiple` times larger"""
        length, width = self.get_dimensions()

        def get_weight(w):
            return (w % 9) or 9

        new_grid = copy.deepcopy(self._grid)
        for row_i in range(length):
            for add in range(1, multiple):
                row = [get_weight(weight + add) for weight in self._grid[row_i]]
                new_grid[row_i].extend(row)

        for add in range(1, multiple):
            for row_i in range(length):
                new_grid.append(
                    [get_weight(weight + add) for weight in new_grid[row_i]]
                )
        return Grid(new_grid)


def main():
    grid = Grid()
    with open("data/path_test.txt") as f:
        for i, line in enumerate(f):
            grid.add_row([int(weight) for weight in line.strip()])

    # part 1
    # network = grid.get_network()
    # START = Node(0, 0)
    # length, width = grid.get_dimensions()
    # END = Node(length - 1, width - 1)
    # distance, shortest_path = network.get_shortest_path(START, END)
    # print(distance)

    # part 2
    new_grid = grid.get_expanded_grid(5)
    print(new_grid.display())
    network = new_grid.get_network()
    START = Node(0, 0)
    length, width = new_grid.get_dimensions()
    END = Node(length - 1, width - 1)
    number_of_edges = 0
    for n, edges in network._edges.items():
        number_of_edges += len(edges)
    print(f"number of edges = {number_of_edges}")
    print(f"number of nodes = {len(network._nodes)}")
    distance, shortest_path = network.get_shortest_path(START, END)
    print(distance)


main()
