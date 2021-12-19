from __future__ import annotations
import json

from abc import ABC
from functools import reduce
from typing import List, Optional


class SnailNumber(ABC):
    def __init__(self):
        self.parent = None


class RegularNumber(SnailNumber):
    def __init__(self, number: int):
        super().__init__()
        self.number = number

    def __repr__(self):
        return str(self.number)

    def split(self) -> Pair:
        left = RegularNumber(int(self.number / 2))
        if self.number % 2 == 0:
            right = RegularNumber(int(self.number / 2))
        else:
            right = RegularNumber(int((self.number + 1) / 2))
        new_number = Pair(left, right)
        new_number.parent = self.parent
        if self == self.parent.right:
            self.parent.right = new_number
        else:
            self.parent.left = new_number
        return new_number

    def get_left_most_number(self) -> RegularNumber:
        return self

    def get_right_most_number(self) -> RegularNumber:
        return self

    def magnitude(self) -> int:
        return self.number


class Pair(SnailNumber):
    def __init__(self, left: SnailNumber, right: SnailNumber):
        super().__init__()
        self.left = left
        self.left.parent = self
        self.right = right
        self.right.parent = self

    def __repr__(self):
        return f"[ {str(self.left)}, {str(self.right)} ]"

    def get_left_most_number(self) -> RegularNumber:
        return self.left.get_left_most_number()

    def get_right_most_number(self) -> RegularNumber:
        return self.right.get_right_most_number()

    def magnitude(self) -> int:
        return (3 * self.left.magnitude()) + (2 * self.right.magnitude())

    def is_within_n_pairs(self, n: int) -> bool:
        levels = 1
        if self.parent is not None:
            curr = self.parent
            while curr.parent is not None:
                curr = curr.parent
                levels += 1
        return levels >= n

    def explode(self) -> RegularNumber:
        new_number = RegularNumber(0)
        new_number.parent = self.parent
        if self == self.parent.right:
            left_number = self.parent.left.get_right_most_number()
            left_number.number += self.left.number
            curr = self.parent
            while curr.parent is not None and curr is curr.parent.right:
                curr = curr.parent
            if curr.parent is not None and curr.parent is not self.parent:
                right_number = curr.parent.right.get_left_most_number()
                right_number.number += self.right.number
            self.parent.right = new_number
        elif self == self.parent.left:
            right_number = self.parent.right.get_left_most_number()
            right_number.number += self.right.number
            curr = self.parent
            while curr.parent is not None and curr is curr.parent.left:
                curr = curr.parent
            if curr.parent is not None and curr.parent is not self.parent:
                left_number = curr.parent.left.get_right_most_number()
                left_number.number += self.left.number
            self.parent.left = new_number
        return new_number


def reduce_explode(snail_number: SnailNumber) -> Optional[SnailNumber]:
    if isinstance(snail_number, RegularNumber):
        return None
    elif snail_number.is_within_n_pairs(4):
        new_snail_number = snail_number.explode()
        return new_snail_number
    else:
        is_in_left = reduce_explode(snail_number.left)
        if not is_in_left:
            is_in_right = reduce_explode(snail_number.right)
        return is_in_left or is_in_right


def reduce_split(snail_number: SnailNumber) -> Optional[SnailNumber]:
    if isinstance(snail_number, RegularNumber):
        if snail_number.number >= 10:
            new_snail_number = snail_number.split()
            return new_snail_number
        else:
            return None
    else:
        is_in_left = reduce_split(snail_number.left)
        if not is_in_left:
            is_in_right = reduce_split(snail_number.right)
        return is_in_left or is_in_right


def reduce_snail_number(root_snail_number: SnailNumber) -> SnailNumber:
    if not reduce_explode(root_snail_number):
        if not reduce_split(root_snail_number):
            return root_snail_number
        else:
            return reduce_snail_number(root_snail_number)
    else:
        return reduce_snail_number(root_snail_number)


def add_two_snail_numbers(left: SnailNumber, right: SnailNumber) -> SnailNumber:
    root = Pair(left, right)
    return root


def parse_to_snail_number(row) -> SnailNumber:
    if isinstance(row[0], int):
        left = RegularNumber(row[0])
    else:
        left = parse_to_snail_number(row[0])
    if isinstance(row[1], int):
        right = RegularNumber(row[1])
    else:
        right = parse_to_snail_number(row[1])
    return Pair(left, right)


def main():
    rows = []
    with open("data/snail_hw.txt") as f:
        for line in f:
            rows.append(json.loads(line.strip()))
    equation = []  # type: List[SnailNumber]
    for row in rows:
        equation.append(parse_to_snail_number(row))
    root = reduce(
        lambda root, eq: reduce_snail_number(add_two_snail_numbers(root, eq)), equation
    )

    print(f"number = {root}")
    print(f"magnitude = {root.magnitude()}")
    largest_magnitude = 0
    for i in range(len(equation)):
        for j in range(len(equation)):
            if i == j:
                continue
            first = parse_to_snail_number(rows[i])
            second = parse_to_snail_number(rows[j])
            root = reduce_snail_number(add_two_snail_numbers(first, second))
            root_magnitude = root.magnitude()
            if root_magnitude > largest_magnitude:
                largest_magnitude = root_magnitude
    print(f"largest magnitude = {largest_magnitude}")


main()
