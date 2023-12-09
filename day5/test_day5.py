from pathlib import Path

import numpy as np

from day5 import parse_input, find_closest_location_for_given_seeds, find_closest_location_for_seed_ranges, get_seed_location

def test_part1_example():
    seeds, maps_as_ranges = parse_input(Path(__file__).parent / "test_input.txt")
    part1_location = find_closest_location_for_given_seeds(seeds, maps_as_ranges)
    # 77 µs
    assert part1_location == 35


def test_part2_example():
    seeds, maps_as_ranges = parse_input(Path(__file__).parent / "test_input.txt")
    part2_location = find_closest_location_for_seed_ranges(seeds, maps_as_ranges)
    # 150 µs
    assert part2_location == 46


def test_part2_on_82():
    _, maps_as_ranges = parse_input(Path(__file__).parent / "test_input.txt")
    seeds = np.array([82])
    assert get_seed_location(seeds, maps_as_ranges).item() == 46


def test_part1():
    seeds, maps_as_ranges = parse_input(Path(__file__).parent / "input.txt")
    part1_location = find_closest_location_for_given_seeds(seeds, maps_as_ranges)
    # 576 µs
    assert part1_location == 403695602


def test_part2():
    seeds, maps_as_ranges = parse_input(Path(__file__).parent / "input.txt")
    part2_location = find_closest_location_for_seed_ranges(seeds, maps_as_ranges)
    # 1496.55s (0:24:56) :D
    assert part2_location == 219529182
