###############################################################################
# Day x, Task y                                                               #
###############################################################################

import aoc_util, sys


year = 2019
day = 3
data_str_easy = """R75,D30,R83,U83,L12,D49,R71,U7,L72
U62,R66,U55,R34,D71,R55,D58,R83"""
data_str = """R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51
U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"""


def move_along(instructions, to_call):
    x, y = 0, 0
    
    for instr in instructions.split(","):
        direction = instr[0]
        length = int(instr[1:])

        while length > 0:
            if direction == "U":
                y += 1
            elif direction == "D":
                y -= 1
            elif direction == "R":
                x += 1
            elif direction == "L":
                x -= 1

            to_call((x, y))
            length -= 1


def task(data_set: list[str]) -> int:
    points_1 = {}
    points_2 = {}

    min_cum_steps = [sys.maxsize]
    steps = [1]

    def add_to_set(point):
        points_1[point] = steps[0]
        steps[0] += 1


    def check_for_intersections(point):
        if point in points_1:
            cum_steps = points_1[point] + steps[0]

            if cum_steps < min_cum_steps[0]:
                min_cum_steps[0] = cum_steps

        steps[0] += 1

    move_along(data_set[0], add_to_set)
    steps[0] = 1
    move_along(data_set[1], check_for_intersections)

    return min_cum_steps[0]


aoc_util.run_with_data_str(task, data_str_easy)
aoc_util.run_with_data_str(task, data_str)
aoc_util.run_with_data_set(task, year, day)
