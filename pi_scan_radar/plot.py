from __future__ import annotations

import argparse
from math import radians

from .scanner import sweep_angles
from .simulation import SimulatedSensor


def main() -> None:
    parser = argparse.ArgumentParser(description="Plot one simulated polar scan")
    parser.add_argument("--save", help="save PNG instead of opening a window")
    args = parser.parse_args()
    try:
        import matplotlib.pyplot as plt
    except ImportError as exc:
        raise SystemExit("Install plotting support: pip install -e '.[plot]'") from exc
    sensor = SimulatedSensor()
    samples = [sensor.read(angle) for angle in sweep_angles(-75, 75, 2)]
    valid = [sample for sample in samples if sample.valid and sample.distance_m is not None]
    figure = plt.figure(figsize=(8, 5))
    axis = figure.add_subplot(111, projection="polar")
    axis.set_theta_zero_location("N")
    axis.set_theta_direction(-1)
    axis.set_thetamin(-75)
    axis.set_thetamax(75)
    axis.set_ylim(0, 4)
    axis.scatter([radians(item.angle_deg) for item in valid], [item.distance_m for item in valid], c="#32e875", s=18)
    axis.set_title("Pi Scan Radar — simulated range returns")
    if args.save:
        figure.savefig(args.save, dpi=160, bbox_inches="tight")
    else:
        plt.show()


if __name__ == "__main__":
    main()
