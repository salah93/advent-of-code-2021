import random


class Player(object):
    def __init__(self, id: int):
        self.id = id
        self.score = 0
        self.curr_position = 1


class Dice(object):
    def __init__(self, sides: int):
        self.number_of_times_rolled = 0
        self.sides = sides

    def roll(self) -> int:
        self.number_of_times_rolled += 1
        return random.randint(1, self.sides)


class DeterminisiticDice(Dice):
    def roll(self):
        super().roll()
        return (self.number_of_times_rolled % self.sides) or self.sides


class DiracDice(Dice):
    def __init__(self):
        super().__init__(3)

    def roll(self):
        super().roll()


class GameBoard(object):
    def __init__(self, board_length: int = 10, winning_threshold: int = 1000):
        self.board_length = board_length
        self.winning_threshold = winning_threshold

    def roll_dice(self, player: Player, dice: Dice) -> bool:
        def inner(times_left: int, paces: int) -> bool:
            if times_left > 0:
                return inner(times_left - 1, paces + dice.roll())
            player.curr_position = (
                (player.curr_position + paces) % self.board_length
            ) or self.board_length
            player.score += player.curr_position
            return player.score >= self.winning_threshold

        return inner(3, 0)


def main():
    player_one = Player(1)
    player_two = Player(2)
    with open("data/game.txt") as f:
        player_one.curr_position = int(next(f).split(":")[1])
        player_two.curr_position = int(next(f).split(":")[1])

    game = GameBoard()
    dice = DeterminisiticDice(100)
    curr_player = player_one
    while not game.roll_dice(curr_player, dice):
        curr_player = player_one if curr_player == player_two else player_two

    print(f"number of times rolled = {dice.number_of_times_rolled}")
    print(f"player one scored {player_one.score}")
    print(f"player two scored {player_two.score}")
    print(
        f"product {dice.number_of_times_rolled * min(player_two.score, player_one.score)}"
    )


main()
