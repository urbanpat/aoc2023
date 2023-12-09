from pathlib import Path

import pytest

from day7 import get_hand_rank, Hand, compute_total_winnings_under_given_ordering, get_max_rank, cards_to_rank, cards_to_max_rank
from notebooks.aoc2023.utils import load_data


def test_get_five():
    camel_rank = get_hand_rank("AAAAA")
    assert camel_rank == 1


def test_get_four():
    camel_rank = get_hand_rank("KJKKK")
    assert camel_rank == 2


def test_get_full_house():
    camel_rank = get_hand_rank("KJKJK")
    assert camel_rank == 3


def test_get_three():
    camel_rank = get_hand_rank("25822")
    assert camel_rank == 4


def test_get_two_pairs():
    camel_rank = get_hand_rank("2244J")
    assert camel_rank == 5


def test_get_one_pairs():
    camel_rank = get_hand_rank("2247J")
    assert camel_rank == 6


def test_get_high_card():
    camel_rank = get_hand_rank("283JA")
    assert camel_rank == 7


def test_get_rank_input0():
    camel_rank = get_hand_rank("32T3K")
    assert camel_rank == 6


def test_get_rank_input1():
    camel_rank = get_hand_rank("T55J5")
    assert camel_rank == 4


def test_get_rank_input2():
    camel_rank = get_hand_rank("KK677")
    assert camel_rank == 5


def test_get_rank_input3():
    camel_rank = get_hand_rank("KTJJT")
    assert camel_rank == 5


def test_get_rank_input4():
    camel_rank = get_hand_rank("QQQJA")
    assert camel_rank == 4


test_input = [
    "32T3K 765",
    "T55J5 684",
    "KK677 28",
    "KTJJT 220",
    "QQQJA 483",
]


def test_sorting1():
    input_as_lines = test_input
    hands = [Hand(*line.split(" ")) for line in input_as_lines]

    h0 = hands[0]
    other_hands = hands[1:]
    assert sum(h0 < h for h in other_hands)


def test_sorting2():
    h1 = Hand("KK677", "28")
    h2 = Hand("KTJJT", "220")

    assert h1.max_rank == h2.max_rank
    assert h1 > h2


def test_sorting3():
    h1 = Hand("T55J5", "28")
    h2 = Hand("QQQJA", "220")

    assert h1.max_rank == h2.max_rank
    assert h2 > h1


def test_part1_test_input():
    input_as_lines = test_input
    hands = sorted([Hand(*line.split(" ")) for line in input_as_lines])

    assert sum(int(h.bid) * i for i, h in enumerate(hands, 1)) == 6440


def test_part1_test_input_func():
    input_as_lines = test_input
    assert compute_total_winnings_under_given_ordering(input_as_lines, get_hand_rank, cards_to_rank) == 6440


def test_part2_test_input_func():
    input_as_lines = test_input
    assert compute_total_winnings_under_given_ordering(input_as_lines, get_max_rank, cards_to_max_rank) == 5905


def test_part1():
    input_as_lines = load_data(Path(__file__).parent / "input.txt")
    assert compute_total_winnings_under_given_ordering(input_as_lines, get_hand_rank, cards_to_rank) == 253866470


def test_part1_hands():
    input_as_lines = load_data(Path(__file__).parent / "input.txt")
    hands = sorted([Hand(*line.split(" ")) for line in input_as_lines])
    assert sum(h.bid * i for i, h in enumerate(hands, 1)) == 253866470


def test_part2():
    input_as_lines = load_data(Path(__file__).parent / "input.txt")
    assert compute_total_winnings_under_given_ordering(input_as_lines, get_max_rank, cards_to_max_rank) == 254494947


def test_part2_hands_test_input():
    input_as_lines = test_input
    hands = sorted([Hand(*line.split(" "), use_max_rank=True) for line in input_as_lines])
    assert sum(h.bid * i for i, h in enumerate(hands, 1)) == 5905


def test_part2_hands():
    input_as_lines = load_data(Path(__file__).parent / "input.txt")
    hands = sorted([Hand(*line.split(" "), use_max_rank=True) for line in input_as_lines])
    assert sum(h.bid * i for i, h in enumerate(hands, 1)) == 254494947
