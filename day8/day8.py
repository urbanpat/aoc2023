from pathlib import Path

import numpy as np

from notebooks.aoc2023.utils import load_data


def parse_input(as_lines: list[str]) -> tuple[dict[str, str], dict[str, str]]:
    map_r = {}
    map_l = {}
    for line in as_lines:
        node, lr = line.split(" = ")
        left, right = lr[1:-1].split(", ")
        map_l[node] = left
        map_r[node] = right
    return map_l, map_r


def compute_steps_from_aaa_to_zzz(instructions: str, left_map: dict[str, str], right_map: dict[str, str]) -> int:
    steps = 0
    node = "AAA"
    while node != "ZZZ":
        direction = instructions[steps % len(instructions)]
        node = left_map[node] if direction == "L" else right_map[node]
        steps += 1
    return steps


def compute_steps_from_xxa_to_xxz_brute_force(instructions: str, left_map: dict[str, str], right_map: dict[str, str]) -> int:
    start_nodes = [node for node in left_map if node[2] == "A"]
    end_nodes = [node for node in left_map if node[2] == "Z"]
    steps = 0
    satisfied = []
    while len(satisfied) != len(start_nodes):
        satisfied = []
        for i in range(len(start_nodes)):
            direction = instructions[steps % len(instructions)]
            start_nodes[i] = left_map[start_nodes[i]] if direction == "L" else right_map[start_nodes[i]]
            if start_nodes[i] in end_nodes:
                satisfied.append(start_nodes[i])
        steps += 1
        if steps > 1e7:
            break

    return steps


def compute_steps_from_xxa_to_xxz_trick(instructions: str, left_map: dict[str, str], right_map: dict[str, str]) -> int:
    start_nodes = [node for node in left_map if node[2] == "A"]
    end_nodes = [node for node in left_map if node[2] == "Z"]
    steps = 0
    instructions_length = len(instructions)
    n_start_nodes = len(start_nodes)
    periods = [[] for _ in range(n_start_nodes)]
    while not all(len(per) >= 3 for per in periods):
        for i in range(n_start_nodes):
            direction = instructions[steps % instructions_length]
            start_nodes[i] = left_map[start_nodes[i]] if direction == "L" else right_map[start_nodes[i]]
            if start_nodes[i] in end_nodes:
                periods[i].append(steps)
        steps += 1
    assert all(np.unique(np.diff(per)).size == 1 for per in periods)  # all are cyclic
    return np.lcm.reduce([per[0] + 1 for per in periods])


if __name__ == "__main__":
    input_as_lines = load_data(Path(__file__).parent / "input.txt")
    instructions = input_as_lines[0]
    left_map, right_map = parse_input(input_as_lines[2:])

    steps = compute_steps_from_aaa_to_zzz(instructions, left_map, right_map)
    print(f"part1: {steps}")

    ans2 = compute_steps_from_xxa_to_xxz_trick(instructions, left_map, right_map)
    print(f"part2: {ans2}")
