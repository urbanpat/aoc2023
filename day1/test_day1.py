from pathlib import Path

from day1 import get_calibration_value_from_line
from notebooks.aoc2023.utils import load_data

test_input = [
    "1abc2",
    "pqr3stu8vwx",
    "a1b2c3d4e5f",
    "treb7uchet",
]

test_input2 = [
    "two1nine",
    "eightwothree",
    "abcone2threexyz",
    "xtwone3four",
    "4nineeightseven2",
    "zoneight234",
    "7pqrstsixteen",
]


def test_part1_test_input1():
    assert sum([get_calibration_value_from_line(line) for line in test_input]) == 142


def test_part2_test_input2():
    assert sum([get_calibration_value_from_line(line) for line in test_input2]) == 281


def test_part2():
    data = load_data(Path(__file__).parent / "input.txt")
    calibration_values = [get_calibration_value_from_line(line) for line in data]
    assert sum(calibration_values) == 53855

