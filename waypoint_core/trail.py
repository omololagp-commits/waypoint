"""Trail model for Waypoint — Week 8: abstract base + hierarchy."""

from abc import ABC, abstractmethod
from .distance import Distance


class Trail(ABC):
    """Abstract base class for all trail types."""

    _VALID_DIFFICULTIES = {"easy", "moderate", "hard", "expert"}
    _default_unit = "km"

    def __init__(self, trail_id: int, name: str, distance: Distance,
                 elevation_gain_m: int, difficulty: str):
        self._id = trail_id
        self._name = name
        self._distance = distance
        self._elevation_gain_m = elevation_gain_m
        self.set_difficulty(difficulty)

    # --- read-only properties ---
    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def distance(self) -> Distance:
        return self._distance

    @property
    def elevation_gain_m(self) -> int:
        return self._elevation_gain_m

    @property
    def difficulty(self) -> str:
        return self._difficulty

    # --- state guards ---
    def set_difficulty(self, value: str) -> None:
        value = value.lower().strip()
        if value not in self._VALID_DIFFICULTIES:
            raise ValueError(
                f"Difficulty must be one of {self._VALID_DIFFICULTIES}"
            )
        self._difficulty = value

    # --- class-level default unit ---
    @classmethod
    def set_default_unit(cls, unit: str) -> None:
        if unit not in {"km", "mi"}:
            raise ValueError("Default unit must be 'km' or 'mi'")
        cls._default_unit = unit

    @classmethod
    def get_default_unit(cls) -> str:
        return cls._default_unit

    # --- alternate constructor ---
    @classmethod
    def from_dict(cls, data: dict) -> "Trail":
        """Build a Trail from an API-shaped dict."""
        raw_dist = data.get("distance", {})
        dist = Distance(
            raw_dist.get("magnitude", 0),
            raw_dist.get("unit", cls._default_unit)
        )
        return cls(
            trail_id=data.get("id", 0),
            name=data.get("name", ""),
            distance=dist,
            elevation_gain_m=data.get("elevation_gain_m", 0),
            difficulty=data.get("difficulty", "moderate")
        )

    # --- static validators ---
    @staticmethod
    def is_valid_difficulty(value: str) -> bool:
        return value.lower().strip() in Trail._VALID_DIFFICULTIES

    @staticmethod
    def is_valid_elevation(value: int) -> bool:
        return isinstance(value, int) and value >= 0

    # --- abstract methods (Week 8) ---
    @abstractmethod
    def estimated_time(self) -> float:
        """Return estimated time in hours."""
        ...

    @abstractmethod
    def summary(self) -> str:
        """Return a one-line summary of the trail."""
        ...

    # --- equality by id ---
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Trail):
            return NotImplemented
        return self._id == other._id

    def __hash__(self) -> int:
        return hash(self._id)

    def __str__(self) -> str:
        return f"{self._name} ({self._distance}) — {self._difficulty}"

    def __repr__(self) -> str:
        return (
            f"Trail(id={self._id}, name={self._name!r}, "
            f"distance={self._distance!r}, elevation_gain_m="
            f"{self._elevation_gain_m}, difficulty={self._difficulty!r})"
        )


class DayHike(Trail):
    """A single-day hiking trail."""

    _PACE_KM_H = 3.0  # km per hour

    def __init__(self, trail_id: int, name: str, distance: Distance,
                 elevation_gain_m: int, difficulty: str):
        super().__init__(trail_id, name, distance, elevation_gain_m, difficulty)

    def estimated_time(self) -> float:
        """Estimate: distance / pace + 1 hour per 300m elevation."""
        dist_km = self._distance.convert("km").magnitude
        base = dist_km / self._PACE_KM_H
        elevation_hours = self._elevation_gain_m / 300
        return base + elevation_hours

    def summary(self) -> str:
        return f"DayHike: {self._name}, ~{self.estimated_time():.1f}h"


class BackpackingRoute(Trail):
    """A multi-day backpacking route."""

    _DAILY_DISTANCE_KM = 15.0

    def __init__(self, trail_id: int, name: str, distance: Distance,
                 elevation_gain_m: int, difficulty: str, days: int = None):
        super().__init__(trail_id, name, distance, elevation_gain_m, difficulty)
        self._days = days

    @property
    def days(self) -> int:
        if self._days is not None:
            return self._days
        return max(1, int(self._distance.convert("km").magnitude / self._DAILY_DISTANCE_KM))

    def estimated_time(self) -> float:
        """Return total days (as a proxy for time)."""
        return float(self.days)

    def summary(self) -> str:
        return f"Backpacking: {self._name}, {self.days} day(s)"


class TrailRun(Trail):
    """A trail running route."""

    _PACE_KM_H = 10.0

    def __init__(self, trail_id: int, name: str, distance: Distance,
                 elevation_gain_m: int, difficulty: str):
        super().__init__(trail_id, name, distance, elevation_gain_m, difficulty)

    def estimated_time(self) -> float:
        dist_km = self._distance.convert("km").magnitude
        return dist_km / self._PACE_KM_H

    def summary(self) -> str:
        return f"TrailRun: {self._name}, ~{self.estimated_time():.1f}h"


class GuidedDayHike(DayHike):
    """A guided day hike with a guide name."""

    def __init__(self, trail_id: int, name: str, distance: Distance,
                 elevation_gain_m: int, difficulty: str, guide_name: str = ""):
        super().__init__(trail_id, name, distance, elevation_gain_m, difficulty)
        self._guide_name = guide_name

    @property
    def guide_name(self) -> str:
        return self._guide_name

    def summary(self) -> str:
        base = super().summary()
        return f"{base} | Guide: {self._guide_name}"