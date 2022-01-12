###############################################################################
# Day x, Task y                                                               #
###############################################################################

import aoc_util, math


year = 2019
day = 10
data_str_easy = """.#....#####...#..
##...##.#####..##
##...#...#.#####.
..#.....#...###..
..#.#.....#....##"""


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


def next_direction(direction_options, original_len, index):
    if index < len(direction_options):
        return direction_options[index]
    elif index < 2 * original_len - 1:
        direction = direction_options[2 * original_len - index - 2]
        return (direction[1], direction[0])
    elif index < 3 * original_len - 2:
        direction = direction_options[index - 2 * original_len + 2]
        return (direction[1], -direction[0])
    elif index < 4 * original_len - 3:
        direction = direction_options[4 *  original_len - index - 4]
        return (direction[0], -direction[1])
    elif index < 5 * original_len - 4:
        direction = direction_options[index - 4 * original_len + 4]
        return (-direction[0], -direction[1])
    elif index < 6 * original_len - 5:
        direction = direction_options[6 * original_len - index - 6]
        return (-direction[1], -direction[0])
    elif index < 7 * original_len - 6:
        direction = direction_options[index - 6 * original_len + 6]
        return (-direction[1], direction[0])
    else:
        direction = direction_options[8 * original_len - index - 8]
        return (-direction[0], direction[1])


def get_all_direction_options(max_len):
    direction_options = [(1, 1)]
    for y in range(1, max_len):
        for x in range(0, y):
            pair = (x, y)

            is_already_there = False
            for e in direction_options:
                if is_linear_combination(e, pair):
                    is_already_there = True
                    break

            if not is_already_there:
                direction_options.append(pair)

    def cmp_angles(a):
        return math.atan(a[0] / a[1])

    direction_options.sort(key=cmp_angles)
    original_len = len(direction_options)
    for i in range(original_len, 8 * original_len - 8):
        direction_options.append(next_direction(direction_options, original_len, i))
    return direction_options


def has_asteroid(grid, direction, row, col):
    new_row = row
    new_col = col

    while 1:
        new_row -= direction[1]
        new_col += direction[0]

        if new_row < 0 or new_row >= len(grid) or new_col < 0 or new_col >= len(grid[0]):
            return None
        elif grid[new_row][new_col]:
            return (new_row, new_col)


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

    pos_row = 13
    pos_col = 11

    max_asteroid_count = 0
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col]:
                asteroid_count = asteroid_count_at(grid, direction_options, row, col)

                if asteroid_count > max_asteroid_count:
                    pos_row = row
                    pos_col = col
                    max_asteroid_count = asteroid_count

    count = 0
    index = 0
    asteroid_pos = None

    while count < 200:
        if index >= len(direction_options):
            index = 0
        direction = direction_options[index]

        asteroid_pos = has_asteroid(grid, direction, pos_row, pos_col)
        if asteroid_pos:
            grid[asteroid_pos[0]][asteroid_pos[1]] = False
            count += 1

        index += 1

    
    return asteroid_pos[0] + asteroid_pos[1] * 100


#aoc_util.run_with_data_str(task, data_str_easy)
aoc_util.run_with_data_str(task, data_str_hard)
aoc_util.run_with_data_set(task, year, day)
