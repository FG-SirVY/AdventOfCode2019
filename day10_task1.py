###############################################################################
# Day x, Task y                                                               #
###############################################################################

import aoc_util


year = 2019
day = 10
data_str_easy = """.#..#
.....
#####
....#
...##"""

data_str = """......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####"""


data_str_hard = """.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##"""


def is_linear_combination(p1, p2):
    return p1[0] * p2[1] == p2[0] * p1[1]


def get_all_direction_options(max_len):
    direction_options = [(1, 1), (1, -1), (-1, -1), (-1, 1)]
    permutations = []
    for x in range(1, max_len):
        for y in range(0, x):
            pair = (x, y)

            is_already_there = False
            for e in direction_options:
                if is_linear_combination(e, pair):
                    is_already_there = True
                    break

            if not is_already_there:
                direction_options.append(pair)
                if y != 0:
                    permutations.append((x, -y))
                    permutations.append((-y, x))
                    permutations.append((-y, -x))
                    permutations.append((-x, -y))
                
                permutations.append((-x, y))
                permutations.append((y, x))
                permutations.append((y, -x))

    direction_options.extend(permutations)
    return direction_options


def has_asteroid(grid, direction, row, col):
    new_row = row
    new_col = col

    while 1:
        new_row += direction[0]
        new_col += direction[1]

        if new_row < 0 or new_row >= len(grid) or new_col < 0 or new_col >= len(grid[0]):
            return False
        elif grid[new_row][new_col]:
            return True


def asteroid_count_at(grid, direction_options, row, col):
    count = 0

    for direction in direction_options:
        if has_asteroid(grid, direction, row, col):
            count += 1

    return count


def task(data_set: list[str]) -> int:
    grid = []

    for row in data_set:
        row_to_add = []
        for cell in row:
            row_to_add.append(cell == "#")
        
        grid.append(row_to_add)

    
    max_len = max(len(data_set), len(data_set[0]))
    direction_options = get_all_direction_options(max_len)

    max_asteroid_count = 0
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col]:
                asteroid_count = asteroid_count_at(grid, direction_options, row, col)

                if asteroid_count > max_asteroid_count:
                    max_asteroid_count = asteroid_count

    return max_asteroid_count


aoc_util.run_with_data_str(task, data_str_easy)
aoc_util.run_with_data_str(task, data_str)
aoc_util.run_with_data_str(task, data_str_hard)
aoc_util.run_with_data_set(task, year, day)
