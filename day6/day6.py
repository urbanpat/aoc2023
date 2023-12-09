from pathlib import Path

from notebooks.aoc2023.utils import load_data


def parse_input(text_as_lines: list[str]) -> tuple[list[int], list[int]]:
    times = [int(number) for number in text_as_lines[0].split(":")[1].split(" ") if number]
    distances = [int(number) for number in text_as_lines[1].split(":")[1].split(" ") if number]
    return times, distances


def determine_number_of_wins_per_race(race_time: int, race_distance: int) -> int:
    number_of_options_to_win = 0
    for i in range(race_time):
        if i * (race_time - i) > race_distance:
            number_of_options_to_win += 1
    return number_of_options_to_win


def get_number_of_wins(times: list[int], distances: list[int]) -> int:
    ans = 1
    for time, dist in zip(times, distances):
        ans *= determine_number_of_wins_per_race(time, dist)
    return ans


if __name__ == "__main__":
    input_as_lines = load_data(Path(__file__).parent / "input.txt")
    race_durations, race_records = parse_input(input_as_lines)

    number_of_ways_to_win = get_number_of_wins(race_durations, race_records)
    print(number_of_ways_to_win)

    part2_time = int("".join(str(t) for t in race_durations))
    part2_dist = int("".join(str(d) for d in race_records))

    number_of_ways_to_win2 = determine_number_of_wins_per_race(part2_time, part2_dist)
    print(number_of_ways_to_win2)
