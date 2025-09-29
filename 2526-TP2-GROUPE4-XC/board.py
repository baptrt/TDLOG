from __future__ import annotations

import dataclasses
import enum

"""
This module contains the classes used to represent a board, which is
essentially a labelled graph:

- vertices are stations, labelled with number and kinds;
- edges are transportation links / connections, labelled with modes of
  transportation.
"""


class StationKind(enum.Enum):
    """
    The possible station kinds (used for display, and thus excluding ferries).
    """

    BUS = "bus"
    TAXI = "taxi"
    UNDERGROUND = "underground"


class ConnectionMode(enum.Enum):
    """
    The possible transportation modes, for connections between stations.
    """

    BUS = "bus"
    TAXI = "taxi"
    UNDERGROUND = "underground"
    FERRY = "ferry"


def _mode_of_kind(kind: StationKind) -> ConnectionMode:
    """
    Converts the passed kind into the corresponding connection mode.
    """
    match kind:
        case StationKind.BUS:
            return ConnectionMode.BUS
        case StationKind.TAXI:
            return ConnectionMode.TAXI
        case StationKind.UNDERGROUND:
            return ConnectionMode.UNDERGROUND


@dataclasses.dataclass(frozen=True)
class Connection:
    """
    A connection (to another station) is represented by both the destination
    station and the transportation mode.
    """

    destination: Station
    mode: ConnectionMode


# Type synonym, used for better readability
StationNumber = int


@dataclasses.dataclass(frozen=True)
class Station:
    """
    A station is defined by its name, its kinds (for display), and the
    connections to other stations.
    """

    number: StationNumber
    kinds: frozenset[StationKind]
    connections: list[Connection]

    def __post_init__(self) -> None:
        assert self.number > 0, f"invalid station number ({self.number})"
        assert self.kinds, "empty kinds"


class InvalidBoard(Exception):
    """
    The exception raised when board data is invalid.
    """

    def __init__(self, message: str) -> None:
        super().__init__()
        self._message = message

    @property
    def message(self) -> str:
        return self._message

    def __str__(self) -> str:
        return f"invalid board: {self._message}"


class Board:
    """
    The class for boards, holding a dictionary from station numbers to their
    definitions (See class `Station` above).
    """

    def __init__(
        self,
        stations: list[tuple[StationNumber, list[StationKind]]],
        connections: list[tuple[StationNumber, StationNumber, ConnectionMode]],
    ) -> None:
        """
        Builds a board from stations and connections definitions, following
        the encoding described in `board_data`.
        """
        self._stations: dict[StationNumber, Station] = {}
        if not (stations):
            raise InvalidBoard("no stations")
        for station_number, station_kinds in stations:
            if station_number < 0:
                raise InvalidBoard(f"invalid station number ({station_number})")
            if station_number in self._stations:
                raise InvalidBoard(f"duplicate station ({station_number})")
            station_kinds_as_set = frozenset(station_kinds)
            if len(station_kinds_as_set) < len(station_kinds):
                duplicate_kinds = station_kinds[:]
                for kind in station_kinds_as_set:
                    duplicate_kinds.remove(kind)
                duplicate_kinds_strings = map(lambda k: k.value, duplicate_kinds)
                raise InvalidBoard(f"duplicate kinds ({set(duplicate_kinds_strings)})")
            station = Station(
                number=station_number, kinds=station_kinds_as_set, connections=[]
            )
            self._stations[station_number] = station
        actual_stations = self._stations.keys()
        expected_stations = set(range(1, len(self._stations) + 1))
        missing_stations = expected_stations - actual_stations
        if missing_stations:
            raise InvalidBoard(f"missing stations ({sorted(missing_stations)})")
        # note: we cannot have "extra" stations without missing ones, since we
        # are building the set of expected stations from the number of actual
        # stations
        for source_number, destination_number, mode in connections:
            if source_number not in self._stations:
                raise InvalidBoard(f"unknown station ({source_number})")
            source_station = self._stations[source_number]
            if destination_number not in self._stations:
                raise InvalidBoard(f"unknown station ({destination_number})")
            destination_station = self._stations[destination_number]
            source_station.connections.append(
                Connection(destination=destination_station, mode=mode)
            )
            destination_station.connections.append(
                Connection(destination=source_station, mode=mode)
            )
        self._check_kinds_connections_consistency()
        self._check_connected()

    def _check_kinds_connections_consistency(self) -> None:
        for station in self._stations.values():
            connection_modes = {
                conn.mode
                for conn in station.connections
                if conn.mode is not ConnectionMode.FERRY
            }
            connection_kinds = {_mode_of_kind(kind) for kind in station.kinds}
            if connection_modes != connection_kinds:
                raise InvalidBoard(
                    f"kinds and connections are not consistent ({station.number})"
                )

    def _check_connected(self) -> None:
        seen: set[StationNumber] = set()
        start: StationNumber = next(iter(self._stations))
        stack: list[StationNumber] = [start]
        while stack:
            station_number = stack.pop()
            seen.add(station_number)
            for connection in self._stations[station_number].connections:
                destination_number = connection.destination.number
                if destination_number not in stack and destination_number not in seen:
                    stack.append(destination_number)
        if len(seen) != len(self._stations):
            raise InvalidBoard("network is not connected")

    def __len__(self) -> int:
        return len(self._stations)

    def __contains__(self, key: StationNumber) -> bool:
        return key in self._stations

    def __getitem__(self, key: StationNumber) -> Station:
        if key in self._stations:
            return self._stations[key]
        else:
            raise IndexError(f"invalid station number ({key})")
