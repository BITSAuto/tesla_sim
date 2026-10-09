# D-001 · Build a custom `tesla_sim` package instead of extending the installed demo

- **Date:** 2026-09-08
- **Status:** Accepted

## Context
The starting point was the upstream `ros-humble-webots-ros2-tesla` demo, and
the team's existing Jetson setup (a source build of Webots plus a
`webots_ros2` checkout driving a custom two-camera stereo world). The demo
worked end to end, but it had no depth sensor, used made-up sensor numbers,
and its control path turned out not to move the car at all.

## Decision
Fork the demo into a new package, `tesla_sim`, rather than patching the
installed apt package or its checkout.

## Alternatives considered
- **Patch the installed package:** rejected. Devices, sensors and a new
  control path can't sensibly be added to a system package.

## Consequences
- The stock demo was verified working first, which confirmed the Webots ↔ ROS
  bridge and extern controllers were sound before anything was changed.
- tesla_sim owns its world, URDF and driver plugin.
