from typing import List


def sum_of_costs_part_1(desired_position: int, crab_positions: List[int]) -> int:
    return sum([abs(pos - desired_position) for pos in crab_positions])


def sum_of_costs_part_2(desired_position: int, crab_positions: List[int]) -> int:
    costs = []
    for pos in crab_positions:
        difference = abs(pos - desired_position)
        costs.append((difference * (difference + 1)) / 2)
    return sum(costs)


def main():
    with open("data/crabs.txt") as f:
        crab_positions = [int(c) for c in next(f).split(",")]  # type: List[int]

    sum_fn = sum_of_costs_part_2
    min_position = (
        0,
        sum_fn(0, crab_positions),
    )
    for i in range(max(crab_positions)):
        cost = sum_fn(i, crab_positions)
        if cost < min_position[1]:
            min_position = (i, cost)
    print(f"minimum cost = {min_position[1]}, at position {min_position[0]}")


main()
