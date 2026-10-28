# Assembly

1. Flash Raspberry Pi OS Lite, create the user account, and configure Wi-Fi/SSH.
2. Mount the Pi and PCA9685 on standoffs. Keep the servo supply terminals covered.
3. Build a rigid base wide enough that servo acceleration cannot tip the unit.
4. Center the servo using a 90° command with its horn removed.
5. Attach the horn and sensor bracket so the sensor faces straight ahead at 90°.
6. Route the sensor cable with a loose service loop. Sweep it by hand through the
   intended range and verify the cable never tightens.
7. Wire the I2C devices and shared ground according to [WIRING.md](WIRING.md).
8. Run the simulation and tests before selecting `--hardware`.
9. With the servo horn still disconnected, run a narrow scan from -20° to +20°.
10. Attach the horn, repeat the narrow scan, then increase the envelope in 5°
    increments only if the mount remains clear.

## Enclosure guidelines

- Leave ventilation around the Pi.
- Keep the sensor window uncovered and free of fingerprints.
- Add strain relief at every wire that moves.
- Keep the center of mass over the base.
- Make the power switch reachable without touching the sweep area.

## Portable operation

Use a power bank that can supply the Pi and the expected servo current without
shutting down at light load. Shut the Pi down cleanly before removing power.
Carry the unit only when the servo is stopped and the moving head is secured.
