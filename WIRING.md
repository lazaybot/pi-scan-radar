# Wiring

Power everything off before changing connections.

## I2C bus

| Raspberry Pi | VL53L1X breakout | PCA9685 |
|---|---|---|
| Pin 1, 3.3 V | VIN only if the breakout explicitly supports 3.3 V | VCC |
| Pin 3, GPIO2/SDA | SDA | SDA |
| Pin 5, GPIO3/SCL | SCL | SCL |
| Pin 6, GND | GND | GND |

Check the exact breakout documentation before selecting VIN. Do not assume all
boards contain identical regulators and level shifters.

## Servo power

| Connection | Destination |
|---|---|
| Regulated 5 V positive | PCA9685 V+ terminal |
| Supply ground | PCA9685 GND and Raspberry Pi GND |
| Servo signal | PCA9685 channel 0 signal |
| Servo red | PCA9685 channel 0 V+ |
| Servo brown/black | PCA9685 channel 0 GND |

Place the bulk capacitor across PCA9685 V+ and GND with correct polarity. Do not
power the servo from the Pi 3.3 V pin. A shared ground is required for the I2C
and PWM references.

## Pre-power checklist

1. Verify there is no continuity between 5 V and 3.3 V rails.
2. Confirm capacitor polarity.
3. Confirm the servo connector orientation.
4. Turn the mechanism by hand and remove cable snags.
5. Power the Pi first without the servo connected and run `i2cdetect -y 1`.
6. Expect the PCA9685 at `0x40`; the VL53L1X normally appears at `0x29`.
