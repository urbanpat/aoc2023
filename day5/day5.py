from pathlib import Path

import numpy as np


def parse_input(p: Path) -> tuple[list[int], dict[str, [list[tuple[int, int, int]]]]]:
    input_as_groups = (p).read_text().split("\n\n")
    seeds = [int(s) for s in input_as_groups[0].split(": ")[1].split(" ")]
    maps = {
        "seed_to_soil_map": [[int(s) for s in line.split(" ")] for line in input_as_groups[1].split("\n")[1:]],
        "soil_to_fertilizer_map": [[int(s) for s in line.split(" ")] for line in input_as_groups[2].split("\n")[1:]],
        "fertilizer_to_water_map": [[int(s) for s in line.split(" ")] for line in input_as_groups[3].split("\n")[1:]],
        "water_to_light_map": [[int(s) for s in line.split(" ")] for line in input_as_groups[4].split("\n")[1:]],
        "light_to_temperature_map": [[int(s) for s in line.split(" ")] for line in input_as_groups[5].split("\n")[1:]],
        "temperature_to_humidity_map": [[int(s) for s in line.split(" ")] for line in input_as_groups[6].split("\n")[1:]],
        "humidity_to_location_map": [[int(s) for s in line.split(" ")] for line in input_as_groups[7].split("\n")[1:] if line],
    }
    return seeds, maps


def apply_map_vectorized(map_range: tuple[int, int, int], what: np.ndarray) -> np.ndarray:
    mask_used = np.zeros_like(what, dtype=bool)
    for target, source, ran in map_range:
        applies_mask = (source <= what) & (what < source + ran)
        applies_mask = applies_mask & (~mask_used)
        if applies_mask.any():
            mask_used |= applies_mask
            what[applies_mask] = target + (what[applies_mask] - source)
    return what


def get_seed_location(seeds: np.ndarray, maps_as_ranges: dict) -> np.ndarray:
    location = seeds.copy()
    for name, mapping in maps_as_ranges.items():
        location = apply_map_vectorized(mapping, location)
    return location


def find_closest_location_for_given_seeds(seeds: list[int], maps_as_ranges: dict[str, tuple[int, int, int]]) -> int:
    min_location = np.inf
    seeds = np.array(seeds)
    locations = get_seed_location(seeds, maps_as_ranges)
    if locations.min() < min_location:
        min_location = locations.min()
    return min_location


def find_closest_location_for_seed_ranges(seeds: list[int], maps_as_ranges: dict[str, tuple[int, int, int]]) -> int:
    min_location = np.inf
    for idx, (seed_start, seed_range) in enumerate(zip(seeds[::2], seeds[1::2])):
        seeds = np.arange(start=seed_start, stop=seed_start + seed_range)
        semi_location = find_closest_location_for_given_seeds(seeds, maps_as_ranges)
        if semi_location < min_location:
            min_location = semi_location
    return min_location


if __name__ == "__main__":
    seed_data, mapping_data = parse_input(Path(__file__).parent / "test_input.txt")

    part1_location = find_closest_location_for_given_seeds(seed_data, mapping_data)
    print(f"part1: {part1_location}")

    part2_location = find_closest_location_for_seed_ranges(seed_data, mapping_data)
    print(f"part2: {part2_location}")
