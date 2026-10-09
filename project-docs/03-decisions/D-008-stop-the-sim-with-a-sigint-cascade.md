# D-008 · Stop the sim with a SIGINT cascade, not a list of process names

- **Date:** 2026-09-09
- **Status:** Accepted

## Context
`stop_tesla_sim.sh` killed a fixed list of process names. Nodes added to the
launch file later (`register_node`, four `static_transform_publisher`s) were
never added to the list, survived every stop, and each held a DDS participant
slot. Twenty orphans had accumulated over four launches.

## Decision
Send `SIGINT` to the `ros2 launch` process (the same as Ctrl-C), which shuts
down every node it manages. Keep the name list only as a fallback.

## Consequences
- New nodes in the launch file are covered automatically.
- One-off diagnostic commands (`ros2 topic echo` in another terminal) are
  deliberately not killed; they may be someone's legitimate session.
- Lesson: [process-cleanup-and-dds.md](../07-bugs-and-lessons/process-cleanup-and-dds.md).
