"""Itinerary composition for Waypoint."""

from .trail import Trail
from .distance import Distance


class Itinerary:
    """An ordered collection of trails."""

    def __init__(self, name: str = ""):
        self._name = name
        self._trails: list[Trail] = []

    @property
    def name(self) -> str:
        return self._name

    def add_trail(self, trail: Trail) -> None:
        """Add a trail to this itinerary."""
        if not isinstance(trail, Trail):
            raise TypeError("Only Trail instances can be added")
        self._trails.append(trail)

    def total_distance(self, unit: str = "km") -> Distance:
        """Sum distances of all trails, returned in the requested unit."""
        total = 0.0
        for trail in self._trails:
            d = trail.distance.convert(unit)
            total += d.magnitude
        return Distance(total, unit)

    def __len__(self) -> int:
        return len(self._trails)

    def __iter__(self):
        return iter(self._trails)

    def __repr__(self) -> str:
        return f"Itinerary(name={self._name!r}, trails={self._trails!r})"