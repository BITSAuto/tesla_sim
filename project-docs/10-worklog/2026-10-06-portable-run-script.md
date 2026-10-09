# 2026-10-06 · Portable run script

**Who:** project owner, with Claude Code
- `0785d4f`: `scripts/run_tesla_sim.sh` detects snap vs source Webots, the ROS
  distro and the Qt plugin path ([D-014](../03-decisions/D-014-portable-run-script.md)).
- README: on the real cart `/steering/angle` comes from vehicle_bridge's
  `encoder_node`; run one vehicle per domain.
- Separately (not in a recorded session), someone started a multi-instance
  `port` change to the launch file; it is still uncommitted
  ([in-progress.md](../05-status/in-progress.md)).
