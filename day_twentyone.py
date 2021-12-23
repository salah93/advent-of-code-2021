from __future__ import annotations
import random
from typing import NamedTuple


class Player(NamedTuple):
    id: int
    score: int
    curr_position: int


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

    def roll_dice(self, player: Player, dice: Dice) -> Player:
        def inner(times_left: int, paces: int) -> Player:
            if times_left > 0:
                return inner(times_left - 1, paces + dice.roll())
            curr_position = (
                (player.curr_position + paces) % self.board_length
            ) or self.board_length
            return Player(player.id, player.score + curr_position, curr_position)

        return inner(3, 0)

    def roll_dice_dirac(self, player: Player) -> List[Player]:
        def inner(player: Player, times_left: int, paces: int) -> List[Player]:
            if times_left > 0:
                player_outcomes = inner(
                    Player(player.id, player.score, player.curr_position),
                    times_left - 1,
                    paces + 1,
                )
                player_outcomes += inner(
                    Player(player.id, player.score, player.curr_position),
                    times_left - 1,
                    paces + 2,
                )
                player_outcomes += inner(
                    Player(player.id, player.score, player.curr_position),
                    times_left - 1,
                    paces + 3,
                )
                return player_outcomes

            curr_position = (player.curr_position + paces) % self.board_length
            return [
                Player(
                    player.id,
                    player.score + curr_position,
                    curr_position,
                )
            ]

        return inner(player, 3, 0)


# def get_wins_dirac(
#    game: GameBoard,
#    player_one_outcomes: list[Player],
#    player_two_outcomes: list[Player],
#    player_one_wins: int = 0,
#    player_two_wins: int = 0,
# ):
#    for p1 in player_one_outcomes:
#        for p2 in player_two_outcomes:
#            if p1.score >= 21:
#                player_one_wins += 1
#            elif p2.score >= 21:
#                player_two_wins += 1
#            else:
#                player_one_wins, player_two_wins = get_wins_dirac(
#                    game,
#                    game.roll_dice_dirac(p1),
#                    game.roll_dice_dirac(p2),
#                    player_one_wins,
#                    player_two_wins,
#                )
#    return player_one_wins, player_two_wins
#
#
def get_wins_dirac(
    game: GameBoard,
    player_one: Player,
    player_two: Player,
    player_one_wins: int = 0,
    player_two_wins: int = 0,
):
    player_one_outcomes = game.roll_dice_dirac(player_one)
    for p1 in player_one_outcomes:
        if p1.score >= 21:
            player_one_wins += 1
        else:
            for p2 in game.roll_dice_dirac(player_two):
                if p2.score >= 21:
                    player_two_wins += 1
                else:
                    player_one_wins, player_two_wins = get_wins_dirac(
                        game,
                        p1,
                        p2,
                        player_one_wins,
                        player_two_wins,
                    )
    return player_one_wins, player_two_wins


def main():
    with open("data/game_test.txt") as f:
        player_one_curr_position = int(next(f).split(":")[1])
        player_two_curr_position = int(next(f).split(":")[1])
    player_one = Player(1, 0, player_one_curr_position)
    player_two = Player(2, 0, player_two_curr_position)

    # game = GameBoard()
    # dice = DeterminisiticDice(100)
    # curr_player = player_one
    # while not game_over:
    #    curr_player = game.roll_dice(curr_player, dice):
    #    game_over = curr_player.score >= 100
    #    curr_player = player_one if curr_player == player_two else player_two

    # print(f"number of times rolled = {dice.number_of_times_rolled}")
    # print(f"player one scored {player_one.score}")
    # print(f"player two scored {player_two.score}")
    # print(
    #    f"product {dice.number_of_times_rolled * min(player_two.score, player_one.score)}"
    # )
    game = GameBoard(winning_threshold=21)
    player_one_wins, player_two_wins = get_wins_dirac(game, player_one, player_two)
    print(f"player one wins = {player_one_wins}")
    print(f"player two wins = {player_two_wins}")


main()
