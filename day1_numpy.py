from pathlib import Path

import numpy as np
from numpy.core.defchararray import isnumeric

from notebooks.aoc2023.utils import load_data

NUMBER_AS_WORD = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


def find_numbers_in_line(line: str) -> tuple[list[int], list[str]]:
    as_array = np.array([*line])
    numeric_mask = isnumeric(as_array)
    numeric_positions = np.where(numeric_mask)[0]
    numbers = as_array[numeric_mask]
    return list(numeric_positions), list(numbers)


def get_calibration_value_from_line(line: str) -> int:
    values, positions = [], []
    for word, value in NUMBER_AS_WORD.items():
        line_with_replaced_words = line.replace(word, value + "x" * (len(word) - 1))
        positions_numeric, values_numeric = find_numbers_in_line(line_with_replaced_words)
        positions.extend(positions_numeric)
        values.extend(values_numeric)
    order = np.argsort(positions)
    return int(values[order[0]] + values[order[-1]])


if __name__ == "__main__":
    data = load_data(Path(__file__).parent / "input.txt")
    calibration_values = [get_calibration_value_from_line(line) for line in data]

    answer = sum(calibration_values)
    print(f"{answer=}")
    # 66ms, +5 min
