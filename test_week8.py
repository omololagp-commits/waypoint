"""Week 8 tests: polymorphism, operators, mixins, MRO."""

from waypoint_core import (
    Distance, Trail, DayHike, BackpackingRoute,
    TrailRun, GuidedDayHike, ElevationMixin, RatingMixin
)


# --- 1. Polymorphic loop over mixed trail types ---
def print_estimates(trails):
    for t in trails:
        print(f"{t.summary()} | estimated time: {t.estimated_time():.1f}")


t1 = DayHike(1, "Eagle Peak", Distance(8, "km"), 450, "moderate")
t2 = BackpackingRoute(2, "Mountain Loop", Distance(45, "km"), 1200, "hard")
t3 = TrailRun(3, "Ridge Sprint", Distance(10, "km"), 200, "moderate")
t4 = GuidedDayHike(4, "Falls Tour", Distance(5, "km"), 100, "easy", "Alice")

print("=== Polymorphic loop ===")
print_estimates([t1, t2, t3, t4])
print()

# --- 2. Distance operator overloading ---
print("=== Distance operators ===")
d1 = Distance(3, "km")
d2 = Distance(2, "km")
print(f"{d1} + {d2} = {d1 + d2}")
print(f"{d1} > {d2} ? {d1 > d2}")

d3 = Distance(2, "mi")
print(f"{d1} + {d3} (mixed units) = {d1 + d3}")

distances = [Distance(5, "km"), Distance(2, "mi"), Distance(3, "km")]
sorted_dist = sorted(distances)
print("Sorted distances:", [str(d) for d in sorted_dist])
print()

# --- 3. FakeTrail — duck-typed, no inheritance ---
class FakeTrail:
    def estimated_time(self):
        return 0.5

    def summary(self):
        return "FakeTrail: test object"


print("=== FakeTrail (duck typing) ===")
fake = FakeTrail()
print_estimates([fake])
print()

# --- 4. Mixins composed into a trail type ---
class RatedDayHike(RatingMixin, ElevationMixin, DayHike):
    pass


print("=== Mixin composition ===")
rated = RatedDayHike(5, "Star Ridge", Distance(6, "km"), 300, "moderate")
rated.add_rating(4.5)
rated.add_rating(5.0)
print(f"Grade: {rated.grade_percent:.1f}%")
print(f"Avg rating: {rated.average_rating:.1f} stars")
print(f"MRO: {[c.__name__ for c in RatedDayHike.__mro__]}")
print()

# --- 5. Instantiating Trail directly should fail ---
print("=== Abstract base check ===")
try:
    Trail(99, "Bad", Distance(1, "km"), 0, "easy")
except TypeError as e:
    print(f"TypeError (expected): {e}")