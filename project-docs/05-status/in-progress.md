# In progress

## Multi-instance support: a `port` launch argument (uncommitted)
- **Owner:** unknown (a collaborator's change, not made in a recorded
  session). Last modified 2026-10-06.
- **Where:** uncommitted edit to `launch/tesla_sim.launch.py` in the
  laptop's working copy. It is **not** on any branch; it has deliberately been
  left out of every commit since.
- **What it does:** adds `port` (default 1234) so a second Webots instance can
  run beside the first (with a different `ROS_DOMAIN_ID`). Moves Webots, the
  supervisor and the driver into an `OpaqueFunction`, and replaces the
  bundled `Ros2Supervisor` process with one whose `WEBOTS_CONTROLLER_URL`
  includes the port (the bundled one omits it, so a second instance's
  supervisor would attach to the first Webots).
- **Next step:** its owner should commit it on a branch and open a PR, or
  discard it. See [Q-008](../06-open-questions/Q-008-owner-of-the-port-change.md).
