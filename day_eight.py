from typing import List, Set, Tuple


class InvalidCode(Exception):
    pass


class Entry(object):
    def __init__(self, unique_patterns_list: List[str], output_list: List[str]):
        self.unique_patterns_list = unique_patterns_list
        self.output_list = output_list

    def execute(self) -> List[str]:
        top_right = set()
        bottom_right = set()
        bottom = set()
        # [0, 6, 9]
        for pattern in self.patterns_with_six_segments():
            if len(self.pattern_one() - pattern):
                top_right = self.pattern_one() - pattern
                bottom_right = self.pattern_one() - top_right
            if len(self.segments_in_bottom_left_and_bottom() - pattern):
                bottom_left = self.segments_in_bottom_left_and_bottom() - pattern
                bottom = self.segments_in_bottom_left_and_bottom() - bottom_left

        top_left = set()
        middle = set()
        # [2, 3, 5]
        for pattern in self.patterns_with_five_segments():
            if len(self.segments_in_top_left_and_middle() - pattern):
                top_left = self.segments_in_top_left_and_middle() - pattern
                middle = self.segments_in_top_left_and_middle() - top_left
            if not bottom and len(self.segments_in_bottom_left_and_bottom() - pattern):
                bottom_left = self.segments_in_bottom_left_and_bottom() - pattern
                bottom = self.segments_in_bottom_left_and_bottom() - bottom_left

        one_pattern = self.pattern_one()
        four_pattern = self.pattern_four() | one_pattern | top_left | middle
        seven_pattern = (
            self.segments_in_top() | self.pattern_seven() | self.pattern_one()
        )
        zero_pattern = (
            one_pattern
            | seven_pattern
            | self.segments_in_bottom_left_and_bottom()
            | top_left
        )
        eight_pattern = self.pattern_eight() | zero_pattern
        two_pattern = (
            self.segments_in_top()
            | self.segments_in_bottom_left_and_bottom()
            | top_right
            | middle
        )
        three_pattern = one_pattern | seven_pattern | middle | bottom
        five_pattern = (
            self.segments_in_top() | top_left | middle | bottom_right | bottom
        )
        six_pattern = (
            self.segments_in_top()
            | top_left
            | middle
            | bottom_right
            | self.segments_in_bottom_left_and_bottom()
        )
        nine_pattern = one_pattern | seven_pattern | four_pattern | three_pattern
        code = [
            # 0
            "".join(sorted(list(zero_pattern))),
            # 1
            "".join(sorted(list(one_pattern))),
            # 2
            "".join(sorted(list(two_pattern))),
            # 3
            "".join(sorted(list(three_pattern))),
            # 4
            "".join(sorted(list(four_pattern))),
            # 5
            "".join(sorted(list(five_pattern))),
            # 6
            "".join(sorted(list(six_pattern))),
            # 7
            "".join(sorted(list(seven_pattern))),
            # 8
            "".join(sorted(list(eight_pattern))),
            # 9
            "".join(sorted(list(nine_pattern))),
        ]
        if not self._code_is_valid(code):
            raise InvalidCode
        return code

    def _code_is_valid(self, code: List[str]) -> bool:
        digits_with_required_segments = {
            2: [1],
            3: [7],
            4: [4],
            5: [2, 3, 5],
            6: [0, 6, 9],
            7: [8],
        }
        is_valid = True
        for i in range(10):
            try:
                if i not in digits_with_required_segments[len(code[i])]:
                    is_valid = False
            except KeyError:
                is_valid = False
        return is_valid

    def segments_in_top(self) -> Set[str]:
        return self.pattern_seven() - self.pattern_one()

    def segments_in_top_left_and_middle(self) -> Set[str]:
        return self.pattern_four() - self.pattern_one()

    def segments_in_bottom_left_and_bottom(self) -> Set[str]:
        return self.pattern_eight() - (self.segments_in_top() | self.pattern_four())

    def patterns_with_five_segments(self) -> List[Set[str]]:
        return self._pattern(5)

    def patterns_with_six_segments(self) -> List[Set[str]]:
        return self._pattern(6)

    def pattern_one(self) -> Set[str]:
        """
        . . .
        .   c
        . . .
        .   f
        . . .
        """
        return self._pattern(2)[0]

    def pattern_four(self) -> Set[str]:
        """
        . . .
        b   c
        d d d
        .   f
        . . .
        """
        return self._pattern(4)[0]

    def pattern_seven(self) -> Set[str]:
        """
        a a a
        .   c
        . . .
        .   f
        . . .
        """
        return self._pattern(3)[0]

    def pattern_eight(self) -> Set[str]:
        """
        a a a
        b   c
        d d d
        e   f
        g g g
        """
        return self._pattern(7)[0]

    def _pattern(self, i: int) -> List[Set[str]]:
        return [
            set(o)
            for o in set(
                ["".join(sorted(o)) for o in self.unique_patterns_list if len(o) == i]
            )
        ]


def main():
    entries = []  # type: List[Entry]
    with open("data/seven_segment.txt") as f:
        for line in f:
            entry = line.split("|")  # type: Tuple[str, str]
            unique_patterns_list = [
                "".join(sorted(seg.strip())) for seg in entry[0].split() if seg.strip()
            ]  # type List[str]
            output_list = [
                "".join(sorted(seg.strip())) for seg in entry[1].split() if seg.strip()
            ]  # type: List[str]
            entries.append(Entry(unique_patterns_list, output_list))

    total = 0
    for entry in entries:
        code = entry.execute()
        digits = []
        for number in entry.output_list:
            digits.append(str(code.index(number)))
        total += int("".join(digits))
    print(f"total is {total}")


main()
