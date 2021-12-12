from typing import List, Set, Tuple


class Cavern(object):
    def __init__(self):
        self._cavern = []  # type: List[List[int]]

    def add_row(self, row: List[int]):
        self._cavern.append(row)

    def get_total_octopuses(self) -> int:
        total = 0
        for row in self._cavern:
            total += len(row)
        return total

    def step(self) -> Set[Tuple[int, int]]:
        self._step_one()
        return self._step_two()

    def _step_one(self):
        for i in range(len(self._cavern)):
            for j in range(len(self._cavern[i])):
                self._cavern[i][j] += 1

    def _step_two(self):
        coords_that_flashed = set()  # type: Set[Tuple[int, int]]
        for i in range(len(self._cavern)):
            for j in range(len(self._cavern[i])):
                coords_that_flashed = self._process(i, j, coords_that_flashed)
        return coords_that_flashed

    def _process(
        self, i: int, j: int, coords_that_flashed: Set[Tuple[int, int]]
    ) -> Set[Tuple[int, int]]:
        if self._cavern[i][j] > 9:
            return self._flash(i, j, coords_that_flashed | set([(i, j)]))
        return coords_that_flashed

    def _flash(self, i: int, j: int, coords_that_flashed) -> Set[Tuple[int, int]]:
        # top left
        self._cavern[i][j] = 0
        coords = [
            (i - 1, j - 1),  # top left
            (i - 1, j),  # top
            (i - 1, j + 1),  # top right
            (i + 1, j - 1),  # bottom left
            (i + 1, j),  # bottom
            (i + 1, j + 1),  # bottom right
            (i, j - 1),  # left
            (i, j + 1),  # right
        ]
        for coord in coords:
            new_i, new_j = coord
            if (
                new_i < 0
                or new_i >= len(self._cavern)
                or new_j < 0
                or new_j >= len(self._cavern[new_i])
            ):
                continue
            if (new_i, new_j) in coords_that_flashed:
                continue
            self._cavern[new_i][new_j] += 1
            coords_that_flashed = self._process(new_i, new_j, coords_that_flashed)
        return coords_that_flashed


def main():
    cavern = Cavern()
    with open("data/octopuses.txt") as f:
        for line in f:
            cavern.add_row([int(o) for o in line.strip()])

    # part 1
    # flashes = 0
    # steps = 100
    # for i in range(1, steps + 1):
    #    current_flashes = len(cavern.step())
    #    print(f"total flashes after step {i} steps is {current_flashes}")
    #    # print(cavern.display())
    #    flashes += current_flashes
    # print(f"total flashes after {steps} steps is {flashes}")

    flashes = 0
    step = 0
    while flashes != cavern.get_total_octopuses():
        flashes = len(cavern.step())
        step += 1

    print(f"synchronized flashes happen at step {step}")


main()
