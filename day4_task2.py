###############################################################################
# Day x, Task y                                                               #
###############################################################################

import aoc_util


year = 2019
day = 4


def task(data_set: list[str]) -> int:
    min_val, max_val = data_set[0].split("-")

    work_val = [int(x) for x in min_val]
    max_val = [int(x) for x in max_val]

    count = 0

    for i in range(1, len(work_val)):
        work_val[i] = max(work_val[i - 1], work_val[i])

    while 1:        
        is_lower = False
        has_double = False
        for i in range(len(work_val)):
            if work_val[i] < max_val[i]:
                is_lower = True
            elif not is_lower and work_val[i] > max_val[i]:
                return count
            
            if i > 0 and work_val[i - 1] == work_val[i] \
                and (i == 1 or work_val[i - 2] != work_val[i]) \
                and (i == len(work_val) - 1 or work_val[i] != work_val[i + 1]):
                has_double = True

        if has_double:
            count += 1


        i = len(work_val) - 1
        while work_val[i] == 9:
            work_val[i] = 0
            i -= 1

        work_val[i] += 1

        for j in range(i + 1, len(work_val)):
            work_val[j] = max(work_val[j - 1], work_val[j])


aoc_util.run_with_data_set(task, year, day)
