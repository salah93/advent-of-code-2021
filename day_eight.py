from typing import List, NamedTuple, Tuple


class Segment(NamedTuple):
    display: int
    number_of_segments: int


def main():
    entries = []  # type: List[Tuple[List[str], List[str]]]
    with open("data/seven_segment.txt") as f:
        for line in f:
            entry = line.split("|")  # type: Tuple[str, str]
            unique_patterns_list = [
                seg.strip() for seg in entry[0].split() if seg.strip()
            ]  # type List[str]
            output_list = [
                seg.strip() for seg in entry[1].split() if seg.strip()
            ]  # type: List[str]
            entries.append((unique_patterns_list, output_list))

    numbers_segments = [
        Segment(display=0, number_of_segments=6),
        Segment(display=1, number_of_segments=2),
        Segment(display=2, number_of_segments=5),
        Segment(display=3, number_of_segments=5),
        Segment(display=4, number_of_segments=4),
        Segment(display=5, number_of_segments=5),
        Segment(display=6, number_of_segments=6),
        Segment(display=7, number_of_segments=3),
        Segment(display=8, number_of_segments=7),
        Segment(display=9, number_of_segments=5),
    ]  # type: List[Segment]

    numbers_with_unique_number_of_segments = []  # type: List[Segment
    for i in range(1, 8):
        filtered_number_segments = [
            n for n in numbers_segments if n.number_of_segments == i
        ]  # type: List[Segment]
        if len(filtered_number_segments) == 1:
            numbers_with_unique_number_of_segments.append(filtered_number_segments[0])

    unique_segment_count = 0
    for patterns, output in entries:
        for digit in output:
            filtered_number_segments = [
                s
                for s in numbers_with_unique_number_of_segments
                if s.number_of_segments == len(digit)
            ]  # type: List[Segment]
            if len(filtered_number_segments):
                unique_segment_count += 1
    print(f"unique segments = {unique_segment_count}")


main()
