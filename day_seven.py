from typing import List

try:
    from scipy.optimize import minimize

    scipy_installed = True
except ImportError:
    scipy_installed = False


def sum_of_costs_part_1(desired_position: List[int], crab_positions: List[int]) -> int:
    return sum([abs(pos - desired_position[0]) for pos in crab_positions])


def sum_of_costs_part_2(desired_position: List[int], crab_positions: List[int]) -> int:
    costs = []
    for pos in crab_positions:
        difference = abs(pos - desired_position[0])
        costs.append((difference * (difference + 1)) / 2)
    return sum(costs)


def main():
    with open("data/crabs.txt") as f:
        crab_positions = [int(c) for c in next(f).split(",")]  # type: List[int]

    sum_fn = sum_of_costs_part_2

    solution_found = False
    if scipy_installed:
        solution = minimize(
            sum_fn,
            x0=crab_positions[0],
            method="Nelder-Mead",
            args=(crab_positions,),
        )
        solution_found = solution.success
    if solution_found:
        print(
            f"minimum cost (minimize funtion) = {sum_fn([round(solution.x[0])], crab_positions)}, at position {round(solution.x[0])}, success = {solution.success}"
        )
    else:
        min_position = (
            0,
            sum_fn([0], crab_positions),
        )
        for i in range(max(crab_positions)):
            cost = sum_fn([i], crab_positions)
            if cost < min_position[1]:
                min_position = (i, cost)
        print(f"minimum cost = {min_position[1]}, at position {min_position[0]}")


main()
