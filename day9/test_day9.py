from pathlib import Path

from day9 import extrapolate_one_forwards
from notebooks.aoc2023.utils import load_data

test_input = [
"0 3 6 9 12 15",
"1 3 6 10 15 21",
"10 13 16 21 30 45",
]


def test_part1_test_input():
    input_as_lines = test_input
    input_as_list_of_ints = [[int(char) for char in line.split(" ")] for line in input_as_lines]
    assert sum([extrapolate_one_forwards(line) for line in input_as_list_of_ints]) == 114


def test_part2_test_input():
    input_as_lines = test_input
    input_as_list_of_ints = [[int(char) for char in line.split(" ")] for line in input_as_lines]
    assert sum([extrapolate_one_forwards(line[::-1]) for line in input_as_list_of_ints]) == 2


def test_part1():
    input_as_lines = load_data(Path(__file__).parent / "input.txt")
    input_as_list_of_ints = [[int(char) for char in line.split(" ")] for line in input_as_lines]
    assert sum([extrapolate_one_forwards(line) for line in input_as_list_of_ints]) == 1877825184


def test_part2():
    input_as_lines = load_data(Path(__file__).parent / "input.txt")
    input_as_list_of_ints = [[int(char) for char in line.split(" ")] for line in input_as_lines]
    assert sum([extrapolate_one_forwards(line[::-1]) for line in input_as_list_of_ints]) == 1108
