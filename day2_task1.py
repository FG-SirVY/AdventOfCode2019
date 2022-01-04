###############################################################################
# Day x, Task y                                                               #
###############################################################################

import aoc_util


year = 2019
day = 2
data_str = """1,1,1,4,99,5,6,0,99"""


def task(data_set: list[str]) -> int:
    program = [int(x) for x in data_set[0].split(",")]

    instruction_ptr = 0

    program[1] = 12
    program[2] = 2

    while program[instruction_ptr] != 99:
        if program[instruction_ptr] == 1:
            program[program[instruction_ptr + 3]] = \
            program[program[instruction_ptr + 1]] \
            + program[program[instruction_ptr + 2]]

            instruction_ptr += 4
        elif program[instruction_ptr] == 2:
            program[program[instruction_ptr + 3]] = \
            program[program[instruction_ptr + 1]] \
            * program[program[instruction_ptr + 2]]

            instruction_ptr += 4

    return program[0]


#aoc_util.run_with_data_str(task, data_str)
aoc_util.run_with_data_set(task, year, day)
