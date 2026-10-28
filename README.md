# Pi Scan Radar

A portable Raspberry Pi scanning rangefinder that sweeps a laser time-of-flight
sensor, records polar measurements, filters noise, groups nearby returns, and
plots the result. It includes a deterministic simulation, so the full software
and tests run before any hardware is purchased.

## What it is—and is not

This is the familiar hobby-project “radar” display, but the instrument is not
radio radar. It measures reflected infrared light with a VL53L1X sensor. It is
useful for tabletop mapping, doorway monitoring, robotics experiments, and
learning polar sensing. It cannot see through walls, identify people, or safely
guide a vehicle.

## Run without hardware

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev,plot]'
pi-scan-radar --output outputs/scan.csv
pi-scan-radar-plot --save outputs/simulated-scan.png
python -m unittest discover -s tests -v
```

## Run on a Raspberry Pi

After completing [PARTS.md](PARTS.md), [WIRING.md](WIRING.md), and
[ASSEMBLY.md](ASSEMBLY.md):

```bash
sudo raspi-config              # enable Interface Options > I2C, then reboot
python3 -m venv --system-site-packages .venv
source .venv/bin/activate
python -m pip install -e '.[hardware,plot]'
pi-scan-radar --hardware --output outputs/live-scan.csv
```

Start with the servo horn disconnected, confirm that the commanded motion stays
within its mechanical range, then attach the sensor mount at the centered
position. Calibration and acceptance checks are in [CALIBRATION.md](CALIBRATION.md).

## Architecture

```text
VL53L1X ──I2C── Raspberry Pi ── scan/filter/cluster ── CSV + polar plot
                    │
                    └──I2C── PCA9685 ── servo ── rotating sensor
```

The same scanner interface supports simulated and physical measurements.
Hardware-only libraries are imported lazily, keeping development and automated
tests independent of a Raspberry Pi.

## Safety and privacy

- Power the servo from a separate regulated 5 V supply; connect grounds.
- Never feed 5 V into Raspberry Pi GPIO.
- Do not point the moving assembly toward eyes or use it as a security device.
- The sensor reports range only; this project does not capture images or audio.
- Secure the power bank and wiring before carrying the unit.

## Current limitations

The simulation and signal-processing functions are tested. The included default
servo pulse limits and sensor settings are starting points, not proof that every
servo/mount combination is calibrated. Real hardware validation and enclosure
testing remain required. See [ROADMAP.md](ROADMAP.md).

## License

BSD-3-Clause. The project is original and does not redistribute vendor example
repositories. Adafruit hardware libraries retain their own licenses.
