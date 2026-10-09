# Q-006 · Report the Driver API no-op upstream?

- **Opened:** 2026-09-09 · **Status:** Open · **Priority:** low

The `driver` executable never calls `wbu_driver_step()`
([webots-internals.md](../04-knowledge/webots-internals.md)), which looks like
a genuine `webots_ros2_driver` bug that the upstream Tesla demo also has. Nobody
has checked whether it is a known issue in `cyberbotics/webots_ros2`.
