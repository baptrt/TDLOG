import board
import board_data
import player
import random
import rules

from observer import SubjectClass, EnglishObserverClass, FrenchObserverClass

"""
This module is the entry point of the application, defining the `Game` class,
which combines all elements to represent Scotland Yard games.
"""

class Game:
    """
    Main class of the application, taking a list of detectives with their
    names, as well as the name for Mister X. Detective colors must be unique.
    """

    def __init__(
        self, detectives: list[tuple[player.Color, str]], mister_x_name: str
    ) -> None:
        self._board = board.Board(
            stations=board_data.STATIONS, connections=board_data.CONNECTIONS
        )
        self._supply_pile = player.Tickets(
            bus=rules.TOTAL_BUS_TICKETS,
            taxi=rules.TOTAL_TAXI_TICKETS,
            underground=rules.TOTAL_UNDERGROUND_TICKETS,
        )
        self._detectives: list[player.Detective] = []
        remaining_positions = rules.DETECTIVES_STARTING_POSITIONS[:]
        seen_colors: set[player.Color] = set()
        for detective_color, detective_name in detectives:
            assert detective_color not in seen_colors, "duplicate color"
            seen_colors.add(detective_color)
            detective_tickets = Game._create_tickets_for_detective()
            detective_position = random.choice(remaining_positions)
            remaining_positions.remove(detective_position)
            detective = player.Detective(
                name=detective_name,
                color=detective_color,
                tickets=detective_tickets,
                position=detective_position,
            )
            self._supply_pile.bus -= detective_tickets.bus
            self._supply_pile.taxi -= detective_tickets.taxi
            self._supply_pile.underground -= detective_tickets.underground
            self._detectives.append(detective)
        mister_x_position = random.choice(rules.MISTER_X_STARTING_POSITIONS)
        self._mister_x = player.MisterX(
            name=mister_x_name,
            position=mister_x_position,
            black_tickets=rules.MISTER_X_BLACK_TICKETS,
            double_move_tickets=rules.MISTER_X_DOUBLE_MOVE_TICKETS,
        )
        self._round = 0

    @property
    def detectives(self) -> list[player.Detective]:
        return self._detectives

    @property
    def mister_x(self) -> player.MisterX:
        return self._mister_x

    @staticmethod
    def _create_tickets_for_detective() -> player.Tickets:
        """
        Build an initial `Tickets` instance for a detective.
        """
        return player.Tickets(
            bus=rules.DETECTIVES_BUS_TICKETS,
            taxi=rules.DETECTIVES_TAXI_TICKETS,
            underground=rules.DETECTIVES_UNDERGROUND_TICKETS,
        )
