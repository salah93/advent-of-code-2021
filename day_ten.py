from typing import Dict, List


class IllegalCharacter(Exception):
    pass


def is_closing_character(character: str) -> bool:
    return character in ["}", "]", ">", ")"]


def is_opening_character(character: str) -> bool:
    return character in ["{", "[", "<", "("]


def characters_match(stack: List[str], ending_character: str) -> bool:
    try:
        opening_character = stack.pop()
    except IndexError:
        opening_character == "x"
    return (
        (opening_character == "{" and ending_character == "}")
        or (opening_character == "(" and ending_character == ")")
        or (opening_character == "<" and ending_character == ">")
        or (opening_character == "[" and ending_character == "]")
    )


def convert_characters_to_points(illegal_characters: str) -> List[int]:
    illegal_character_score_map = {
        ")": 3,
        "]": 57,
        "}": 1197,
        ">": 25137,
    }  # type: Dict[str, int]
    return [illegal_character_score_map[char] for char in illegal_characters]


def main():
    illegal_characters = []  # type: List[str]
    with open("data/syntax.txt") as f:
        for line in f:
            stack = []
            for character in line.strip():
                if is_opening_character(character):
                    stack.append(character)
                elif is_closing_character(character):
                    if not characters_match(stack, character):
                        illegal_characters.append(character)
                        break
                else:
                    raise IllegalCharacter
    points = convert_characters_to_points(illegal_characters)
    print(f"total syntax error score is {sum(points)}")


main()
