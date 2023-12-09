from pathlib import Path
from typing import Callable

import numpy as np

from notebooks.aoc2023.utils import load_data

CARDS_TO_CHARS = {
    "A": "A",
    "K": "B",
    "Q": "C",
    "J": "D",
    "T": "E",
    "9": "F",
    "8": "G",
    "7": "H",
    "6": "I",
    "5": "J",
    "4": "K",
    "3": "L",
    "2": "M",
}

CARDS_TO_CHARS_PART2 = {
    "A": "A",
    "K": "B",
    "Q": "C",
    "T": "D",
    "9": "E",
    "8": "F",
    "7": "G",
    "6": "H",
    "5": "I",
    "4": "J",
    "3": "K",
    "2": "L",
    "J": "M",
}


def get_hand_rank(hand: str) -> int:  # highest card get lowest rank (is first)
    _, counts = np.unique([*hand], return_counts=True)
    counts[::-1].sort()
    u_uniq = counts.size
    if u_uniq == 1:  # five
        return 1
    elif u_uniq == 2 and max(counts) == 4:  # four
        return 2
    elif u_uniq == 2 and max(counts) == 3:  # full house
        return 3
    elif u_uniq == 3 and max(counts) == 3:  # three
        return 4
    elif u_uniq == 3 and max(counts) == 2:  # two pairs
        return 5
    elif u_uniq == 4 and max(counts) == 2:  # one pair
        return 6
    else:
        return 7  # high card


def get_max_rank(hand: str) -> int:
    val = get_hand_rank(hand)
    if "J" in hand:
        for substitute in CARDS_TO_CHARS_PART2:
            sub_val = get_hand_rank(hand.replace("J", substitute))
            val = sub_val if sub_val < val else val
    return val


class Hand:
    def __init__(self, cards: str, bid: str, use_max_rank: bool = False):
        self.cards = cards
        self.bid = int(bid)
        self.max_rank = get_max_rank(self.cards) if use_max_rank else get_hand_rank(self.cards)

        cards_map = CARDS_TO_CHARS_PART2 if use_max_rank else CARDS_TO_CHARS
        self.card_ranks = tuple([cards_map[card] for card in cards])

    def __gt__(self, other):  # better (greater) card has lower rank number and/or is composed of lower ranking cards (rank 1 is best)
        if self.max_rank < other.max_rank:
            return True
        elif self.max_rank == other.max_rank:
            return self.card_ranks < other.card_ranks

    def __lt__(self, other):
        return not self > other


def cards_to_rank(cards: str) -> str:
    return "".join(CARDS_TO_CHARS[card] for card in cards)


def cards_to_max_rank(cards: str) -> str:
    return "".join(CARDS_TO_CHARS_PART2[card] for card in cards)


def compute_total_winnings_under_given_ordering(
    input_as_lines: list[str], rank_func: Callable[[str], int], card_to_rank_func: Callable[[str], str]
) -> int:
    hands_raw, bids = list(zip(*[line.split(" ") for line in input_as_lines]))
    rank_tuples = [str(rank_func(h)) + card_to_rank_func(h) for h in hands_raw]
    order = np.argsort(rank_tuples)[::-1]
    return (np.array(bids)[order].astype(int) * np.arange(1, order.shape[0] + 1)).sum()


if __name__ == "__main__":
    input_as_lines = load_data(Path(__file__).parent / "input.txt")

    ans1 = compute_total_winnings_under_given_ordering(input_as_lines, get_hand_rank, cards_to_rank)

    hands = sorted([Hand(*line.split(" "), use_max_rank=False) for line in input_as_lines])
    ans1_hands = sum(h.bid * i for i, h in enumerate(hands, 1))

    print(f"part1: {ans1}, {ans1_hands}")

    ans2 = compute_total_winnings_under_given_ordering(input_as_lines, get_max_rank, cards_to_max_rank)

    hands = sorted([Hand(*line.split(" "), use_max_rank=True) for line in input_as_lines])
    ans2_hands = sum(h.bid * i for i, h in enumerate(hands, 1))

    print(f"part2: {ans2}, {ans2_hands}")
