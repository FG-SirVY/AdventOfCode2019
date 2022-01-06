###############################################################################
# Day x, Task y                                                               #
###############################################################################

import aoc_util, sys


year = 2019
day = 8
data_str = """123456789012"""


def task(data_set: list[str]) -> int:
    width = 25
    height = 6

    layer_length = width * height
    in_layer = 1

    min_zero_digits = sys.maxsize
    ret = 0

    zero_digits = 0
    one_digits = 0
    two_digits = 0

    for i in data_set[0]:
        if i == "0":
            zero_digits += 1
        elif i == "1":
            one_digits += 1
        elif i == "2":
            two_digits += 1

        if in_layer == layer_length:
            if zero_digits < min_zero_digits:
                min_zero_digits = zero_digits
                ret = one_digits * two_digits

            in_layer = 0
            zero_digits = 0
            one_digits = 0
            two_digits = 0

        in_layer += 1


    return ret




aoc_util.run_with_data_str(task, data_str)
aoc_util.run_with_data_set(task, year, day)
