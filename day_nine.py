from typing import List, NamedTuple
from collections.abc import Iterator


class Position(NamedTuple):
    i: int
    j: int
    height: int


class Cave(Iterator):
    def __init__(self):
        self._grid = []  # type: List[List[int]]
        self._curr = (0, 0)

    def add_row(self, row: List[int]):
        self._grid.append(row)

    def pos_is_low_point(self, pos: Position) -> bool:
        return (
            self._top_is_lower(pos)
            and self._bottom_is_lower(pos)
            and self._right_is_lower(pos)
            and self._left_is_lower(pos)
        )

    def _top_is_lower(self, pos: Position) -> bool:
        return pos.i == 0 or self._grid[pos.i][pos.j] < self._grid[pos.i - 1][pos.j]

    def _bottom_is_lower(self, pos: Position) -> bool:
        return (pos.i == (len(self._grid) - 1)) or self._grid[pos.i][
            pos.j
        ] < self._grid[pos.i + 1][pos.j]

    def _left_is_lower(self, pos: Position) -> bool:
        return pos.j == 0 or self._grid[pos.i][pos.j] < self._grid[pos.i][pos.j - 1]

    def _right_is_lower(self, pos: Position) -> bool:
        return (pos.j == (len(self._grid) - 1)) or self._grid[pos.i][
            pos.j
        ] < self._grid[pos.i][pos.j + 1]

    def __iter__(self):
        return self

    def __next__(self) -> Position:
        if self._curr[1] == len(self._grid):
            self._curr = (self._curr[0] + 1, 0)
        if self._curr[0] == len(self._grid):
            raise StopIteration
        pos = Position(
            i=self._curr[0],
            j=self._curr[1],
            height=self._grid[self._curr[0]][self._curr[1]],
        )
        self._curr = (self._curr[0], self._curr[1] + 1)
        return pos


def main():
    cave = Cave()
    with open("data/height_map.txt") as f:
        for line in f:
            cave.add_row([int(pos) for pos in line.strip()])

    low_points = []
    for pos in cave:
        if cave.pos_is_low_point(pos):
            low_points.append(pos.height)
    print(f"sum of risk levels = {len(low_points) + sum(low_points)}")


main()
