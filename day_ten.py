from functools import reduce
from typing import Dict, List


class IllegalCharacter(Exception):
    pass


def is_closing_character(character: str) -> bool:
    return character in ["}", "]", ">", ")"]


def is_opening_character(character: str) -> bool:
    return character in ["{", "[", "<", "("]


def get_matching_character(opening_character: str) -> str:
    ending_character = ""
    if opening_character == "{":
        ending_character = "}"
    elif opening_character == "<":
        ending_character = ">"
    elif opening_character == "(":
        ending_character = ")"
    elif opening_character == "[":
        ending_character = "]"
    else:
        raise IllegalCharacter
    return ending_character


def characters_match(opening_character: str, ending_character: str) -> bool:
    try:
        expected_ending_character = get_matching_character(opening_character)
        matches = expected_ending_character == ending_character
    except IllegalCharacter:
        matches = False
    return matches


def convert_characters_to_points_corrupt_line(
    illegal_characters: List[str],
) -> int:
    illegal_character_score_map = {
        ")": 3,
        "]": 57,
        "}": 1197,
        ">": 25137,
    }  # type: Dict[str, int]
    return sum([illegal_character_score_map[char] for char in illegal_characters])


def convert_characters_to_points_incomplete_line(missing_characters: List[str]) -> int:
    illegal_character_score_map = {
        ")": 1,
        "]": 2,
        "}": 3,
        ">": 4,
    }  # type: Dict[str, int]
    return reduce(
        lambda total, char: (total * 5) + illegal_character_score_map[char],
        missing_characters,
        0,
    )


def main():
    illegal_characters = []  # type: List[str]
    incomplete_lines = []  # type: List[List[str]]
    with open("data/syntax.txt") as f:
        for line in f:
            stack = []
            for character in line.strip():
                if is_opening_character(character):
                    stack.append(character)
                elif is_closing_character(character):
                    try:
                        opening_character = stack.pop()
                    except IndexError:
                        opening_character = "x"
                    if not characters_match(opening_character, character):
                        illegal_characters.append(character)
                        break
                else:
                    raise IllegalCharacter
            else:
                incomplete_line = []  # type: List[str]
                while stack:
                    opening_character = stack.pop()
                    ending_character = get_matching_character(opening_character)
                    incomplete_line.append(ending_character)
                incomplete_lines.append(incomplete_line)
    points = convert_characters_to_points_corrupt_line(illegal_characters)
    print(f"total syntax error score is {points}")

    scores_incomplete_lines = sorted(
        [
            convert_characters_to_points_incomplete_line(incomplete_line)
            for incomplete_line in incomplete_lines
        ]
    )  # type List[int]
    print(
        f"middle score = {scores_incomplete_lines[int(len(scores_incomplete_lines) / 2)]}"
    )


main()
