from scipy.optimize import minimize
from shapely.geometry import Point, Polygon
from typing import NamedTuple, Tuple, List


class Slope(NamedTuple):
    x: int
    y: int


def point_missed_target(point: Point, target: Polygon) -> bool:
    _, miny, _, _ = target.bounds
    return point.y < miny


def trajectory_hits_target(slope: Slope, target: Polygon) -> Tuple[bool, List[Point]]:
    def inner(point: Point, slope: Slope, path: List[Point]) -> bool:
        # if point == Point(21, -10):
        #    import pdb; pdb.set_trace()
        if target.intersects(point.buffer(0.5)):
            return True, path
        elif point_missed_target(point, target):
            return False, path
        else:
            new_point = Point(point.x + slope.x, point.y + slope.y)
            if slope.x > 0:
                new_slope_x = slope.x - 1
            elif slope.x < 0:
                new_slope_x = slope.x + 1
            else:
                new_slope_x = slope.x
            return inner(new_point, Slope(new_slope_x, slope.y - 1), path + [new_point])

    return inner(Point(0, 0), slope, [])


def main():
    with open("data/target.txt") as f:
        target_area = f.read().strip()
        "target area: x=20..30, y=-10..-5"
        x_area, y_area = target_area.lstrip("target area: ").split(", ")
        min_x, max_x = (int(x) for x in x_area[2:].split(".."))
        min_y, max_y = (int(y) for y in y_area[2:].split(".."))
    target = Polygon(
        [
            Point(min_x, min_y),
            Point(min_x, max_y),
            Point(max_x, min_y),
            Point(max_x, max_y),
        ]
    )

    # 17! is 153 meaning it will not move further rightward at point 153
    # 19! is 190 meaning it will not move further rightward at point 153
    # 113 was trial and error tbh
    slope = Slope(17, 113)
    hits, path = trajectory_hits_target(slope, target)
    if hits:
        print(f"Slope {slope} hits target area {target}")
        print(f"max is {max([p.y for p in path])}")


main()
