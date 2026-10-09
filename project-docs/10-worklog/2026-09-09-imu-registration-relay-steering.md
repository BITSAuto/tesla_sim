# 2026-09-09 · IMU, depth registration, relay steering, DDS clean-up

**Who:** project owner, with Claude Code
**Goal:** finish D435i fidelity; make steering behave like the real relay; fix start-up failures.

## What was done
- IMU from gyro + accelerometer ([D-006](../03-decisions/D-006-imu-without-inertial-unit.md)); fixed the bare-plugin crash (M-02) and the orientation docs (M-03).
- `register_node` and the optical/body TF tree ([D-007](../03-decisions/D-007-register-depth-with-register-node.md), M-04).
- Built `vehicle_bridge` and moved steering to the shared relay controller
  ([D-010](../03-decisions/D-010-relay-steering-shared-with-vehicle-bridge.md));
  published `/steering/angle`, `/bitsauto/speed` ([D-011](../03-decisions/D-011-publish-under-the-real-carts-topic-names.md)).
- DDS participant failures: fixed the stale stop list, respawn storm and stray
  echo (M-05 to M-07); remaining cause open ([Q-001](../06-open-questions/Q-001-dds-participant-index-failures.md)).
  Owner declined overriding `CYCLONEDDS_URI` ([D-009](../03-decisions/D-009-do-not-override-cyclonedds-uri.md)).
- Two-tier docs with private notes ([D-012](../03-decisions/D-012-two-tier-documentation.md), now superseded).

## Results
- Relay parity dry run with vehicle_bridge: 12 s, no missing-angle warnings.
