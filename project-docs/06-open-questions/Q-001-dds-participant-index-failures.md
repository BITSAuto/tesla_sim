# Q-001 · What still causes intermittent DDS participant-index failures?

- **Opened:** 2026-09-09 · **Status:** Open · **Priority:** high when it happens

## Symptom
`rmw_create_node: failed to create domain` / `Failed to find a free
participant index for domain N`, and `webots_controller_vehicle` aborting
(SIGABRT) in a loop.

## Already found and fixed
Orphaned nodes from a stale stop script, a zero-backoff respawn storm, and a
stray `ros2 topic echo` holding a slot
([process-cleanup-and-dds.md](../07-bugs-and-lessons/process-cleanup-and-dds.md)).
It recurred at least once after all three, with no orphan found.

## Ruled out
- Too few slots: the default ceiling is 99 ([ros-and-dds-environment.md](../04-knowledge/ros-and-dds-environment.md)).
- `/dev/shm/fastrtps_port*` clutter: probably unrelated (reasoned, not proven).

## Prime suspect (2026-10-02)
A custom `CYCLONEDDS_URI` built for an unrelated multi-machine setup (one
VPN interface, multicast off, static peers including an offline host).
It reproduced the failure reliably on a local domain; unsetting it fixed node
creation, but then nodes with different settings can't discover each other,
so the sim and every terminal must agree. Whether unsetting it everywhere
fully cured it was never confirmed. The run script will not unset it
([D-009](../03-decisions/D-009-do-not-override-cyclonedds-uri.md)).

## Other theory, untested
A node killed by SIGABRT may leave its UDP ports in `TIME_WAIT` for up to
~60 s, so an immediate retry fails and a later one works. To test: force a
crash and watch `ss -tuln` for CycloneDDS's ports while retrying.

## What would close this
A controlled A/B with and without the custom DDS config over several
launch/stop cycles.
