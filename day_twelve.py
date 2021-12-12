from collections import defaultdict
from typing import Dict, List, NamedTuple, Set, Tuple


class CaveNotFound(Exception):
    pass


class Cave(NamedTuple):
    name: str
    is_small: bool


START = Cave("start", is_small=True)
END = Cave("end", is_small=True)


class Graph(object):
    def __init__(self):
        self._caves = set()  # type: Set[Cave]
        self._edges = defaultdict(set)  # type: Dict[Cave, Set[Cave]]

    def add_cave(self, cave: Cave):
        self._caves.add(cave)

    def add_caves_from(self, caves: List[str]):
        for cave in caves:
            self.add_cave(cave)

    def add_edge(self, cave_a: Cave, cave_b: Cave):
        if cave_a not in self._caves or cave_b not in self._caves:
            raise CaveNotFound
        self._edges[cave_a].add(cave_b)
        self._edges[cave_b].add(cave_a)

    def get_paths(self) -> List[List[Cave]]:
        return self.explore_cave(
            cave=START,
            path=[],
            all_paths=[],
        )

    def _part_two_clause(self, cave: Cave, path: List[Cave]) -> bool:
        can_not_pass = False
        if cave == START and len(path) > 0:
            can_not_pass = True
        elif cave.is_small:
            cave_counts = {c: path.count(c) for c in path if c.is_small}
            already_visited_small_cave_twice = any(
                [count == 2 for count in cave_counts.values()]
            )
            can_not_pass = already_visited_small_cave_twice and cave in path
        return can_not_pass

    def _part_one_clause(self, cave: Cave, path: List[Cave]) -> bool:
        return cave.is_small and path.count(cave) >= 1

    def explore_cave(
        self,
        cave: Cave,
        path: List[Cave],
        all_paths: List[List[Cave]],
    ) -> List[List[Cave]]:
        path = path + [cave]
        if cave == END:
            return all_paths + [path]
        else:
            for next_cave in self._edges[cave]:
                if self._part_two_clause(next_cave, path):
                    continue
                all_paths = self.explore_cave(next_cave, path, all_paths)
            return all_paths


def main():
    g = Graph()
    with open("data/network_test.txt") as f:
        for line in f:
            caves = [
                Cave(name=name, is_small=name.islower())
                for name in sorted(line.strip().split("-"))
            ]  # type: List[Cave]
            g.add_caves_from(caves)
            g.add_edge(caves[0], caves[1])
    paths = sorted([",".join([c.name for c in path]) for path in g.get_paths()])
    print(f"total paths = {len(paths)}")


main()
