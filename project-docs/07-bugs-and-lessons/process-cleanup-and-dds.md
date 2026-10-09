# Process cleanup and DDS bugs

See also [Q-001](../06-open-questions/Q-001-dds-participant-index-failures.md)
for what is still unresolved.

## M-05: The stop script's process-name list went stale twice
- **Found:** 2026-09-09
- **Symptom:** after four launches, 20 orphaned processes, each holding a DDS
  participant slot.
- **Root cause:** `stop_tesla_sim.sh` killed a fixed list of names;
  `register_node` and four `static_transform_publisher`s were added to the
  launch file later and never added to the list.
- **Fix:** SIGINT the `ros2 launch` process and let it cascade
  ([D-008](../03-decisions/D-008-stop-the-sim-with-a-sigint-cascade.md)).
- **Rule:** a cleanup driven by a maintained list breaks whenever the managed
  set grows. Signal the parent instead.

## M-06: `respawn_delay=0.0` turned one failure into a crash storm
- **Found:** 2026-09-09
- **Symptom:** `webots_controller_vehicle` aborting dozens of times a second.
- **Root cause:** `respawn=True` with the default zero delay. Each failed
  start aborted via an uncaught C++ exception and probably leaked a
  half-created participant slot, making recovery impossible.
- **Fix:** `respawn_delay=2.0` (a supported option).
- **Rule:** always give retries a backoff unless failure is proven
  side-effect-free.

## M-07: A stray diagnostic process held a DDS slot for an hour
- **Found:** 2026-09-09
- **Symptom:** participant-index failures with no orphaned sim nodes.
- **Root cause:** a forgotten `ros2 topic echo /cmd_ackermann` in another
  terminal.
- **Found by:** scanning every `/proc/<pid>/environ` for the domain's
  `ROS_DOMAIN_ID`, not by process name.
- **Rule:** hunt resource leaks by the resource key (environment value), not
  by guessing names.

## M-08: The first fix for a domain mismatch was backwards
- **Found:** 2026-09-08
- **Symptom:** teleop commands had no effect.
- **What went wrong:** the sim was assumed to be on a different domain
  because it was started via `bash -c`, which "doesn't source `.bashrc`". The
  advice was to unset `ROS_DOMAIN_ID` in the teleop terminal. But distrobox's
  wrapper does source `.bashrc`, so both were already on the same domain;
  unsetting would have created a mismatch. The real problem was sharing the
  domain with another graph that also uses `/cmd_vel`.
- **Rule:** check a live process's environment in the actual execution
  context before reasoning about shell semantics.

## M-09: Guessing CycloneDDS's participant limit
- **Found:** 2026-09-09
- **What went wrong:** a theory that the default `MaxAutoParticipantIndex`
  was about 10 nearly led to a "run fewer processes" change. The schema says
  99.
- **Rule:** look up the documented value before acting on "there must be a
  low limit".
