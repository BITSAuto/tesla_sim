# Hardware and environment

## The real cart this imitates

| Item | Value | Confidence | Details |
| --- | --- | --- | --- |
| Camera | Intel RealSense D435i (RGB + active-stereo depth + Bosch BMI055 IMU) | Verified | [realsense-d435i.md](../04-knowledge/realsense-d435i.md) |
| Camera mount | 1.52 m above the road, centred, pitched about 9° down | Verified (campus bag 2026-10-01) | [realsense-d435i.md](../04-knowledge/realsense-d435i.md#mount-on-the-cart) |
| Steering | three-state relay (left / stop / right), about 12.86 °/s, ±15° | Verified from the protocol scripts | vehicle_bridge's book |
| Speed | throttle only; releasing throttle coasts; the brake stops instantly | Verified (behaviour); coast rate **Assumed** 0.4 m/s² | [Q-007](../06-open-questions/Q-007-cart-dimensions-and-coast-rate.md) |
| Speed sensor | none known yet on the real cart | Assumed | cart_driver's book |
| Compute | Nvidia Jetson Orin AGX, Ubuntu 24.04, ROS 2 Jazzy | Verified | |

## Development machine (laptop)

- **ROS:** ROS 2 Humble inside a `distrobox` container named `ubuntu22`
  (Ubuntu 22.04). Build and run everything ROS-side from inside it.
- **Webots:** R2025a, installed on the host as a **snap**. The container
  reaches it through `/run/host/snap/webots/current/usr/share/webots`. The
  snap ships no PROTO files; see [webots-internals.md](../04-knowledge/webots-internals.md).
- **DDS:** `rmw_cyclonedds_cpp`.
- **Workspace:** `~/ros2_ws`, with each BITSAuto package cloned under
  `~/ros2_ws/src/`. The workspace's helper scripts (`scripts/run_tesla_sim.sh`,
  `stop_tesla_sim.sh`, `warm_webots_assets.sh`, `build.sh`) live in the
  workspace, not in this repo, except `scripts/run_tesla_sim.sh`, which this
  repo also ships as a portable copy.
- **Python packaging quirk:** a newer `setuptools` in `~/.local` breaks
  `ament_python` builds; build with `PYTHONNOUSERSITE=1`. See
  [08-guides/setup-and-build.md](../08-guides/setup-and-build.md).

## The Jetson Orin

The Orin runs Ubuntu 24.04 and ROS 2 Jazzy. No arm64 Webots snap exists, so
Webots there is **built from source** in `$HOME/webots`. The repo's
`scripts/run_tesla_sim.sh` detects that layout (see
[08-guides/running-the-sim.md](../08-guides/running-the-sim.md)).

## Simulation speed

Webots runs at roughly **0.55× real time** on the laptop with perception
running (2026-10-08). `/clock` carries sim time, but sensor message header
stamps are wall-clock. Anything that measures time must use sim time; see
[webots-internals.md](../04-knowledge/webots-internals.md#time-sim-clock-vs-wall-clock-stamps).
