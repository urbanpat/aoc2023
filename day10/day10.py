from pathlib import Path

import cv2
import numpy as np

from notebooks.aoc2023.utils import load_data

PIPE_TYPES = ["|", "-", "F", "L", "J", "7"]


def get_right_possibilities(pipe_masks: dict[str, np.ndarray], start_mask: np.ndarray) -> np.ndarray:
    right_of_me_viable_options = pipe_masks["-"] | pipe_masks["J"] | pipe_masks["7"] | start_mask
    right_of_me_viable_options[:, 0] = False  # cannot enter leftmost column
    right_of_me_viable_options = np.roll(right_of_me_viable_options, -1)
    my_viable_right_pointing_options = pipe_masks["-"] | pipe_masks["L"] | pipe_masks["F"] | start_mask
    return my_viable_right_pointing_options & right_of_me_viable_options


def get_left_possibilities(pipe_masks: dict[str, np.ndarray], start_mask: np.ndarray) -> np.ndarray:
    left_of_me_viable_options = pipe_masks["-"] | pipe_masks["L"] | pipe_masks["F"] | start_mask
    left_of_me_viable_options[:, -1] = False  # cannot enter rightmost column
    left_of_me_viable_options = np.roll(left_of_me_viable_options, 1)
    my_viable_left_pointing_options = pipe_masks["-"] | pipe_masks["J"] | pipe_masks["7"] | start_mask
    return my_viable_left_pointing_options & left_of_me_viable_options


def get_top_possibilities(pipe_masks: dict[str, np.ndarray], start_mask: np.ndarray) -> np.ndarray:
    top_of_me_viable_options = pipe_masks["|"] | pipe_masks["7"] | pipe_masks["F"] | start_mask
    top_of_me_viable_options[-1, :] = False  # cannot enter bottommost column
    top_of_me_viable_options = np.roll(top_of_me_viable_options, 1, axis=0)
    my_viable_top_pointing_options = pipe_masks["|"] | pipe_masks["J"] | pipe_masks["L"] | start_mask
    return my_viable_top_pointing_options & top_of_me_viable_options


def get_bottom_possibilities(pipe_masks: dict[str, np.ndarray], start_mask: np.ndarray) -> np.ndarray:
    bottom_of_me_viable_options = pipe_masks["|"] | pipe_masks["J"] | pipe_masks["L"] | start_mask
    bottom_of_me_viable_options[0, :] = False  # cannot enter bottommost column
    bottom_of_me_viable_options = np.roll(bottom_of_me_viable_options, -1, axis=0)
    my_viable_bottom_pointing_options = pipe_masks["|"] | pipe_masks["7"] | pipe_masks["F"] | start_mask
    return my_viable_bottom_pointing_options & bottom_of_me_viable_options


def create_direction_maps(maze_map: np.ndarray) -> dict[tuple[int, int], np.ndarray]:
    pipe_masks = {pipe_type: maze_map == pipe_type for pipe_type in PIPE_TYPES}
    start_mask = maze_map == "S"
    can_go_right = get_right_possibilities(pipe_masks, start_mask)
    can_go_left = get_left_possibilities(pipe_masks, start_mask)
    can_go_top = get_top_possibilities(pipe_masks, start_mask)
    can_go_bottom = get_bottom_possibilities(pipe_masks, start_mask)
    return {(0, 1): can_go_right, (0, -1): can_go_left, (-1, 0): can_go_top, (1, 0): can_go_bottom}


def where_can_i_go_next(my_position: tuple[int, int], direction_maps: dict[tuple[int, int], np.ndarray]) -> list[tuple[int, int]]:
    # 4 binary masks saying, what direction os possible -> (+-1, +-1)
    return [direction for direction, dir_map in direction_maps.items() if dir_map[*my_position]]


