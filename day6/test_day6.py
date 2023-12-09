from pathlib import Path

from day6 import parse_input, determine_number_of_wins_per_race, get_number_of_wins
from notebooks.aoc2023.utils import load_data

test_input = [
    "Time:      7  15   30",
    "Distance:  9  40  200",
]


def test_part1_test_input():
    assert get_number_of_wins(*parse_input(test_input)) == 288


def test_part2_test_input():
    input_as_lines = test_input

    times, distances = parse_input(input_as_lines)
    part2_time = int("".join(str(t) for t in times))
    part2_dist = int("".join(str(d) for d in distances))

    assert determine_number_of_wins_per_race(part2_time, part2_dist) == 71503


def test_part1():
    input_as_lines = load_data(Path(__file__).parent / "input.txt")
    assert get_number_of_wins(*parse_input(input_as_lines)) == 1084752


def test_part2():
    input_as_lines = load_data(Path(__file__).parent / "input.txt")

    times, distances = parse_input(input_as_lines)
    part2_time = int("".join(str(t) for t in times))
    part2_dist = int("".join(str(d) for d in distances))

    assert determine_number_of_wins_per_race(part2_time, part2_dist) == 28228952
