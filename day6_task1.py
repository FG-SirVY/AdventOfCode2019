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
K)L"""


def num_orbits(orbit_map, point, n):
    n += 1
    next = orbit_map.get(point, [])
    
    ret = n
    for t in next:
        ret += num_orbits(orbit_map, t, n)

    return ret


def task(data_set: list[str]) -> int:
    orbit_map = {}

    for l in data_set:
        [source, target] = l.split(")")
        orbit_map.setdefault(source, []).append(target)

    return num_orbits(orbit_map, "COM", -1)


aoc_util.run_with_data_str(task, data_str)
aoc_util.run_with_data_set(task, year, day)
