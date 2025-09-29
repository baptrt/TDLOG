import board
import dataclasses

"""
This module defines the different kinds of moves, for the different kinds of
players.
"""


@dataclasses.dataclass
class SimpleMove:
    """
    A simple move is a move between two positions (source and destination) on
    the board. The mode of transportation is also recorded, as a move between
    two given positions could use different modes, which would have an impact
    on the ticket to use.
    """

    source: board.Station
    destination: board.Station
    mode: board.ConnectionMode


@dataclasses.dataclass
class BlackTicketMove:
    """
    A black-ticket move is akin to a simple move, but can use any mode of
    transportation, which is hence not recorded. As a result, the class has
    only two attributes for source and destination positions.
    """

    source: board.Station
    destination: board.Station


@dataclasses.dataclass
class DoubleTicketMove:
    """
    A double-ticket move is simply the succession of two moves.
    """

    first_move: SimpleMove | BlackTicketMove
    second_move: SimpleMove | BlackTicketMove


# A detective move is a simple move. This is a mere type synonym, used for
# better readability.
DetectiveMove = SimpleMove

# A Mister X move is any of the moves above. This is a type disjunction
# of the dataclasses above.
MisterXMove = SimpleMove | BlackTicketMove | DoubleTicketMove
