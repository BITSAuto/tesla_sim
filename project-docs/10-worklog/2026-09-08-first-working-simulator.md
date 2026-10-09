# 2026-09-08 · First working simulator

**Who:** project owner, with Claude Code
**Goal:** run the upstream Tesla demo locally, then get full ROS 2 control and depth.

## What was done
- Ran `webots_ros2_tesla` end to end to confirm the plumbing.
- Forked it into `tesla_sim` ([D-001](../03-decisions/D-001-fork-a-custom-package.md)).
- Found the Driver API no-op by `nm -D` and drove the motors directly
  ([D-003](../03-decisions/D-003-drive-wheel-motors-directly.md), M-01).
- Added a `RangeFinder` and GPS; calibrated to D435 specs
  ([D-002](../03-decisions/D-002-rangefinder-depth-not-simulated-stereo.md),
  [D-005](../03-decisions/D-005-calibrate-sensors-to-d435.md)).
- Pinned `EXTERNPROTO`s to `R2025a`; wrote the asset warm-up script.
- Debugged teleop doing nothing: domain mismatch and topic collision with
  another graph (M-08, M-10). Owner declined hardcoding a domain
  ([D-004](../03-decisions/D-004-do-not-hardcode-ros-domain-id.md)).

## Results
- Car drives: ~38 m in 10 s at 15 km/h by GPS.
