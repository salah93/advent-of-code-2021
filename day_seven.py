from typing import List


def sum_of_costs(desired_position: int, crab_positions: List[int]):
    return sum([abs(pos - desired_position) for pos in crab_positions])


def main():
    with open("data/crabs.txt") as f:
        crab_positions = [int(c) for c in next(f).split(",")]  # type: List[int]

    min_position = (crab_positions[0], sum_of_costs(crab_positions[0], crab_positions))
    for crab_position in crab_positions:
        cost = sum_of_costs(crab_position, crab_positions)
        if cost < min_position[1]:
            min_position = (crab_position, cost)
    print(f"minimum cost = {min_position[1]}, at position {min_position[0]}")


main()
