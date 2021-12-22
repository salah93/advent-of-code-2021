from __future__ import annotations
from collections.abc import Iterator
from typing import NamedTuple


class Pixel(NamedTuple):
    row: int
    column: int
    bit: int


class PixelOutOfBounds(Exception):
    pass


class Image(Iterator):
    def __init__(self):
        self._grid = []  # type: list[list[Pixel]]
        self._curr_pixel = None

    def add_pixels(self, row: list[int]) -> Image:
        row_i = len(self._grid)
        self._grid.append(
            [Pixel(row=row_i, column=i, bit=bit) for i, bit in enumerate(row)]
        )
        return self

    def set_pixels(self, pixels: list[Pixel]) -> Image:
        normalize_factor = abs(min([p.row for p in pixels]))
        for pixel in pixels:
            row_i = pixel.row + normalize_factor
            column_i = pixel.column + normalize_factor
            new_pixel = Pixel(row=row_i, column=column_i, bit=pixel.bit)
            if len(self._grid) == row_i:
                self._grid.append([])
            elif len(self._grid) < row_i:
                raise PixelOutOfBounds
            row = self._grid[row_i]
            if len(row) == column_i:
                row.append(new_pixel)
            elif len(row) < column_i:
                raise PixelOutOfBounds
            else:
                row[column_i] = new_pixel
        return self

    def __iter__(self) -> Iterator:
        return self

    def __next__(self) -> Pixel:
        if len(self._grid) == 0:
            raise StopIteration
        if self._curr_pixel is None:
            self._curr_pixel = self._get_pixel(-1, -1)
        if self._curr_pixel.row == (len(self._grid) + 1):
            self._curr_pixel = None
            raise StopIteration
        if self._curr_pixel.column == (len(self._grid[0])):
            column_i = -1
            row_i = self._curr_pixel.row + 1
        else:
            column_i = self._curr_pixel.column + 1
            row_i = self._curr_pixel.row
        curr_pixel = self._curr_pixel
        self._curr_pixel = self._get_pixel(row_i, column_i)
        return curr_pixel

    def get_surrounding_pixels(self, pixel: Pixel) -> list[Pixel]:
        return [
            # top left
            self._get_pixel(pixel.row - 1, pixel.column - 1),
            # top
            self._get_pixel(pixel.row - 1, pixel.column),
            # top right
            self._get_pixel(pixel.row - 1, pixel.column + 1),
            # left
            self._get_pixel(pixel.row, pixel.column - 1),
            # current
            pixel,
            # right
            self._get_pixel(pixel.row, pixel.column + 1),
            # bottom left
            self._get_pixel(pixel.row + 1, pixel.column - 1),
            # bottom
            self._get_pixel(pixel.row + 1, pixel.column),
            # bottom right
            self._get_pixel(pixel.row + 1, pixel.column + 1),
        ]

    def _get_pixel(self, row_i: int, column_i: int) -> Pixel:
        if row_i < 0 or column_i < 0:
            pixel = Pixel(row=row_i, column=column_i, bit=0)
        else:
            try:
                pixel = self._grid[row_i][column_i]
            except IndexError:
                pixel = Pixel(row=row_i, column=column_i, bit=0)
        return pixel

    def display(self) -> str:
        display = ""
        for row in self._grid:
            for pixel in row:
                display += "." if pixel.bit == 0 else "#"
            display += "\n"
        return display

    def get_pixels_lit_up(self) -> list[Pixel]:
        pixels = []
        for row in self._grid:
            pixels.extend([p for p in row if p.bit])
        return pixels


def process_image(input_image: Image, algorithm: str) -> Image:
    pixels = []  # type: list[Pixel]
    for pixel in input_image:
        surrounding_pixels = input_image.get_surrounding_pixels(pixel)
        bit_str = "".join([str(p.bit) for p in surrounding_pixels])
        index = int(bit_str, 2)
        new_pixel = Pixel(
            row=pixel.row, column=pixel.column, bit=0 if algorithm[index] == "." else 1
        )
        pixels.append(new_pixel)
    return Image().set_pixels(pixels)


def main():
    input_image = Image()
    with open("data/image_input_test.txt") as f:
        algorithm = next(f).strip()
        for line in f:
            if line.strip():
                input_image.add_pixels([0 if n == "." else 1 for n in line.strip()])
    print(input_image.display())

    output_image_1 = process_image(input_image, algorithm)
    print(output_image_1.display())
    print(len(output_image_1.get_pixels_lit_up()))

    output_image_2 = process_image(output_image_1, algorithm)
    print(output_image_2.display())
    print(len(output_image_2.get_pixels_lit_up()))


main()
