from __future__ import annotations

from collections.abc import Iterable

from .models import Detection, ScanSample


def sweep_angles(min_angle: int, max_angle: int, step: int, reverse: bool = False) -> list[int]:
    if step <= 0:
        raise ValueError("step must be positive")
    if min_angle >= max_angle:
        raise ValueError("min_angle must be less than max_angle")
    angles = list(range(min_angle, max_angle + 1, step))
    if angles[-1] != max_angle:
        angles.append(max_angle)
    return list(reversed(angles)) if reverse else angles


def median_filter(samples: list[ScanSample], radius: int = 1) -> list[ScanSample]:
    if radius < 0:
        raise ValueError("radius cannot be negative")
    filtered: list[ScanSample] = []
    for index, sample in enumerate(samples):
        window = samples[max(0, index - radius) : index + radius + 1]
        values = sorted(
            item.distance_m for item in window if item.valid and item.distance_m is not None
        )
        distance = values[len(values) // 2] if values else None
        filtered.append(
            ScanSample(sample.angle_deg, distance, sample.timestamp_s, distance is not None)
        )
    return filtered


def cluster_detections(
    samples: Iterable[ScanSample],
    threshold_m: float,
    max_gap_deg: float = 6.0,
) -> list[Detection]:
    """Group adjacent in-range returns into simple angular detections."""
    in_range = [
        item
        for item in sorted(samples, key=lambda value: value.angle_deg)
        if item.valid and item.distance_m is not None and item.distance_m <= threshold_m
    ]
    if not in_range:
        return []
    groups: list[list[ScanSample]] = [[in_range[0]]]
    for item in in_range[1:]:
        if item.angle_deg - groups[-1][-1].angle_deg <= max_gap_deg:
            groups[-1].append(item)
        else:
            groups.append([item])
    return [
        Detection(
            group[0].angle_deg,
            group[-1].angle_deg,
            sum(item.angle_deg for item in group) / len(group),
            min(item.distance_m for item in group if item.distance_m is not None),
            len(group),
        )
        for group in groups
    ]