def find_loop_mask(maze_map: np.ndarray):
    direction_maps = create_direction_maps(maze_map)
    start_position = np.where(maze_map == "S")
    loop_found = False
    y, x = start_position
    maze_mask = np.zeros_like(maze_map, dtype=bool)
    maze_mask[y, x] = True
    start_directions = where_can_i_go_next((y, x), direction_maps)
    while not loop_found:
        start_direction = start_directions.pop()
        # at least two possible directions to go to from start
        y += start_direction[0]
        x += start_direction[1]
        maze_mask[y, x] = True
        # find
        while True:
            if not (directions := where_can_i_go_next((y, x), direction_maps)):
                # dead end
                break
            else:
                assert len(directions) == 2
                can_go_somewhere = False
                for direction in directions:
                    y_var = y + direction[0]
                    x_var = x + direction[1]
                    if maze_mask[y_var, x_var]:
                        # been here
                        pass
                    else:
                        # print(f"can go {direction}")
                        can_go_somewhere = True
                        y += direction[0]
                        x += direction[1]
                        break
                if not can_go_somewhere:
                    loop_found = True
                    break
                maze_mask[y, x] = True
    return maze_mask


def compute_vertical_crossings(way_out: np.ndarray) -> int:
    start_pieces = ["L", "J"]
    start_of_crossing_pattern = {"7": "L", "F": "J"}
    end_pieces = ["7", "F"]

    crosses = 0
    way_out_as_list = list(way_out)
    while way_out_as_list:
        piece = way_out_as_list.pop()
        if piece == "-":
            crosses += 1
        elif piece in start_pieces:
            start_of_segment = piece
            end_of_crossing = False
            while (not end_of_crossing) and way_out_as_list:
                piece = way_out_as_list.pop()
                if piece in end_pieces:
                    # second bend found
                    if start_of_crossing_pattern.get(piece) == start_of_segment:
                        crosses += 1
                    else:
                        end_of_crossing = True
                elif piece == "|":
                    # continuation
                    pass
                elif piece == "-":
                    end_of_crossing = True
                elif piece in start_pieces:
                    start_of_segment = piece
                else:
                    end_of_crossing = True
                    print(piece)
        elif piece in end_pieces:
            # not interesting
            pass
        elif piece == "|":
            # not interesting
            pass
        else:
            # todo: if "S" was "-" or was a continuation of a cross-segment, this would make my result wrong, however, "S" = "J" and right on top of it is "7"
            print(piece)
            pass

    return crosses


def inside_area(area_mask: np.ndarray, loop_mask: np.ndarray, maze_map: np.ndarray) -> int:
    area_representative = np.where(area_mask)
    repre_y = area_representative[0][0]
    repre_x = area_representative[1][0]

    if area_mask[:, 0].any() or area_mask[:, -1].any() or area_mask[0, :].any() or area_mask[-1, :].any():
        # we are border pieces are outside
        return 0
    n_crossings_top = compute_vertical_crossings(maze_map[:repre_y, repre_x][loop_mask[:repre_y, repre_x]])
    if n_crossings_top % 2:
        return area_mask.sum()
    else:
        return 0


def compute_inner_area(input_as_arr, loop_mask) -> int:
    _, area_labels, _, _ = cv2.connectedComponentsWithStats((~loop_mask).astype(np.uint8), connectivity=4)

    inner_area = 0
    glob_mask = np.zeros_like(input_as_arr, dtype=bool)
    for label in range(1, area_labels.max() + 1):
        area_mask = area_labels == label
        ar = inside_area(area_mask, loop_mask, input_as_arr)
        if ar > 0:
            glob_mask |= area_mask
        inner_area += ar
    return inner_area


if __name__ == "__main__":
    fix_input_manually = True
    input_as_lines = load_data(Path(__file__).parent / "input.txt")

    input_as_arr = np.array([list(l) for l in input_as_lines])
    loop_mask = find_loop_mask(input_as_arr)
    farthest_point = round(loop_mask.sum() / 2)
    print(f"part1: {farthest_point}")

    if fix_input_manually:
        # does not change the result
        input_as_arr[input_as_arr == "S"] = "J"

    inner_area = compute_inner_area(input_as_arr, loop_mask)
    print(f"part2: {inner_area}")
