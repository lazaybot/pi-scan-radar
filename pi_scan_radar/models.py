from __future__ import annotations

from dataclasses import dataclass
from math import cos, radians, sin


@dataclass(frozen=True)
class ScanSample:
    angle_deg: float
    distance_m: float | None
    timestamp_s: float
    valid: bool = True

    @property
    def xy_m(self) -> tuple[float, float] | None:
        if not self.valid or self.distance_m is None:
            return None
        angle = radians(self.angle_deg)
        return self.distance_m * sin(angle), self.distance_m * cos(angle)


@dataclass(frozen=True)
class Detection:
    start_angle_deg: float
    end_angle_deg: float
    center_angle_deg: float
    nearest_distance_m: float
    sample_count: int
