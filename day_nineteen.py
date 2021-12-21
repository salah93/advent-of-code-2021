from __future__ import annotations
from collections import defaultdict
from itertools import combinations
from typing import Dict, List, NamedTuple, Optional, Set, Tuple

import copy


class Coords(NamedTuple):
    x: int
    y: int
    z: int

    def __sub__(self, coords: Coords) -> Translation:
        return Translation(self.x - coords.x, self.y - coords.y, self.z - coords.z)

    def __add__(self, transl: Translation) -> Coords:
        return Coords(self.x + transl.x, self.y + transl.y, self.z + transl.z)


class Translation(NamedTuple):
    x: int
    y: int
    z: int


TRANSFORMATION_FNS = (
    # face z towards x
    lambda coords: Coords(coords.z, coords.y, -1 * coords.x),
    lambda coords: Coords(coords.z, coords.x, coords.y),
    lambda coords: Coords(coords.z, -1 * coords.y, coords.x),
    lambda coords: Coords(coords.z, -1 * coords.x, -1 * coords.y),
    # face z towards -x
    lambda coords: Coords(-1 * coords.z, coords.y, coords.x),
    lambda coords: Coords(-1 * coords.z, coords.x, -1 * coords.y),
    lambda coords: Coords(-1 * coords.z, -1 * coords.y, -1 * coords.x),
    lambda coords: Coords(-1 * coords.z, -1 * coords.x, coords.y),
    # face z towards y
    lambda coords: Coords(coords.x, coords.z, -1 * coords.y),
    lambda coords: Coords(-1 * coords.y, coords.z, -1 * coords.x),
    lambda coords: Coords(-1 * coords.x, coords.z, coords.y),
    lambda coords: Coords(coords.y, coords.z, coords.x),
    # face z towards -y
    lambda coords: Coords(coords.x, -1 * coords.z, coords.y),
    lambda coords: Coords(coords.y, -1 * coords.z, -1 * coords.x),
    lambda coords: Coords(-1 * coords.x, -1 * coords.z, -1 * coords.y),
    lambda coords: Coords(-1 * coords.y, -1 * coords.z, coords.x),
    # face z towards z
    lambda coords: Coords(coords.x, coords.y, coords.z),
    lambda coords: Coords(-1 * coords.y, coords.x, coords.z),
    lambda coords: Coords(-1 * coords.x, -1 * coords.y, coords.z),
    lambda coords: Coords(coords.y, -1 * coords.x, coords.z),
    # face z towards -z
    lambda coords: Coords(-1 * coords.x, coords.y, -1 * coords.z),
    lambda coords: Coords(coords.x, -1 * coords.y, -1 * coords.z),
    lambda coords: Coords(-1 * coords.y, -1 * coords.x, -1 * coords.z),
    lambda coords: Coords(coords.y, coords.x, -1 * coords.z),
)


class Scanner(object):
    def __init__(self, identifier: int):
        self.__identifier = identifier
        self.beacons = []  # type: List[Coords]
        self._scanners_relative_to = {}  # type: Dict[Scanner, Tuple[int, Translation]]

    def __eq__(self, other: Scanner) -> bool:
        return self.__identifier == other.__identifier

    def __hash__(self) -> str:
        return hash(self.__identifier)

    @classmethod
    def get_beacons_relative(
        cls, transf_i: int, translation: Translation, beacons: List[Coords]
    ) -> List[Coords]:
        transf_fn = TRANSFORMATION_FNS[transf_i]

        return [(transf_fn(beacon) + translation) for beacon in beacons]

    def add_beacons(self, coords: List[Coords]) -> Scanner:
        self.beacons.extend(coords)
        return self

    def add_beacon(self, coords: Coords) -> Scanner:
        self.beacons.append(coords)
        return self

    def set_coords(self, coords: Coords) -> Scanner:
        self._coords = coords
        return self

    def compare_to_scanner(self, scanner: Scanner) -> Optional[Tuple[int, Translation]]:
        translations = defaultdict(int)  # type: Dict[Translation, int]
        for fn_i, transformation_fn in enumerate(TRANSFORMATION_FNS):
            for beacon in scanner.beacons:
                for b in self.beacons:
                    transformation = transformation_fn(b)
                    translation = beacon - transformation
                    translations[translation] += 1
                    # atleast 12 beacons map to each other
                    if translations[translation] >= 12:
                        return (fn_i, translation)
        else:
            return None

    def __repr__(self):
        return f"Scanner<{self.__identifier}>"


def main():
    with open("data/beacons_test.txt") as f:
        scanners = []
        for line in f:
            if line.startswith("---"):
                scanner_id = int(line.strip().strip("-").split()[1])
                scanners.append(Scanner(scanner_id))
            elif line.strip():
                x, y, z = [int(pos) for pos in line.strip().split(",")]
                scanners[-1].add_beacon(Coords(x, y, z))

    mappings = defaultdict(
        list
    )  # type: Dict[Scanner, List[Tuple[Scanner, int, Translation]]]
    for scanner_a, scanner_b in combinations(scanners, 2):
        compare_result = scanner_b.compare_to_scanner(scanner_a)
        if compare_result:
            print(f"matched {scanner_b} to {scanner_a}")
            (
                fn_i,
                scanner_b_to_a_translation,
            ) = compare_result
            mappings[scanner_a].append((scanner_b, fn_i, scanner_b_to_a_translation))
            compare_result = scanner_a.compare_to_scanner(scanner_b)
            (
                fn_i,
                scanner_a_to_b_translation,
            ) = compare_result
            mappings[scanner_b].append((scanner_a, fn_i, scanner_a_to_b_translation))
            if len(mappings) == len(scanners):
                break

    def get_beacons_for_scanner(scanner: Scanner) -> List[Coords]:
        def inner(scanner, processed) -> List[Coords]:
            beacons = copy.copy(scanner.beacons)
            processed.add(scanner)
            for other_scanner, fn_i, translation in mappings[scanner]:
                if other_scanner in processed:
                    continue
                other_scanner_beacons = inner(other_scanner, processed)
                beacons.extend(
                    Scanner.get_beacons_relative(
                        fn_i, translation, other_scanner_beacons
                    )
                )
            return beacons

        return list(set(inner(scanner, set())))

    def get_scanner_positions(scanner: Scanner) -> List[Coords]:
        def inner(scanner, processed) -> List[Coords]:
            scanner_positions = [Coords(0, 0, 0)]
            processed.add(scanner)
            for other_scanner, fn_i, translation in mappings[scanner]:
                if other_scanner in processed:
                    continue
                other_scanner_positions = inner(other_scanner, processed)
                scanner_positions.extend(
                    Scanner.get_beacons_relative(
                        fn_i, translation, other_scanner_positions
                    )
                )
            return scanner_positions

        return list(set(inner(scanner, set())))

    beacons = get_beacons_for_scanner(scanners[0])
    print(f"number of beacons = {len(beacons)}")

    def manhattan_distance(coords_a: Coords, coords_b: Coords) -> int:
        return (
            abs(coords_a.x - coords_b.x)
            + abs(coords_a.y - coords_b.y)
            + abs(coords_a.z - coords_b.z)
        )

    scanner_positions = get_scanner_positions(scanners[0])
    largest_distance = 0
    for s_a, s_b in combinations(scanner_positions, 2):
        distance = manhattan_distance(s_a, s_b)
        if distance > largest_distance:
            largest_distance = distance
    print(f"largest distance = {largest_distance}")


main()
