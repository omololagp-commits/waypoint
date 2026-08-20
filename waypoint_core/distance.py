"""Distance value type for Waypoint."""


class Distance:
    """A magnitude with a unit (km or mi). Supports +, -, <, >, ==."""

    _KM_TO_MI = 0.621371
    _VALID_UNITS = {"km", "mi"}

    def __init__(self, magnitude: float, unit: str):
        if magnitude < 0:
            raise ValueError("Distance magnitude cannot be negative")
        if unit not in self._VALID_UNITS:
            raise ValueError(f"Unit must be one of {self._VALID_UNITS}")
        self._magnitude = float(magnitude)
        self._unit = unit

    @property
    def magnitude(self) -> float:
        """Read-only magnitude."""
        return self._magnitude

    @property
    def unit(self) -> str:
        """Read-only unit."""
        return self._unit

    def convert(self, to_unit: str) -> "Distance":
        """Return a new Distance converted to the given unit."""
        if to_unit not in self._VALID_UNITS:
            raise ValueError(f"Unit must be one of {self._VALID_UNITS}")
        if to_unit == self._unit:
            return Distance(self._magnitude, self._unit)

        if self._unit == "km" and to_unit == "mi":
            new_mag = self._magnitude * self._KM_TO_MI
        else:
            new_mag = self._magnitude / self._KM_TO_MI
        return Distance(new_mag, to_unit)

    # --- operator overloading ---
    def _to_common(self, other: "Distance") -> tuple[float, float]:
        """Normalize both distances to km for arithmetic/comparison."""
        return self.convert("km").magnitude, other.convert("km").magnitude

    def __add__(self, other: "Distance") -> "Distance":
        if not isinstance(other, Distance):
            return NotImplemented
        a, b = self._to_common(other)
        return Distance(a + b, "km")

    def __sub__(self, other: "Distance") -> "Distance":
        if not isinstance(other, Distance):
            return NotImplemented
        a, b = self._to_common(other)
        result = a - b
        if result < 0:
            raise ValueError("Subtraction would yield a negative distance")
        return Distance(result, "km")

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Distance):
            return NotImplemented
        a, b = self._to_common(other)
        return abs(a - b) < 1e-9

    def __lt__(self, other: "Distance") -> bool:
        if not isinstance(other, Distance):
            return NotImplemented
        a, b = self._to_common(other)
        return a < b

    def __le__(self, other: "Distance") -> bool:
        return self == other or self < other

    def __gt__(self, other: "Distance") -> bool:
        if not isinstance(other, Distance):
            return NotImplemented
        a, b = self._to_common(other)
        return a > b

    def __ge__(self, other: "Distance") -> bool:
        return self == other or self > other

    def __repr__(self) -> str:
        return f"Distance({self._magnitude}, '{self._unit}')"

    def __str__(self) -> str:
        return f"{self._magnitude} {self._unit}"