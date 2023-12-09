from pathlib import Path

import pytest

from day8 import parse_input, compute_steps_from_aaa_to_zzz, compute_steps_from_xxa_to_xxz_trick, compute_steps_from_xxa_to_xxz_brute_force
from notebooks.aoc2023.utils import load_data

test_input = [
    "RL",
    "",
    "AAA = (BBB, CCC)",
    "BBB = (DDD, EEE)",
    "CCC = (ZZZ, GGG)",
    "DDD = (DDD, DDD)",
    "EEE = (EEE, EEE)",
    "GGG = (GGG, GGG)",
    "ZZZ = (ZZZ, ZZZ)",
]


def test_part1_test_input():
    input_as_lines = test_input
    instructions = input_as_lines[0]
    left_map, right_map = parse_input(input_as_lines[2:])

    assert compute_steps_from_aaa_to_zzz(instructions, left_map, right_map) == 2


test_input2 = [
    "LLR",
    "",
    "AAA = (BBB, BBB)",
    "BBB = (AAA, ZZZ)",
    "ZZZ = (ZZZ, ZZZ)",
]


def test_part1_test_input2():
    input_as_lines = test_input2
    instructions = input_as_lines[0]
    left_map, right_map = parse_input(input_as_lines[2:])

    assert compute_steps_from_aaa_to_zzz(instructions, left_map, right_map) == 6


def test_part1():
    input_as_lines = load_data(Path(__file__).parent / "input.txt")
    instructions = input_as_lines[0]
    left_map, right_map = parse_input(input_as_lines[2:])

    assert compute_steps_from_aaa_to_zzz(instructions, left_map, right_map) == 20221


test_input3 = [
    "LR",
    "",
    "11A = (11B, XXX)",
    "11B = (XXX, 11Z)",
    "11Z = (11B, XXX)",
    "22A = (22B, XXX)",
    "22B = (22C, 22C)",
    "22C = (22Z, 22Z)",
    "22Z = (22B, 22B)",
    "XXX = (XXX, XXX)",
]


def test_part2_test_input_bf():
    input_as_lines = test_input3
    instructions = input_as_lines[0]
    left_map, right_map = parse_input(input_as_lines[2:])

    assert compute_steps_from_xxa_to_xxz_brute_force(instructions, left_map, right_map) == 6


@pytest.mark.skip
def test_part2_bf():
    input_as_lines = load_data(Path(__file__).parent / "input.txt")
    instructions = input_as_lines[0]
    left_map, right_map = parse_input(input_as_lines[2:])

    assert compute_steps_from_xxa_to_xxz_brute_force(instructions, left_map, right_map) == 14616363770447
    # would need to run for 11s * 14616363770447 / 10000000 ~ 190days


def test_part2_trick():
    input_as_lines = load_data(Path(__file__).parent / "input.txt")
    instructions = input_as_lines[0]
    left_map, right_map = parse_input(input_as_lines[2:])

    assert compute_steps_from_xxa_to_xxz_trick(instructions, left_map, right_map) == 14616363770447
