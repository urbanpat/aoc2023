from pathlib import Path

import cv2
import numpy as np
from numpy.core.defchararray import isnumeric

from notebooks.aoc2023.utils import load_data


def dilate_mask(mask: np.ndarray) -> np.ndarray:
    kernel = np.ones((3, 3), np.uint8)
    return cv2.dilate(mask.astype(np.uint8), kernel, iterations=1).astype(bool)


def read_number_from_number_mask(input_arr: np.ndarray, number_labels: np.ndarray, label: int):
    number_mask = number_labels == label
    return int("".join(input_arr[number_mask]))


def get_sum_of_part_numbers(input_arr: np.ndarray) -> int:
    number_chars_mask = isnumeric(input_arr)
    dots_mask = input_arr == "."
    symbols_mask = (~dots_mask) & (~number_chars_mask)
    chars_adjacent_to_symbols = dilate_mask(symbols_mask) & number_chars_mask

    _, number_labels, _, _ = cv2.connectedComponentsWithStats(number_chars_mask.astype(np.uint8))
    return sum(get_part_numbers_from_labels(number_labels, input_arr, chars_adjacent_to_symbols))


def get_part_numbers_from_labels(number_labels: np.ndarray, input_arr: np.ndarray, chars_adjacent_to_symbols: np.ndarray) -> list[int]:
    part_numbers = []
    for label in range(number_labels.max()):
        number_mask = number_labels == (label + 1)
        if (number_mask & chars_adjacent_to_symbols).any():
            part_numbers.append(read_number_from_number_mask(input_arr, number_labels, label + 1))
    return part_numbers


def get_sum_of_gear_ratios(input_arr: np.ndarray) -> int:
    number_chars_mask = isnumeric(input_arr)
    _, number_labels, _, _ = cv2.connectedComponentsWithStats(number_chars_mask.astype(np.uint8))

    stars_mask = input_arr == "*"
    _, star_labels, _, _ = cv2.connectedComponentsWithStats(stars_mask.astype(np.uint8))

    return sum(get_gear_ratios_from_labels(input_arr, star_labels, number_labels))


def get_gear_ratios_from_labels(input_arr: np.ndarray, star_labels: np.ndarray, number_labels: np.ndarray) -> list[int]:
    gear_ratios = []
    for label in range(star_labels.max()):
        star_mask = star_labels == (label + 1)
        bigger_star = dilate_mask(star_mask)
        uniq_hits = np.unique(number_labels[bigger_star.astype(bool)])
        if (uniq_hits > 0).sum() == 2:  # label 0 corresponds with background
            l1, l2 = tuple(uniq_hits[uniq_hits > 0])
            gear_p1 = read_number_from_number_mask(input_arr, number_labels, l1)
            gear_p2 = read_number_from_number_mask(input_arr, number_labels, l2)
            gear_ratios.append(gear_p1 * gear_p2)
    return gear_ratios


if __name__ == "__main__":
    input_as_lines = load_data(Path(__file__).parent / "input.txt")
    input_as_arr = np.array([list(l) for l in input_as_lines])

    answer1 = get_sum_of_part_numbers(input_as_arr)
    print(f"part1: {answer1}")

    answer2 = get_sum_of_gear_ratios(input_as_arr)
    print(f"part2: {answer2}")
