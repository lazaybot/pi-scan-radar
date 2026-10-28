from __future__ import annotations

from time import monotonic, sleep

from .models import ScanSample


class PiRangeScanner:
    """VL53L1X range sensor and PCA9685-controlled servo.

    Hardware modules are imported only here so simulation works on any computer.
    """

    def __init__(self, channel: int = 0, min_pulse: int = 500, max_pulse: int = 2500) -> None:
        try:
            import board
            import busio
            import adafruit_vl53l1x
            from adafruit_motor import servo
            from adafruit_pca9685 import PCA9685
        except ImportError as exc:
            raise RuntimeError(
                "Hardware libraries are missing. Install with: pip install -e '.[hardware]'"
            ) from exc

        i2c = busio.I2C(board.SCL, board.SDA)
        self._sensor = adafruit_vl53l1x.VL53L1X(i2c)
        self._sensor.distance_mode = 2
        self._sensor.timing_budget = 100
        self._sensor.start_ranging()
        self._pca = PCA9685(i2c)
        self._pca.frequency = 50
        self._servo = servo.Servo(
            self._pca.channels[channel], min_pulse=min_pulse, max_pulse=max_pulse
        )

    def read(self, angle_deg: float, settle_s: float = 0.08) -> ScanSample:
        servo_angle = max(0.0, min(180.0, angle_deg + 90.0))
        self._servo.angle = servo_angle
        sleep(settle_s)
        if not self._sensor.data_ready:
            return ScanSample(angle_deg, None, monotonic(), False)
        distance_cm = self._sensor.distance
        self._sensor.clear_interrupt()
        valid = distance_cm is not None and distance_cm > 0
        return ScanSample(angle_deg, distance_cm / 100.0 if valid else None, monotonic(), valid)

    def close(self) -> None:
        self._sensor.stop_ranging()
        self._pca.deinit()
