from typing import List, Optional
from functools import reduce


class Fishy(object):
    def __init__(self, initial_days_remaining: int):
        self.days_remaining = initial_days_remaining

    def decrement(self):
        # type: () -> Optional[Fishy]
        new_days_remaining = self.days_remaining - 1
        new_fishy = None
        if new_days_remaining < 0:
            new_days_remaining = 6
            new_fishy = Fishy(8)
        self.days_remaining = new_days_remaining
        return new_fishy

    def get_children(self):
        # type: () -> List[Fishy]
        fishies = self.children
        for fishy in self.children:
            fishies.extend(fishy.get_children())
        return fishies


class Pond(object):
    def __init__(self, fishies: List[Fishy]):
        self.fishies = fishies

    def new_day(self):
        new_fishies = []
        for fishy in self.fishies:
            new_fishy = fishy.decrement()
            if new_fishy:
                new_fishies.append(new_fishy)
        self.fishies.extend(new_fishies)


def main():
    with open("data/lanternfish.txt") as f:
        lantern_fish = [
            Fishy(int(fishy_days_remaining))
            for fishy_days_remaining in next(f).split(",")
        ]  # type: List[Fishy]
    pond = Pond(lantern_fish)

    iter_days = 80

    def get_fishy_count(a: int, b: Fishy) -> int:
        return a + 1 + len(b.get_children())

    for day_i in range(1, iter_days + 1):
        pond.new_day()
        print(f"fishy count after {day_i} days is {len(pond.fishies)}")


main()
