from collections import Counter
from collections.abc import Iterator
from typing import List, NamedTuple


class Position(NamedTuple):
    x: int
    y: int

    def __eq__(self, other) -> bool:
        # type: (Position) -> bool
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __add__(self, other):
        # type: (Position) -> Position
        return Position(
            x=(self.x + other.x),
            y=(self.y + other.y),
        )


class Line(NamedTuple):
    start: Position
    end: Position

    @property
    def is_horizontal(self) -> bool:
        return self.start.x == self.end.x

    @property
    def is_vertical(self) -> bool:
        return self.start.y == self.end.y

    def __iter__(self):
        return LineIterator(self)


class LineIterator(Iterator):
    def __init__(self, line: Line):
        self.line = line
        self.curr_pos = self.line.start

        if line.end.x == line.start.x:
            increment_x = 0
        elif line.end.x < line.start.x:
            increment_x = -1
        else:
            increment_x = 1

        if line.end.y == line.start.y:
            increment_y = 0
        elif line.end.y < line.start.y:
            increment_y = -1
        else:
            increment_y = 1
        self.reached_end = False
        self.increment = Position(x=increment_x, y=increment_y)

    def __iter__(self):
        return self

    def __next__(self) -> Position:
        if self.reached_end:
            raise StopIteration

        self.reached_end = self.curr_pos == self.line.end

        next_pos = self.curr_pos
        self.curr_pos += self.increment
        return next_pos


class Grid(object):
    def __init__(self):
        self.grid = []  # type: List[List[int]]

    @property
    def size(self):
        return len(self.grid)

    def add_line(self, line: Line):
        max_size = max([line.start.x, line.start.y, line.end.x, line.end.y]) + 1
        if len(self.grid) < max_size:
            self._expand_grid(max_size)
        for pos in line:
            self.mark_position(pos)

    def mark_position(self, pos: Position):
        self.grid[pos.x][pos.y] += 1

    def _expand_grid(self, max_size: int):
        for i in range(max_size):
            try:
                self.grid[i].extend([0] * (max_size - len(self.grid[i])))
            except IndexError:
                self.grid.append([0] * (max_size))

    def display(self) -> str:
        grid = ""
        for row in self.grid:
            for item in row:
                if item == 0:
                    grid += "."
                else:
                    grid += str(item)
                grid += " "
            grid += "\n"
        return grid

    def get_counts(self) -> Counter:
        counts = Counter()
        for row in self.grid:
            for item in row:
                counts[item] += 1
        return counts


def main():
    grid = Grid()
    with open("data/vents.txt") as f:
        for line in f:
            start, end = line.split("->")
            start_pos = Position(*[int(pos) for pos in start.split(",")])
            end_pos = Position(*[int(pos) for pos in end.split(",")])
            grid.add_line(Line(start=start_pos, end=end_pos))
    print(
        f"overlaps = {sum([count for overlaps, count in grid.get_counts().items() if overlaps >= 2])}"
    )


main()
