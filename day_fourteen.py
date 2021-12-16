from argparse import ArgumentParser
from collections import Counter, defaultdict
from typing import Dict, List, Tuple

import copy


def get_args():
    parser = ArgumentParser()
    parser.add_argument("-S", "--steps", type=int, default=1)
    parser.add_argument("-F", "--file", required=True)
    return parser.parse_args()


def main():
    args = get_args()
    pair_insertion_rules = []  # type: List[Tuple[str, str]]
    with open(args.file) as f:
        template = next(f).strip()
        for line in f:
            if line.strip():
                pattern, insert = line.strip().split("->")
                pair_insertion_rules.append((pattern.strip(), insert.strip()))

    template_dict = defaultdict(int)  # type: Dict[str, List[int]]
    for i in range(len(template) - 1):
        template_dict[template[i] + template[i + 1]] += 1
    new_template_dict = copy.deepcopy(template_dict)

    print(f"template = {template}")
    for step in range(1, args.steps + 1):
        print(f"step {step}")
        for pattern, insert in pair_insertion_rules:
            if pattern in template_dict:
                new_template_dict[pattern[0] + insert] += template_dict[pattern]
                new_template_dict[insert + pattern[1]] += template_dict[pattern]
                new_template_dict[pattern] -= template_dict[pattern]
                if new_template_dict[pattern] <= 0:
                    new_template_dict.pop(pattern)
        template_dict = copy.deepcopy(new_template_dict)

    print("done")
    counter = Counter()
    for pattern, count in template_dict.items():
        counter[pattern[0]] += count
    counter[template[-1]] += 1

    most_common_list = counter.most_common()
    most_common = most_common_list[0]
    least_common = most_common_list[-1]
    print(
        f"most common element - least common element = {most_common[1] - least_common[1]}"
    )


main()
