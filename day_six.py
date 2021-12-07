from collections import defaultdict
from typing import List


class Pond(object):
    def __init__(self, fishies: List[int]):
        self.fishies = defaultdict(int)
        for days_remaining in fishies:
            self.fishies[days_remaining] += 1

    def new_day(self):
        new_fishies = defaultdict(int)
        for days_remaining in sorted(self.fishies, reverse=True):
            new_days_remaining = days_remaining - 1
            if new_days_remaining < 0:
                new_days_remaining = 6
                new_fishies[8] += self.fishies[days_remaining]
            new_fishies[new_days_remaining] += self.fishies[days_remaining]
        self.fishies = new_fishies

    def get_count(self) -> int:
        return sum([v for v in self.fishies.values()])


def main():
    with open("data/lanternfish.txt") as f:
        lantern_fish = [
            int(fishy_days_remaining) for fishy_days_remaining in next(f).split(",")
        ]  # type: List[int]
    pond = Pond(lantern_fish)

    iter_days = 256

    for day_i in range(1, iter_days + 1):
        pond.new_day()
        print(f"fishy count after {day_i} days is {pond.get_count()}")


main()
