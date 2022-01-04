###############################################################################
# Day x, Task y                                                               #
###############################################################################

import aoc_util


year = 2019
day = 2
data_str = """1,1,1,4,99,5,6,0,99"""


def task(data_set: list[str]) -> int:
    fresh_program = [int(x) for x in data_set[0].split(",")]

    instruction_ptr = 0

    for i in range(100):
        for j in range(100):
            program = fresh_program.copy()
            instruction_ptr = 0
            program[1] = i
            program[2] = j

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

            if program[0] == 19690720:
                return 100 * i + j


#aoc_util.run_with_data_str(task, data_str)
aoc_util.run_with_data_set(task, year, day)
