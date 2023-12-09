from pathlib import Path

from math import floor, ceil

from day6 import parse_input
from notebooks.aoc2023.utils import load_data


def determine_number_of_wins_per_race_analytical(race_time: int, race_distance: int) -> int:
    a = 1
    b = -race_time
    c = race_distance
    D = b * b - 4 * a * c
    d = D**0.5
    x_bigger = (-b + d) / (2 * a)
    x_smaller = (-b - d) / (2 * a)

    return floor(x_bigger) - ceil(x_smaller) + 1 - x_smaller.is_integer() - x_bigger.is_integer()


def get_number_of_wins(times: list[int], distances: list[int]) -> int:
    ans = 1
    for time, dist in zip(times, distances):
        ans *= determine_number_of_wins_per_race_analytical(time, dist)
    return ans


if __name__ == "__main__":
    input_as_lines = load_data(Path(__file__).parent / "input.txt")
    race_durations, race_records = parse_input(input_as_lines)

    number_of_ways_to_win = get_number_of_wins(race_durations, race_records)
    print(number_of_ways_to_win)

    part2_time = int("".join(str(t) for t in race_durations))
    part2_dist = int("".join(str(d) for d in race_records))

    number_of_ways_to_win2 = determine_number_of_wins_per_race_analytical(part2_time, part2_dist)
    print(number_of_ways_to_win2)
