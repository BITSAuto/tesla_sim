# Cart-fidelity bugs (2026-10-08)

Found while making the sim behave like the cart and testing `cart_driver`
against it.

## M-13: Releasing the emergency brake crashed the driver
- **Symptom:** the driver plugin threw on brake release; the same bug crashed
  vehicle_bridge's serial bridge.
- **Root cause:** one log call site was used with `warn` severity on engage
  and `info` on release. rclpy raises "Logger severity cannot be changed
  between calls" when a call site changes severity.
- **Fix:** two separate log calls (`7bf344f`).
- **Rule:** in rclpy, one log call site, one severity.

## M-14: Measuring in wall time made the speed model look 0.58× too slow
- **Symptom:** the throttle lag and coast measurements came out far too slow.
- **Root cause:** Webots runs at about 0.55× real time; the test timed in
  wall-clock seconds, and sensor stamps are wall-clock too.
- **Fix:** measure with `use_sim_time` against `/clock`.
- **Rule:** in this sim, time everything on sim time
  ([webots-internals.md](../04-knowledge/webots-internals.md#time-sim-clock-vs-wall-clock-stamps)).

## M-15: Pedestrian crossings read as a step, causing a false emergency brake
- **Symptom:** `cart_driver`'s safety monitor braked at the start line.
- **Root cause:** the crossings were visual-only slabs about 0.095 m above
  the road; depth geometry correctly saw a raised surface.
- **Fix:** lowered both crossings flush ([D-019](../03-decisions/D-019-lower-pedestrian-crossings.md)).
  `cart_driver` also ignores lethal cells under the vehicle's own footprint
  and requires two consecutive ticks before braking.
- **Rule:** when perception reports an obstacle, check the world before
  tuning thresholds; sim artefacts are real geometry to a depth camera.

## M-16: Objects spawned near the start sink into the road
- **Found:** 2026-10-02 (by `traversability`'s test scene)
- **Root cause:** the start is inside a `RoadIntersection` whose visible
  surface is about 10 cm above its collision surface.
- **Workaround:** drive about 20 m onto `road(5)` before spawning
  ([Q-010](../06-open-questions/Q-010-intersection-surface-offset.md)).
