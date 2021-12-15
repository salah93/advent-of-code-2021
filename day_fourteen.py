from argparse import ArgumentParser
from collections import Counter, defaultdict
from typing import Dict, List, Tuple


def get_args():
    parser = ArgumentParser()
    parser.add_argument("-S", "--steps", type=int, default=1)
    parser.add_argument("-F", "--file", required=True)
    return parser.parse_args()


def get_template_dict_from_template(template: str) -> Dict[str, List[int]]:
    template_dict = defaultdict(list)  # type: Dict[str, List[int]]
    for i in range(len(template) - 1):
        template_dict[template[i] + template[i + 1]].append(i)
    return template_dict


def main():
    args = get_args()
    pair_insertion_rules = []  # type: List[Tuple[str, str]]
    with open(args.file) as f:
        template = next(f).strip()
        for line in f:
            if line.strip():
                pattern, insert = line.strip().split("->")
                pair_insertion_rules.append((pattern.strip(), insert.strip()))

    template_dict = get_template_dict_from_template(template)
    print(f"template = {template}")
    for step in range(1, args.steps + 1):
        updates = {}  # type: Dict[int, str]
        for pattern, insert in pair_insertion_rules:
            for index in template_dict.get(pattern, []):
                updates[index] = insert
        new_template = ""
        for i, char in enumerate(template):
            new_template += char
            if i in updates:
                new_template += updates[i]
        template = new_template
        template_dict = get_template_dict_from_template(template)
    counter = Counter(template)
    most_common_list = counter.most_common()
    most_common = most_common_list[0]
    least_common = most_common_list[-1]
    print(
        f"most common element - least common element = {most_common[1] - least_common[1]}"
    )


main()
