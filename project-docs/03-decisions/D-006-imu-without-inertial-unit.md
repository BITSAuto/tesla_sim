# D-006 · IMU from `Gyro` + `Accelerometer` only, no `InertialUnit`

- **Date:** 2026-09-09
- **Status:** Accepted

## Context
The D435i has a Bosch BMI055: a raw 6-axis IMU with no orientation output.
`webots_ros2_driver::Ros2IMU` can also take a Webots `InertialUnit`, which
gives ground-truth orientation for free.

## Decision
Use only `Gyro` and `Accelerometer`. Leave `inertialUnitName` out.

## Alternatives considered
- **Add `InertialUnit`:** rejected. It would simulate a capability the real
  sensor doesn't have, defeating the point of hardware fidelity.

## Consequences
- `Imu.orientation` stays at the message default `(0,0,0,1)` forever: a valid
  identity quaternion, not an invalid one. Consumers must ignore it.
  (This was first documented wrongly as an "invalid zero quaternion"; see
  [webots-api-and-plugins.md](../07-bugs-and-lessons/webots-api-and-plugins.md#m-03-imu-orientation-documented-as-invalid-before-checking-a-live-message).)
- `orientation_covariance[0]` is not set to −1; a relay node may be needed for
  fusion tools that check it.
