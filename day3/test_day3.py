from pathlib import Path

import numpy as np

from day3 import get_sum_of_gear_ratios, get_sum_of_part_numbers
from notebooks.aoc2023.utils import load_data

TEST_INPUT = [
    "467..114..",
    "...*......",
    "..35..633.",
    "......#...",
    "617*......",
    ".....+.58.",
    "..592.....",
    "......755.",
    "...$.*....",
    ".664.598..",
]


def test_example_part1():
    input_as_lines = TEST_INPUT
    input_as_arr = np.array([list(l) for l in input_as_lines])
    assert get_sum_of_part_numbers(input_as_arr) == 4361


def test_example_part2():
    input_as_lines = TEST_INPUT
    input_as_arr = np.array([list(l) for l in input_as_lines])
    assert get_sum_of_gear_ratios(input_as_arr) == 467835


def test_data_part1():
    input_as_lines = load_data(Path(__file__).parent / "input.txt")
    input_as_arr = np.array([list(l) for l in input_as_lines])
    assert get_sum_of_part_numbers(input_as_arr) == 556057


def test_data_part2():
    input_as_lines = load_data(Path(__file__).parent / "input.txt")
    input_as_arr = np.array([list(l) for l in input_as_lines])
    assert get_sum_of_gear_ratios(input_as_arr) == 82824352
