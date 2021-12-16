from collections import defaultdict
from typing import Dict, List, NamedTuple, Set


class Node(NamedTuple):
    x: int
    y: int


class Edge(NamedTuple):
    weight: int
    node_a: Node
    node_b: Node


class MissingNode(Exception):
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

    def get_shortest_path(self, start: Node, end: Node) -> List[Edge]:
        distances = {}  # type: Dict[Node, List[Edge]]
        for node in self._nodes:
            distances[node] = [Edge(float("inf"), None, None)]
        distances[start] = []
        unvisited_nodes = self._nodes
        while unvisited_nodes:
            node_with_min_distance = self._get_node_with_min_distance(
                distances, unvisited_nodes
            )
            if node_with_min_distance == end:
                return distances[node_with_min_distance]
            unvisited_nodes = unvisited_nodes - {node_with_min_distance}
            self._explore_node(node_with_min_distance, distances)

    def _get_node_with_min_distance(
        self, distances: Dict[Node, List[Edge]], unvisited_nodes: Set[Node]
    ) -> Node:
        node_with_min_distance = (None, float("inf"))
        for node in distances:
            if node in unvisited_nodes:
                distance = self.get_cost_of_path(distances[node])
                if distance < node_with_min_distance[1]:
                    node_with_min_distance = (node, distance)
        return node_with_min_distance[0]

    def get_cost_of_path(self, path: List[Edge]) -> int:
        return sum([e.weight for e in path])

    def _explore_node(self, node: Node, distances: Dict[Node, float]):
        total_distance_for_node = self.get_cost_of_path(distances[node])
        for edge in self._edges[node]:
            if (total_distance_for_node + edge.weight) < self.get_cost_of_path(
                distances[edge.node_b]
            ):
                distances[edge.node_b] = distances[node] + [edge]


def main():
    network = Network()
    with open("data/path_test.txt") as f:
        grid = []  # type: List[List[int]]
        for i, line in enumerate(f):
            grid.append([])
            for j, weight in enumerate(line.strip()):
                grid[-1].append(int(weight))
                network.add_node(Node(x=i, y=j))

        START = Node(0, 0)
        END = Node(len(grid) - 1, len(grid[-1]) - 1)

        for i, row in enumerate(grid):
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

                if i + 1 < len(grid):
                    bottom_node = Node(x=i + 1, y=j)
                    network.add_edge(bottom_node, this_node, weight)
        shortest_path = network.get_shortest_path(START, END)
        print(network.get_cost_of_path(shortest_path))


main()
