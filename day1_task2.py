###############################################################################
# Day x, Task y                                                               #
###############################################################################

import aoc_util


year = 2019
day = 1
data_str = """100756"""


def task(data_set: list[str]) -> int:
    fuel = 0

    for m in data_set:
        weight = int(m) // 3 - 2
        while weight >= 0:
            fuel += weight
            weight = weight // 3 - 2
        

    return fuel


aoc_util.run_with_data_str(task, data_str)
aoc_util.run_with_data_set(task, year, day)
