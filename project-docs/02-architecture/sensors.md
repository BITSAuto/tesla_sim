# Sensors

All sensors sit in the Tesla's front sensor slot at the real cart's camera
pose: **1.52 m above the road, centred, pitched about 9° down**
(`translation -2.12 0 1.115`, `rotation 0 1 0 0.157` relative to the slot),
measured from the 2026-10-01 campus recording
([D-018](../03-decisions/D-018-camera-mount-from-campus-bag.md)). With that
tilt the bonnet hides the road out to about 2.7 m; perception sees roughly
2.7–10 m ahead.

| Sensor | Webots device | Spec | Source of the spec |
| --- | --- | --- | --- |
| RGB camera | `Camera` | 69° horizontal FOV, 1280×720 | D435 datasheet (Documented) |
| Depth | `RangeFinder` | 87° horizontal FOV, 848×480, 0.105–10 m | D435 datasheet (Documented); ground-truth depth, no noise |
| IMU | `Gyro` + `Accelerometer` via `Ros2IMU` | noise-free, unbounded range | D435i has a Bosch BMI055 (Verified); range/noise not modelled |
| GPS | `GPS` | ground truth, front bumper (3.79 m ahead of the rear axle) | |

## Point clouds

Camera and depth have different FOVs and resolutions, so depth is not
pixel-aligned with colour. `depth_image_proc register_node` reprojects depth
into the colour camera's framing (`/vehicle/range_finder/image_registered`),
like the RealSense SDK's `align_depth`, and `point_cloud_xyzrgb_node` builds
`/vehicle/points` from that. Only the central 69° has colour; the outer
depth wedges come through uncoloured, as on a real D435.
`/vehicle/range_finder/point_cloud` is the driver's own XYZ cloud in depth
framing.

## IMU orientation

`Imu.orientation` is never written and stays at the message default
`(0, 0, 0, 1)`: a valid identity quaternion that silently reads as "no
rotation". Ignore it. `orientation_covariance[0]` is not set to −1, so a
relay node may be needed for fusion tools that check it
([D-006](../03-decisions/D-006-imu-without-inertial-unit.md)).

## What is approximated

- Camera, depth and IMU share one pose (the real camera–depth baseline is
  about 25 mm) — [Q-005](../06-open-questions/Q-005-sensor-baseline-approximated.md).
- Depth is perfect. Use `traversability`'s `depth_noise` node for D435-like
  noise (σ_z ∝ z²).
- No IMU noise or range limits — [Q-003](../06-open-questions/Q-003-bmi055-specs.md).
