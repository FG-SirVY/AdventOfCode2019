###############################################################################
# Day x, Task y                                                               #
###############################################################################

import aoc_util, sys


year = 2019
day = 8
data_str = """0222112222120000"""


def task(data_set: list[str]) -> int:
    width = 25
    height = 6

    layer_length = width * height

    for i in range(layer_length):
        while data_set[0][i] == "2":
            i += layer_length
            pass

        if i % width == 0:
            print()

        if data_set[0][i] == "0":
            print(" ", end="")
        else:
            print("#", end="")    

    return 0


#aoc_util.run_with_data_str(task, data_str)
aoc_util.run_with_data_set(task, year, day)
