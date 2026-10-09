# Troubleshooting

| Symptom | Likely cause | What to do |
| --- | --- | --- |
| Commands do nothing | Different `ROS_DOMAIN_ID` or DDS config between terminals; another graph using the same generic topics | Check a live subscriber sees messages (`ros2 topic echo`); export the same domain everywhere; use an unused domain |
| `failed to create domain` / `Failed to find a free participant index`; driver aborting in a loop | Orphaned nodes, a stray `ros2 topic echo`, or a custom `CYCLONEDDS_URI` | `ps aux \| grep -i ros2`; stop leftovers; wait a minute; try a plain shell without custom DDS config. See [Q-001](../06-open-questions/Q-001-dds-participant-index-failures.md) |
| World loads with missing objects | Asset download dropped | [world-assets.md](world-assets.md) |
| Car doesn't move but speed reads high | Wedged against scenery | Check GPS displacement; restart the sim |
| Point cloud sideways in RViz | Fixed frame is an `_optical` frame | Use `camera` or `range_finder` |
| RViz display subscribed but empty | QoS mismatch (`/vehicle/points` is best-effort) | Match the display's QoS; check `ros2 topic info -v` |
| Build fails in `setup.py` (`canonicalize_version`, `--uninstall not recognized`) | `~/.local` setuptools | `PYTHONNOUSERSITE=1 colcon build --symlink-install ...` |
| Launch can't be stopped with Ctrl-C | Started as a background job with SIGINT ignored | Restore SIGINT in a wrapper; stop orphans by PID |
| Timing looks about 0.55× too slow | Wall-clock measurement | Use sim time |
| `ros2 topic info` says a live topic is unknown | Stale daemon cache | `ros2 daemon stop` |
| False obstacle at the start line | Old world with raised crossings | Pull `main` (crossings lowered in PR #1) |
