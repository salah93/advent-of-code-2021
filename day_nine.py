from typing import List, NamedTuple, Set
from collections.abc import Iterator
from functools import reduce


class Position(NamedTuple):
    i: int
    j: int
    height: int

    def __eq__(self, other):
        return (self.i, self.j) == (self.i, self.j)

    def __hash__(self):
        return hash((self.i, self.j))


class Marked(object):
    def __init__(self, marked: bool, height: int):
        self.marked = marked
        self.height = height

    def __repr__(self):
        return f"Marked<{self.height}>{'*' if self.marked else ''}"

    def pos_is_valid(self) -> bool:
        return not self.marked and self.height != 9


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

    def get_basins(self) -> List[List[Position]]:
        # if # is not 9 and pos is not marked, add number
        # try right, try left, try up, try down
        grid = []
        for row_i, row in enumerate(self._grid):
            grid.append([Marked(marked=False, height=pos) for pos in row])

        def inner(row_i: int, col_j: int) -> List[Position]:
            """process row until end or reach a 9"""
            if row_i >= len(grid) or col_j >= len(grid) or row_i < 0 or col_j < 0:
                return set()
            else:
                grid[row_i][col_j].marked = True
                positions = [
                    Position(i=row_i, j=col_j, height=grid[row_i][col_j].height)
                ]

                can_go_up = (row_i - 1) >= 0
                if can_go_up:
                    if grid[row_i - 1][col_j].pos_is_valid():
                        positions += inner(row_i - 1, col_j)

                can_go_down = (row_i + 1) < len(grid)
                if can_go_down:
                    if grid[row_i + 1][col_j].pos_is_valid():
                        positions += inner(row_i + 1, col_j)

                can_go_right = (col_j + 1) < len(grid)
                if can_go_right:
                    if grid[row_i][col_j + 1].pos_is_valid():
                        positions += inner(row_i, col_j + 1)

                can_go_left = (col_j - 1) >= 0
                if can_go_left:
                    if grid[row_i][col_j - 1].pos_is_valid():
                        positions += inner(row_i, col_j - 1)

                return positions

        basins = []  # type: List[List[int]]
        for row_i in range(len(grid)):
            for col_j in range(len(grid)):
                mark = grid[row_i][col_j]
                if not mark.pos_is_valid():
                    continue
                else:
                    basin = list(inner(row_i, col_j))
                    basins.append(basin)
        return basins


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
    basins = cave.get_basins()
    sum_of_basins = sorted([len(basin) for basin in basins], reverse=True)
    print(f"product of basins = {reduce(lambda a, b: a * b, sum_of_basins[:3], 1)}")


main()
