from dataclasses import astuple
from pathlib import Path

import numpy as np

from day2 import parse_input, get_max_cubes_per_color_per_game
from notebooks.aoc2023.utils import load_data

test_input1 = [
    "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green",
    "Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue",
    "Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red",
    "Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red",
    "Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green",
]


def test_part1_part2_test_input():
    test_threshold = np.array([12, 12, 12])
    input_as_lines = test_input1
    max_cubes_in_game = get_max_cubes_per_color_per_game(parse_input(input_as_lines))

    viable_data = [game_id for game_id, turn in max_cubes_in_game if (np.array(astuple(turn)) <= test_threshold).all()]

    assert sum(viable_data) == 8

    answer2 = np.array([astuple(turn) for _, turn in max_cubes_in_game]).prod(1).sum()

    assert answer2 == 2286


def test_part1_part2():
    threshold = np.array([12, 13, 14])
    input_as_lines = load_data(Path(__file__).parent / "input.txt")
    max_cubes_in_game = get_max_cubes_per_color_per_game(parse_input(input_as_lines))

    viable_data = [game_id for game_id, turn in max_cubes_in_game if (np.array(astuple(turn)) <= threshold).all()]

    assert sum(viable_data) == 2237

    answer2 = np.array([astuple(turn) for _, turn in max_cubes_in_game]).prod(1).sum()

    assert answer2 == 66681
