# Q-009 · Should sensor messages be stamped with sim time?

- **Opened:** 2026-10-08 · **Status:** Open · **Priority:** medium

`/clock` is sim time (about 0.55× real time) but camera, depth, GPS and IMU
stamps are wall-clock. Consumers must map stamps to sim time
(`cart_driver`'s `ClockMap`), and message-filter time sync across
wall-stamped and sim-stamped topics is error-prone. Check whether
`webots_ros2_driver` can stamp with sim time (e.g. a `use_sim_time`
parameter on the driver node) and whether anything depends on wall stamps.
