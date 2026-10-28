from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from .hardware import PiRangeScanner
from .scanner import cluster_detections, median_filter, sweep_angles
from .simulation import SimulatedSensor


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Portable scanning rangefinder")
    parser.add_argument("--hardware", action="store_true", help="use Pi-connected sensor")
    parser.add_argument("--min-angle", type=int, default=-75)
    parser.add_argument("--max-angle", type=int, default=75)
    parser.add_argument("--step", type=int, default=3)
    parser.add_argument("--threshold", type=float, default=2.5)
    parser.add_argument("--output", type=Path, help="optional CSV output path")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    sensor = PiRangeScanner() if args.hardware else SimulatedSensor()
    try:
        samples = [sensor.read(angle) for angle in sweep_angles(args.min_angle, args.max_angle, args.step)]
        samples = median_filter(samples)
        detections = cluster_detections(samples, args.threshold, max_gap_deg=args.step * 1.5)
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            with args.output.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.writer(handle)
                writer.writerow(("angle_deg", "distance_m", "valid", "timestamp_s"))
                writer.writerows(
                    (sample.angle_deg, sample.distance_m, sample.valid, sample.timestamp_s)
                    for sample in samples
                )
        print(json.dumps({
            "mode": "hardware" if args.hardware else "simulation",
            "samples": len(samples),
            "valid_returns": sum(sample.valid for sample in samples),
            "detections": [detection.__dict__ for detection in detections],
        }, indent=2))
    finally:
        if args.hardware:
            sensor.close()


if __name__ == "__main__":
    main()
