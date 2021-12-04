import re

from collections import deque, namedtuple
from typing import List, Optional


class BingoItem(object):
    def __init__(self, value: int, marked: bool = False):
        self.value = value
        self.marked = marked


Position = namedtuple("Position", ["row", "column"])


class BingoBoard(object):
    def __init__(self):
        self.data = []  # List[List[BingoItem]]
        self.is_completed = False

    def add_row(self, data: List[int]):
        bingo_data = [BingoItem(d) for d in data]
        self.data.append(bingo_data)

    @property
    def is_populated(self):
        is_populated = len(self.data) == 5
        for row in self.data:
            is_populated = is_populated and len(row) == 5
        return is_populated

    def get_row(self, row: int) -> List[BingoItem]:
        return self.data[row]

    def get_column(self, column: int) -> List[BingoItem]:
        return [d[column] for d in self.data]

    def get_item(self, pos: Position) -> BingoItem:
        return self.data[pos.row][pos.column]

    def get_positions_for_value(self, value: int) -> List[Position]:
        positions = []  # type: List[Position]
        for row_i, row in enumerate(self.data):
            for col_i, item in enumerate(row):
                if not item.marked and item.value == value:
                    positions.append(Position(row=row_i, column=col_i))
        return positions

    def mark_item_at_position(self, pos: Position) -> BingoItem:
        item = self.get_item(pos)
        item.marked = True
        return item

    def mark_items_with_value(self, value: int) -> List[BingoItem]:
        positions = self.get_positions_for_value(value)
        items = []  # type: List[BingoItem]
        for position in positions:
            items.append(self.mark_item_at_position(position))
        return items

    def get_unmarked_values(self) -> List[int]:
        items = []  # type: List[int]
        for row in self.data:
            for item in row:
                if not item.marked:
                    items.append(item.value)
        return items

    def bingo(self) -> bool:
        return self._bingo_for_rows() or self._bingo_for_columns()

    def _bingo_for_rows(self) -> bool:
        bingo = False
        for i in range(5):
            bingo = bingo or all([d.marked for d in self.get_row(i)])
        return bingo

    def _bingo_for_columns(self) -> bool:
        bingo = False
        for i in range(5):
            bingo = bingo or all([d.marked for d in self.get_column(i)])
        return bingo

    def display(self):
        total_display = ""
        for row in self.data:
            for item in row:
                total_display += f"*{item.value:2}*" if item.marked else f" {item.value} "
                total_display += " "
            total_display += "\n"
        return total_display


def main():
    boards = []  # type: List[BingoBoard]
    numbers_draw = deque()  # type: List[int]
    pattern = re.compile(
        r"^(?P<first>(\d|\s)\d )(?P<second>(\d|\s)\d )(?P<third>(\d|\s)\d )(?P<fourth>(\d|\s)\d )(?P<fifth>(\d|\s)\d)$"
    )
    with open("bingo.txt") as f:
        numbers_draw = deque([int(d) for d in next(f).split(",")])
        board = BingoBoard()
        for line in f:
            match = pattern.match(line.rstrip())
            if match:
                board.add_row([int(d) for d in match.groupdict().values()])
            else:
                board = BingoBoard()
            if board.is_populated:
                boards.append(board)


    winning_boards = []  # type: List[Tuple[BingoBoard, int]]
    number_drawn = numbers_draw.popleft()
    while len(winning_boards) < len(boards) and numbers_draw:
        remaining_boards = [b for b in boards if not b.is_completed]
        for board in remaining_boards:
            board.mark_items_with_value(number_drawn)
            if board.bingo():
                board.is_completed = True
                winning_boards.append((board, number_drawn))
        number_drawn = numbers_draw.popleft()

    if len(winning_boards):
        for winning_board, winning_number in winning_boards:
            print(
                f"""
                    winning draw = {winning_number}
                    board =
{winning_board.display()}
                    score = {sum(winning_board.get_unmarked_values()) * winning_number}
                """
            )

main()
