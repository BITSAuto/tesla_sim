# D-016 · `/vehicle/emergency_brake` is the only way to brake

- **Date:** 2026-10-08
- **Status:** Accepted ([PR #1](https://github.com/BITSAuto/tesla_sim/pull/1); same topic added to vehicle_bridge in its PR #1)

## Context
On the cart, braking is for emergencies only. Normal commands must never be
able to brake by accident (e.g. a 0 or negative speed).

## Decision
A separate `std_msgs/Bool` topic, `/vehicle/emergency_brake`: `true` stops the
car instantly and holds it, `false` releases. Nothing else brakes. The same
topic and semantics exist on the real cart (vehicle_bridge).

## Consequences
- Only `cart_driver`'s safety monitor publishes it.
- The engage and release are logged from two separate calls, because rclpy
  forbids one log call site changing severity
  ([cart-fidelity-bugs.md](../07-bugs-and-lessons/cart-fidelity-bugs.md)).
