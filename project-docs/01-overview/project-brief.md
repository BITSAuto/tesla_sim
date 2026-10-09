# Project brief

## What it is

A Webots simulation of a Tesla Model 3 in a small city, driven and sensed
entirely over ROS 2. The car body is a Tesla, but its sensors, steering and
speed behaviour imitate the **BITSAuto campus cart**: a RealSense D435i
camera mounted 1.52 m high, a relay-driven steering motor limited to ±15°,
throttle-only speed control that slows by coasting, and an emergency-only
brake. Package `tesla_sim`, `ament_python`, repository
[BITSAuto/tesla_sim](https://github.com/BITSAuto/tesla_sim).

## Why it exists

- **Test without the cart.** Most development happens remotely, without
  access to the vehicle. Perception (`traversability`) and driving
  (`cart_driver`) are developed and tested here first.
- **A "digital clone", not a demo.** The upstream `webots_ros2_tesla` demo
  had no depth sensor, used made-up sensor specs, and its control path does
  nothing (see [D-003](../03-decisions/D-003-drive-wheel-motors-directly.md)).
  tesla_sim matches the real hardware closely enough that a controller tuned
  here sees the same steering step response and stopping behaviour as on the
  cart.
- **Same interface as the real cart.** It listens and publishes on the same
  topics as `vehicle_bridge` (`/cmd_ackermann`, `/vehicle/emergency_brake`,
  `/steering/angle`), so driving code runs against either without changes.

## History in one paragraph

Started on 2026-09-08 by running the upstream demo, then forked into this
package to add a depth camera, a GPS and a working control path. On
2026-09-09 sensors were calibrated to D435/D435i datasheet figures, an IMU
was added, and steering was rewritten to the real cart's relay behaviour
(shared with `vehicle_bridge`). It became its own repository on 2026-09-13.
On 2026-10-08 it was made to behave like the cart longitudinally (coasting,
throttle lag, emergency brake), steering was clamped to ±15°, and the sensors
were moved to the real mount measured from a campus recording. See
[05-status/completed.md](../05-status/completed.md) for the full list.

## Requirements that shaped it

Reconstructed from what was asked for, in order:
1. Run the upstream Tesla demo locally with working ROS integration.
2. Full ROS 2 control plus a depth point cloud.
3. Sensors calibrated to the real hardware (D435i), not arbitrary numbers.
   Precision was an explicit, repeated priority.
4. Steering that behaves like the real relay ("simulate how the vehicle
   actually works").
5. Speed behaviour like the cart: never brake in normal driving, coast to
   slow down, emergency brake only.

## What "done" looks like

A teammate can clone, build and launch tesla_sim, drive it over the same
topics as the real cart, and get camera, depth, point cloud, IMU and GPS
data close enough to the real D435i-equipped cart to develop and check
perception and driving code.

## What it deliberately is not

- **Not a sensor-noise simulator.** Depth is ground truth from a
  `RangeFinder`; the IMU is noise-free; the camera and depth sensor share a
  pose (the real ~25 mm baseline is ignored). `traversability` adds D435-like
  depth noise itself when needed.
- **Not the cart's geometry.** The body is a Tesla Model 3 (2.94 m wheelbase).
  The cart's real dimensions are still unknown; see
  [Q-007](../06-open-questions/Q-007-cart-dimensions-and-coast-rate.md).
- **No ground-truth orientation.** On purpose; see
  [D-006](../03-decisions/D-006-imu-without-inertial-unit.md).
