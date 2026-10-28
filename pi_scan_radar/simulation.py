from __future__ import annotations

from dataclasses import dataclass
from math import cos, radians, sin, sqrt
from random import Random
from time import monotonic

from .models import ScanSample


@dataclass(frozen=True)
class CircleObstacle:
    x_m: float
    y_m: float
    radius_m: float


DEFAULT_SCENE = (
    CircleObstacle(-0.65, 1.35, 0.22),
    CircleObstacle(0.35, 0.85, 0.16),
    CircleObstacle(0.90, 1.75, 0.30),
)


def ray_circle_distance(angle_deg: float, obstacle: CircleObstacle) -> float | None:
    """Return the nearest positive intersection of a ray and circle."""
    angle = radians(angle_deg)
    dx, dy = sin(angle), cos(angle)
    projection = obstacle.x_m * dx + obstacle.y_m * dy
    center_sq = obstacle.x_m**2 + obstacle.y_m**2
    discriminant = obstacle.radius_m**2 - (center_sq - projection**2)
    if discriminant < 0:
        return None
    root = sqrt(discriminant)
    candidates = [value for value in (projection - root, projection + root) if value >= 0]
    return min(candidates) if candidates else None


class SimulatedSensor:
    def __init__(
        self,
        obstacles: tuple[CircleObstacle, ...] = DEFAULT_SCENE,
        max_range_m: float = 4.0,
        noise_m: float = 0.01,
        seed: int = 7,
    ) -> None:
        self.obstacles = obstacles
        self.max_range_m = max_range_m
        self.noise_m = noise_m
        self.random = Random(seed)

    def read(self, angle_deg: float) -> ScanSample:
        hits = [ray_circle_distance(angle_deg, obstacle) for obstacle in self.obstacles]
        valid_hits = [distance for distance in hits if distance is not None]
        if not valid_hits or min(valid_hits) > self.max_range_m:
            return ScanSample(angle_deg, None, monotonic(), False)
        distance = max(0.0, min(valid_hits) + self.random.gauss(0.0, self.noise_m))
        return ScanSample(angle_deg, distance, monotonic(), True)
