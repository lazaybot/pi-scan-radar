# Calibration and test plan

## 1. Servo center and safe travel

Set the servo to 90° before attaching the horn. Mark the physical straight-ahead
line. Test -20°, 0°, and +20° commands and measure actual angles with a printed
protractor. Increase the scan range only while the bracket and cable remain clear.

If the servo buzzes or presses against a stop, disconnect power immediately and
reduce the pulse or angular range. The defaults in code are not universal.

## 2. Range bias

Place a large matte target perpendicular to the sensor at measured distances of
0.25, 0.50, 1.00, 1.50, and 2.00 m. Collect at least 30 samples per distance.
Record mean error, standard deviation, ambient lighting, and target material.
Do not conceal poor readings; they define the actual operating envelope.

## 3. Angular alignment

Place a narrow target at known angles. Compare the center of the detected group
with the protractor angle. A constant offset belongs in the mechanical alignment
or a documented software correction.

## 4. Repeatability

Scan the same scene left-to-right and right-to-left ten times. Compare detected
centers and nearest ranges. Direction-dependent error suggests servo backlash;
random dropouts suggest lighting, target, wiring, or timing problems.

## Acceptance targets for the first prototype

- No mechanical collision over the configured range
- No undervoltage warning during ten continuous sweeps
- Median distance error below 5 cm from 0.25–2.0 m on a matte indoor target
- Angular center repeatability within 5° for a fixed target
- Clean shutdown and readable CSV after portable operation

These are project targets, not currently verified hardware results.
