from dataclasses import dataclass, astuple
from pathlib import Path

import numpy as np

from notebooks.aoc2023.utils import load_data


@dataclass
class Turn:
    red: int = 0
    green: int = 0
    blue: int = 0


def parse_cube_numbers_and_color(turn: str) -> dict[str, int]:
    count, color = turn.split(" ")
    return {color: int(count)}


def parse_turns(turn_string: str) -> Turn:
    turn_as_dict = {}
    if "," in turn_string:
        for cube in turn_string.split(", "):
            turn_as_dict |= parse_cube_numbers_and_color(cube)
    else:
        turn_as_dict |= parse_cube_numbers_and_color(turn_string)
    return Turn(**turn_as_dict)


def parse_input(lines: list[str]) -> list[tuple[int, list[Turn]]]:
    game_id_turns = []
    for line in lines:
        game_id, turns = line.split(": ")
        game_id = int(game_id.split("Game ")[1])
        turns_per_game = [parse_turns(turn) for turn in turns.split("; ")]
        game_id_turns.append((game_id, turns_per_game))
    return game_id_turns


def get_max_cubes_per_color_per_game(game_id_turns: list[tuple[int, list[Turn]]]) -> list[tuple[int, Turn]]:
    max_cubes_turn = []
    for game_id, turns in game_id_turns:
        cube_counts = np.array([astuple(t) for t in turns])
        max_counts = cube_counts.max(axis=0)
        max_cubes_turn.append((game_id, Turn(*max_counts)))
    return max_cubes_turn


if __name__ == "__main__":
    input_as_lines = load_data(Path(__file__).parent / "input.txt")

    threshold = np.array([12, 13, 14])
    max_cubes_in_game = get_max_cubes_per_color_per_game(parse_input(input_as_lines))

    viable_data = [game_id for game_id, turn in max_cubes_in_game if (np.array(astuple(turn)) <= threshold).all()]
    answer1 = sum(viable_data)
    print(f"{answer1=}")

    answer2 = np.array([astuple(turn) for _, turn in max_cubes_in_game]).prod(1).sum()
    print(f"{answer2=}")
