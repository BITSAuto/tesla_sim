# Completed

Newest first.

## 2026-10-09 · Project docs
- This `project-docs/` book replaces the private notes
  ([D-020](../03-decisions/D-020-project-docs-replace-private-notes.md)).

## 2026-10-08 · Cart fidelity — [PR #1](https://github.com/BITSAuto/tesla_sim/pull/1), merged as `e9e33dd`
Commits `5f484ad`, `7bf344f`, `de39487`.
- Throttle lag and coast-only slowing, `longitudinal.py` with 6 unit tests
  ([D-015](../03-decisions/D-015-cart-like-longitudinal-model.md)).
- `/vehicle/emergency_brake` as the only brake ([D-016](../03-decisions/D-016-emergency-brake-is-the-only-brake.md)).
- Steering clamped to ±15° ([D-017](../03-decisions/D-017-clamp-steering-to-15-degrees.md)).
- Sensors moved to the cart's mount from the campus bag ([D-018](../03-decisions/D-018-camera-mount-from-campus-bag.md)).
- Pedestrian crossings lowered flush ([D-019](../03-decisions/D-019-lower-pedestrian-crossings.md)).
- Fixed: e-brake release crashed the driver (rclpy log severity).

## 2026-10-06 · Portable run script — `0785d4f`
- `scripts/run_tesla_sim.sh` for snap or source-built Webots, Humble or Jazzy
  ([D-014](../03-decisions/D-014-portable-run-script.md)).
- README documents that on the real cart `/steering/angle` comes from
  vehicle_bridge's `encoder_node`.

## 2026-09-13 · Own repository — `ec8c9f8`
- Published as BITSAuto/tesla_sim ([D-013](../03-decisions/D-013-own-repository.md)).

## 2026-09-09 · Hardware fidelity
- IMU (gyro + accelerometer) ([D-006](../03-decisions/D-006-imu-without-inertial-unit.md)).
- Depth registration and the optical/body TF tree ([D-007](../03-decisions/D-007-register-depth-with-register-node.md)).
- Relay steering shared with vehicle_bridge ([D-010](../03-decisions/D-010-relay-steering-shared-with-vehicle-bridge.md)),
  and measured speed/steering on the real cart's topic names ([D-011](../03-decisions/D-011-publish-under-the-real-carts-topic-names.md)).
- `stop_tesla_sim.sh` SIGINT cascade ([D-008](../03-decisions/D-008-stop-the-sim-with-a-sigint-cascade.md)),
  `respawn_delay=2.0`.
- `ackermann_teleop_keyboard`.

## 2026-09-08 · First working simulator
- Forked the upstream demo ([D-001](../03-decisions/D-001-fork-a-custom-package.md)),
  drove the wheel motors directly ([D-003](../03-decisions/D-003-drive-wheel-motors-directly.md)),
  added a `RangeFinder` ([D-002](../03-decisions/D-002-rangefinder-depth-not-simulated-stereo.md)),
  a GPS, `/cmd_vel` and `/cmd_ackermann`, point clouds.
- Sensors calibrated to D435 specs ([D-005](../03-decisions/D-005-calibrate-sensors-to-d435.md)).
- World `EXTERNPROTO`s pinned to `R2025a`; `warm_webots_assets.sh`.
