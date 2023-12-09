from pathlib import Path

import numpy as np

from notebooks.aoc2023.utils import load_data


def parse_input(input_as_lines: list[str]) -> tuple[list[list[int]], list[list[int]]]:
    all_winning_numbers = []
    all_your_numbers = []
    for line in input_as_lines:
        winning, turns = line.split(":")[1].split("|")
        all_winning_numbers.append([int(num) for num in winning.split(" ") if num])
        all_your_numbers.append([int(num) for num in turns.split(" ") if num])
    return all_winning_numbers, all_your_numbers


def get_winnings_from_cards(all_winning_numbers: list[list[int]], all_your_numbers: list[list[int]]) -> int:
    prize = 0
    for winning_numbers, your_numbers in zip(all_winning_numbers, all_your_numbers):
        your_winning_numbers = set(winning_numbers) & set(your_numbers)
        if your_winning_numbers:
            prize += 2 ** (len(your_winning_numbers) - 1)
    return prize


def collect_winning_cards(all_winning_numbers: list[list[int]], all_your_numbers: list[list[int]]) -> int:
    multiples = np.ones(len(all_winning_numbers))
    for idx, (winning_numbers, your_numbers, coef) in enumerate(zip(all_winning_numbers, all_your_numbers, multiples)):
        your_winning_numbers = set(winning_numbers) & set(your_numbers)
        if your_winning_numbers:
            multiples[idx + 1 : idx + 1 + len(your_winning_numbers)] += 1 * coef
    return multiples.sum()


if __name__ == "__main__":
    input = load_data(Path(__file__).parent / "input.txt")

    ans1 = get_winnings_from_cards(*parse_input(input))
    print(f"part1: {ans1}")
    ans2 = collect_winning_cards(*parse_input(input))
    print(f"part2: {ans2}")
