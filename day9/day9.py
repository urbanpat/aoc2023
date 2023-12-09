from pathlib import Path

import numpy as np

from notebooks.aoc2023.utils import load_data


def extrapolate_one_forwards(lines: list[int]) -> int:
    line_diff = np.diff(lines)
    last_elements = [lines[-1], line_diff[-1]]
    while line_diff.any():
        line_diff = np.diff(line_diff)
        last_elements.append(line_diff[-1])

    return sum(last_elements)


if __name__ == "__main__":
    input_as_lines = load_data(Path(__file__).parent / "input.txt")
    input_as_list_of_ints = [[int(char) for char in line.split(" ")] for line in input_as_lines]

    extrapolated_forwards = [extrapolate_one_forwards(line) for line in input_as_list_of_ints]
    backwards = [extrapolate_one_forwards(line[::-1]) for line in input_as_list_of_ints]

    ans1 = sum(extrapolated_forwards)
    print(ans1)

    ans2 = sum(backwards)
    print(ans2)
