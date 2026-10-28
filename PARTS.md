# Parts list

## Required

| Qty | Part | Recommended specification | Why |
|---:|---|---|---|
| 1 | Raspberry Pi Zero 2 W | headers installed | compact computer and Wi-Fi |
| 1 | microSD card | 16 GB or larger, high endurance preferred | operating system and logs |
| 1 | VL53L1X breakout | 2.8–5 V breakout with I2C level handling | range measurement |
| 1 | PCA9685 servo driver | I2C, separate V+ terminal | stable servo pulses and power isolation |
| 1 | micro servo | metal gear preferred, 180° class | rotates the sensor |
| 1 | regulated 5 V supply | at least 2 A total; servo rail appropriately fused | portable power |
| 1 | 470–1000 µF capacitor | at least 10 V rating | reduces servo-rail voltage dips |
| 1 | sensor bracket and base | printed or hand-built, nonconductive | holds alignment |
| — | jumper wires, screws, standoffs | sized for the selected boards | assembly |

## Useful extras

- Small power switch and inline fuse
- USB power meter for diagnosing brownouts
- Short flexible ribbon/jumper bundle for the moving sensor
- 0.96-inch I2C OLED for a future standalone display
- Tripod insert or rubber feet

## Expected measurement envelope

The VL53L1X data sheet advertises distance performance that depends strongly on
timing budget, target reflectance, ambient light, cover glass, and field of view.
Treat 0.1–3 m indoors as an initial engineering target, then record actual test
results for the finished build. Dark, angled, small, transparent, or sunlit
targets can perform worse.

## Parts deliberately avoided

The common HC-SR04 ultrasonic module has a 5 V echo output and requires a level
divider before connection to Pi GPIO. This design uses the I2C ToF sensor to
reduce wiring risk and improve angular resolution. It is still a rangefinder,
not true radio radar.
