from typing import List, NamedTuple


class Position(NamedTuple):
    x: int
    y: int


class Fold(NamedTuple):
    increment: int
    horizontal: bool


class Grid(object):
    def __init__(self):
        self._grid = []  # type: List[List[bool]]

    def mark_position(self, position: Position):
        self._expand_grid(position)
        self._grid[position.y][position.x] = True

    def _expand_grid(self, position: Position):
        try:
            max_x = max([len(self._grid[0]), position.x + 1])
        except IndexError:
            max_x = position.x + 1

        max_y = max([len(self._grid), position.y + 1])
        if max_y == len(self._grid) and max_x == len(self._grid[0]):
            return
        for i in range(max_y):
            try:
                self._grid[i].extend([False] * (max_x - len(self._grid[i])))
            except IndexError:
                self._grid.append([False] * (max_x))

    def fold(self, fold: Fold):
        if fold.horizontal:
            self._fold_horizontal(fold.increment)
        else:
            self._fold_vertical(fold.increment)

    def _fold_horizontal(self, y_fold: int):
        for y in range(y_fold + 1, len(self._grid)):
            for x in range(len(self._grid[y])):
                marked = self._grid[y][x]
                if marked:
                    self.mark_position(Position(x, y=(2 * y_fold) - y))
        self._grid = self._grid[:y_fold]

    def _fold_vertical(self, x_fold: int):
        for y in range(len(self._grid)):
            for x in range(x_fold + 1, len(self._grid[y])):
                marked = self._grid[y][x]
                if marked:
                    self.mark_position(Position(x=(2 * x_fold) - x, y=y))
            self._grid[y] = self._grid[y][:x_fold]

    def display(self) -> str:
        display = ""
        for row in self._grid:
            for marked in row:
                display += "#" if marked else "."
                display += " "
            display += "\n"
        return display

    def number_of_dots_visible(self) -> int:
        count = 0
        for row in self._grid:
            count += sum(row)
        return count


def main():
    folds = []  # type: List[Fold]
    grid = Grid()
    with open("data/dots.txt") as f:
        for line in f:
            if line.startswith("fold"):
                xy, increment = line.strip().split()[-1].split("=")
                folds.append(Fold(increment=int(increment), horizontal=(xy == "y")))
            elif line.strip():
                pos = Position(*[int(i) for i in line.strip().split(",")])
                grid.mark_position(pos)
    grid.fold(folds[0])
    print(f"count = {grid.number_of_dots_visible()}")
    for fold in folds[1:]:
        grid.fold(fold)
    print(grid.display())


main()
