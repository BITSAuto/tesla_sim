# D-003 · Drive the wheel motors directly, not through the Webots `Driver` API

- **Date:** 2026-09-08
- **Status:** Accepted (forced by a bug, not a preference)

## Context
The upstream demo calls `Driver.setCruisingSpeed()` and
`setSteeringAngle()`. In this stack these store and read back their values
but never move the car: `webots_ros2_driver`'s `driver` executable steps the
simulation with `wb_robot_step()` instead of `wbu_driver_step()`, so the
vehicle library's cruise controller never runs.

## Decision
`tesla_driver.py` sets `left_rear_wheel`/`right_rear_wheel` velocities
(`setPosition(inf)` + `setVelocity`) and the two steering motors' positions,
computing Ackermann geometry itself from the PROTO's dimensions.

## Consequences
- The car moves, verified by GPS displacement over time.
- The plugin owns all actuation, which later made the relay steering and the
  longitudinal model easy to add.
- Full diagnosis: [webots-api-and-plugins.md](../07-bugs-and-lessons/webots-api-and-plugins.md#m-01-the-webots-vehicle-driver-api-is-a-silent-no-op).
  Whether to report this upstream is
  [Q-006](../06-open-questions/Q-006-report-driver-api-bug-upstream.md).
