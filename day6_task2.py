###############################################################################
# Day x, Task y                                                               #
###############################################################################

import aoc_util


year = 2019
day = 6
data_str = """COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
K)YOU
I)SAN"""


def create_list(orbit_map, start):
    ret = []

    while 1:
        start = orbit_map[start]
        ret.append(start)

        if start == "COM":
            return ret



def task(data_set: list[str]) -> int:
    orbit_map = {}

    for l in data_set:
        [source, target] = l.split(")")
        orbit_map[target] = source

    lst_me = create_list(orbit_map, "YOU")
    lst_santa = create_list(orbit_map, "SAN")

    i = len(lst_me) - 1
    j = len(lst_santa) - 1

    while lst_me[i] == lst_santa[j]:
        i -= 1
        j -= 1

    return i + j + 2


aoc_util.run_with_data_str(task, data_str)
aoc_util.run_with_data_set(task, year, day)
