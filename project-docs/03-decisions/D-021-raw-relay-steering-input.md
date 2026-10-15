# D-021 · Accept raw relay commands on `/steering/command`

- **Date:** 2026-10-10 (Orin session, for road_follower); committed 2026-10-15
- **Status:** Accepted

## Context
`road_follower` steers the way the real cart's input works: a value 0–100,
above 50 turns right until told otherwise, below 50 left, 50 stops. It runs
its own relay control with a fitted actuation delay, so it needs to send relay
states, not a target angle.

## Decision
`tesla_driver` subscribes to `/steering/command` (`std_msgs/UInt8`). While
commands keep arriving (each counts for 0.5 s) they drive the simulated relay
directly and the `/cmd_ackermann` steering angle is ignored; speed still comes
from `/cmd_ackermann`. Parameters on `/tesla_driver` model the actuator:
`steer_delay_s`, `steer_start_delay_s`, `steer_stop_delay_s`,
`steer_rate_scale`, and `max_steer_deg` (end stop, default `maxSteeringDeg`).

## Consequences
- Two steering paths in the sim; `cart_driver` uses `/cmd_ackermann`,
  road_follower uses `/steering/command`. Don't run both.
- `vehicle_bridge` has no `/steering/command` input yet, so road_follower
  wouldn't steer the real cart.
