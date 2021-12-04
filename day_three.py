from collections import Counter
from typing import List, Optional, Tuple


BitPositionCount = Counter()


def get_oxygen_data(
    bit: Counter, oxygen_generator_data: List[str], index: int
) -> List[str]:
    most_common = bit.most_common()[0]  # type: Tuple[str, int]
    least_common = bit.most_common()[-1]  # type: Tuple[str, int]
    same_count = most_common[1] == least_common[1]
    oxygen_bit = "1" if same_count else most_common[0]  # type: str
    return [d for d in oxygen_generator_data if d[index] == oxygen_bit]


def get_co2_data(bit: Counter, co2_scrubber_data: List[str], index: int) -> List[str]:
    most_common = bit.most_common()[0]  # type: Tuple[str, int]
    least_common = bit.most_common()[-1]  # type: Tuple[str, int]
    same_count = most_common[1] == least_common[1]
    co2_bit = "0" if same_count else least_common[0]  # type: str
    return [d for d in co2_scrubber_data if d[index] == co2_bit]


def populate_counter(data: List[str]) -> List[Counter]:
    counter = [
        Counter(),
        Counter(),
        Counter(),
        Counter(),
        Counter(),
        Counter(),
        Counter(),
        Counter(),
        Counter(),
        Counter(),
        Counter(),
        Counter(),
    ]  # type: List[Counter]
    for line in data:
        for i, bit in enumerate(line):
            counter[i][bit] += 1
    return counter


def get_counter_for_index(data: List[str], index: int) -> Counter:
    counter = Counter()
    for line in data:
        counter[line[index]] += 1
    return counter


def main():
    all_data = []  # type: List[str]
    with open("diagnostics.txt") as f:
        for line in f:
            all_data.append(line.strip())

    # part 1
    # counter = populate_counter(all_data)
    # gamma = ''.join([bit.most_common()[0][0] for bit in counter])
    # epsilon = ''.join([bit.most_common()[-1][0] for bit in counter])
    # print(f'gamma = {gamma}, epsilon = {epsilon}, power consumption = {int(gamma, 2) * int(epsilon, 2)}')

    # part 2

    oxygen_generator_data = co2_scrubber_data = all_data
    oxygen_filtered = co2_filtered = False
    for i in range(len(all_data[0])):
        if not oxygen_filtered:
            oxygen_generator_data = get_oxygen_data(
                get_counter_for_index(oxygen_generator_data, i),
                oxygen_generator_data,
                i,
            )

        if not co2_filtered:
            co2_scrubber_data = get_co2_data(
                get_counter_for_index(co2_scrubber_data, i), co2_scrubber_data, i
            )

        oxygen_filtered = len(oxygen_generator_data) == 1
        co2_filtered = len(co2_scrubber_data) == 1

        if oxygen_filtered and co2_filtered:
            break

    if not (oxygen_filtered and co2_filtered):
        raise RuntimeError

    print(
        f"""
            oxygen generator rating = {oxygen_generator_data}
            co2 scrubber rating = {co2_scrubber_data}
            life support rating = {int(oxygen_generator_data[0], 2) * int(co2_scrubber_data[0], 2)}"""
    )


main()
