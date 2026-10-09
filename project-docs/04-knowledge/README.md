# 04 · Knowledge

Facts we have established, grouped by topic, each with how it was checked.

**Confidence tags**
- **Verified:** checked directly against source code, a binary, a live
  system or a measurement here (the entry says which).
- **Documented:** from a datasheet or upstream docs, cross-checked at least
  once but not re-derived.
- **Assumed:** a placeholder, guess or inference. If it matters, it also has
  an open question.

| Page | Contents |
| --- | --- |
| [webots-internals.md](webots-internals.md) | How Webots and `webots_ros2_driver` actually behave: the Driver API bug, plugin parameter parsing, `Ros2IMU`, asset caching, PROTOs on the snap, time stamps |
| [vehicle-model-facts.md](vehicle-model-facts.md) | Tesla PROTO geometry, devices, steering sign, wheel vs rack angle, relay rate, measured longitudinal behaviour |
| [realsense-d435i.md](realsense-d435i.md) | D435/D435i specs, the IMU chip, and the cart's camera mount |
| [world-geometry.md](world-geometry.md) | The tesla_city road layout, lanes, start pose and surface quirks |
| [ros-and-dds-environment.md](ros-and-dds-environment.md) | CycloneDDS limits, distrobox environment inheritance, stale daemon caches, signals |
| [tooling.md](tooling.md) | Build quirks and diagnostic-tool limitations |

Facts about the real cart's serial protocol and steering hardware are in
`vehicle_bridge`'s book (`project-docs/04-knowledge/`).
