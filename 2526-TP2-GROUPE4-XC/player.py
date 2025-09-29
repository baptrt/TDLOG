import abc
import board
import enum
import dataclasses

"""
This module defines the different kinds of players.
"""


class Color(enum.Enum):
    """
    The possible colors for a player.
    """

    BLACK = "black"
    BLUE = "blue"
    GREEN = "green"
    ORANGE = "orange"
    PURPLE = "purple"
    RED = "red"


@dataclasses.dataclass
class Tickets:
    """
    The tickets (bus, taxi, and underground) a player can use.
    """

    bus: int
    taxi: int
    underground: int

    def __post_init__(self) -> None:
        assert self.bus >= 0, f"invalid bus ({self.bus})"
        assert self.taxi >= 0, f"invalid taxi ({self.taxi})"
        assert self.underground >= 0, f"invalid underground ({self.underground})"


class Player(abc.ABC):
    """
    The parent class for all players.

    A player is defined by its name, color, and position on the board.
    Name and color are immutable, but position is mutable.
    """

    def __init__(self, name: str, color: Color, position: board.StationNumber) -> None:
        super().__init__()
        assert name != "", "empty name"
        self._name = name
        self._color = color
        self._position = position

    @property
    def name(self) -> str:
        return self._name

    @property
    def color(self) -> Color:
        return self._color

    @property
    def position(self) -> board.StationNumber:
        return self._position

    @position.setter
    def position(self, position: board.StationNumber) -> None:
        self._position = position


class Detective(Player):
    """
    The class of detective players: color is restricted (cannot be black,
    reserved for Mister X), and instances also hold tickets information.
    """

    def __init__(
        self, name: str, color: Color, position: board.StationNumber, tickets: Tickets
    ) -> None:
        super().__init__(name, color, position)
        assert color != Color.BLACK, "black is not a detective color"
        self._tickets = tickets

    @property
    def tickets(self) -> Tickets:
        return self._tickets


class MisterX(Player):
    """
    The class of Mister X: color is implicitly set to black, and additional
    attributes for black tickets and double move tickets (both mutable) are
    defined.
    """

    def __init__(
        self,
        name: str,
        position: board.StationNumber,
        black_tickets: int,
        double_move_tickets: int,
    ) -> None:
        super().__init__(name, Color.BLACK, position)
        assert black_tickets >= 0, f"invalid black tickets ({black_tickets})"
        assert (
            double_move_tickets >= 0
        ), f"invalid double tickets ({double_move_tickets})"
        self._black_tickets = black_tickets
        self._double_move_tickets = double_move_tickets

    @property
    def black_tickets(self) -> int:
        return self._black_tickets

    @black_tickets.setter
    def black_tickets(self, black_tickets: int) -> None:
        assert black_tickets >= 0, f"invalid black tickets ({black_tickets})"
        self._black_tickets = black_tickets

    @property
    def double_move_tickets(self) -> int:
        return self._double_move_tickets

    @double_move_tickets.setter
    def double_move_tickets(self, double_move_tickets: int) -> None:
        assert (
            double_move_tickets >= 0
        ), f"invalid double tickets ({double_move_tickets})"
        self._double_move_tickets = double_move_tickets
