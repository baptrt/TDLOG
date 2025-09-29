import board

"""
This module defines symbolic constants related to the rules, such as the
possible starting positions, or the maximum number of turns.
"""


TOTAL_BUS_TICKETS = 45
TOTAL_TAXI_TICKETS = 57
TOTAL_UNDERGROUND_TICKETS = 23

MAX_ROUND = 23

# fmt: off
DETECTIVES_STARTING_POSITIONS : list[board.StationNumber] = [
     13,
     26,
     29,
     34,
     50,
     53,
     91,
     94,
    103,
    112,
    117,
    123,
    138,
    141,
    155,
    174,
]
# fmt: on

DETECTIVES_BUS_TICKETS = 8
DETECTIVES_TAXI_TICKETS = 11
DETECTIVES_UNDERGROUND_TICKETS = 4

# fmt: off
MISTER_X_STARTING_POSITIONS : list[board.StationNumber] = [
     35,
     45,
     51,
     71,
     78,
    104,
    106,
    127,
    132,
    146,
    166,
    170,
    172,
]
# fmt: on

MISTER_X_BLACK_TICKETS = 5
MISTER_X_DOUBLE_MOVE_TICKETS = 3
