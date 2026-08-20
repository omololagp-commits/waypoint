"""Mixins for Waypoint trail types."""


class ElevationMixin:
    """Adds grade-percentage calculation."""

    @property
    def grade_percent(self) -> float:
        """Return average grade as a percentage."""
        if not hasattr(self, "_distance") or not hasattr(self, "_elevation_gain_m"):
            raise AttributeError("Trail must have _distance and _elevation_gain_m")
        dist_km = self._distance.convert("km").magnitude
        if dist_km == 0:
            return 0.0
        return (self._elevation_gain_m / (dist_km * 1000)) * 100


class RatingMixin:
    """Adds a simple star-rating system."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._ratings: list[float] = []

    def add_rating(self, stars: float) -> None:
        if not (0 <= stars <= 5):
            raise ValueError("Rating must be between 0 and 5")
        self._ratings.append(stars)

    @property
    def average_rating(self) -> float:
        if not self._ratings:
            return 0.0
        return sum(self._ratings) / len(self._ratings)