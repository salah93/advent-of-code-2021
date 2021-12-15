from argparse import ArgumentParser
from collections import Counter, defaultdict
from typing import Dict, List, Tuple


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

    template_dict = defaultdict(list)  # type: Dict[str, List[int]]
    for i in range(len(template) - 1):
        template_dict[template[i] + template[i + 1]].append(i)

    print(f"template = {template}")
    for step in range(1, args.steps + 1):
        print(f"step {step}")
        updates = {}  # type: Dict[int, str]
        for pattern, insert in pair_insertion_rules:
            for index in template_dict.get(pattern, []):
                updates[index] = insert
        new_template_dict = defaultdict(list)
        for pattern, indices in template_dict.items():
            for i in indices:
                chars_inserted_before_this_point = len(
                    [update_i for update_i in updates if update_i < i]
                )
                if i in updates:
                    new_template_dict[pattern[0] + updates[i]].append(
                        i + chars_inserted_before_this_point
                    )
                    new_template_dict[updates[i] + pattern[1]].append(
                        i + 1 + chars_inserted_before_this_point
                    )
                else:
                    new_template_dict[pattern].append(
                        i + chars_inserted_before_this_point
                    )
        template_dict = new_template_dict
    print("done")
    counter = Counter()
    for pattern, indices in template_dict.items():
        for i in indices:
            counter[pattern[0]] += 1
    counter[pattern[1]] += 1
    most_common_list = counter.most_common()
    most_common = most_common_list[0]
    least_common = most_common_list[-1]
    print(
        f"most common element - least common element = {most_common[1] - least_common[1]}"
    )


main()
