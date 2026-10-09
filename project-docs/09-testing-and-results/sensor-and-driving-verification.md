# Sensor and driving verification (2026-09)

## Driving
Verified by GPS displacement over time, not instantaneous speed: about 38 m
in 10 s at a commanded 15 km/h; negative displacement in reverse; a curving
track when steering.

## IMU
- Stationary: `linear_acceleration.z ≈ 9.808` (gravity, correct sign).
- Driving and steering: gyro and accelerometer respond and settle as
  expected.
- Orientation reads `(0,0,0,1)` as designed.

## Camera
Pixel statistics of a live `/vehicle/camera/image_color` message
(`min=12, max=255, mean=121.34`) confirmed real image content.

## Point cloud
Centre pixel of `/vehicle/points`: `x=0, y=0, z=75.4` (optical convention),
which led to the optical/body frame fix. Cloud lies flat in RViz with a body
fixed frame.

## Ackermann geometry
Commanding 0.3 rad (17.19°) put the left (inner) wheel at +18.22°, as
Ackermann geometry predicts.

## Relay steering parity with the real bridge
vehicle_bridge's `serial_bridge_node` in `dry_run:=true` ran against the live
sim's `/cmd_ackermann` and `/steering/angle` for 12 s with no "no
/steering/angle" warnings. Identical relay decisions are guaranteed by both
importing the same class; the decision streams were not diffed.
