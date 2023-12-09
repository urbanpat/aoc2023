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


def find_words_line(line: str) -> tuple[list[int], list[str]]:
    values = []
    positions = []
    for word, value in NUMBER_AS_WORD.items():
        sub_line = line
        starting_position = 0
        while word in sub_line:
            position = sub_line.index(word)
            positions.append(starting_position + position)
            values.append(value)
            sub_line = sub_line[position + len(word) :]
            starting_position += position + len(word)
    return positions, values


def get_calibration_value_from_line(line: str) -> int:
    positions_numeric, values_numeric = find_numbers_in_line(line)
    positions_wordy, values_wordy = find_words_line(line)
    positions = positions_numeric + positions_wordy
    values = values_numeric + values_wordy
    order = np.argsort(positions)

    return int(values[order[0]] + values[order[-1]])


if __name__ == "__main__":
    data = load_data(Path(__file__).parent / "input.txt")
    calibration_values = [get_calibration_value_from_line(line) for line in data]

    answer = sum(calibration_values)
    print(f"{answer=}")
    # 10ms, 40min
