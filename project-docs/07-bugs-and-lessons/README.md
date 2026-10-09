# 07 · Bugs and lessons

Every bug found in or around tesla_sim: symptom, root cause, fix, and the
rule that would have prevented it. Several are patterns, not one-offs, so
read the relevant page before touching the driver plugin, the launch file or
anything DDS-related.

| Page | Bugs |
| --- | --- |
| [webots-api-and-plugins.md](webots-api-and-plugins.md) | M-01 Driver API no-op · M-02 bare `<plugin>` name · M-03 IMU orientation documented wrongly · M-04 point cloud rendered sideways |
| [process-cleanup-and-dds.md](process-cleanup-and-dds.md) | M-05 stale stop-script list · M-06 respawn crash storm · M-07 stray diagnostic process · M-08 backwards domain fix · M-09 guessed DDS limit |
| [diagnosis-pitfalls.md](diagnosis-pitfalls.md) | M-10 one explanation applied to two reports · M-11 black `scrot` screenshot · M-12 anchored `pgrep` |
| [cart-fidelity-bugs.md](cart-fidelity-bugs.md) | M-13 e-brake release crash · M-14 wall-clock timing · M-15 crossings read as a step · M-16 objects sink at the start |

## Recurring patterns

| Pattern | Seen in | Rule |
| --- | --- | --- |
| Trusting an API because it accepted and echoed a value | M-01, M-03 | Verify the physical effect (GPS displacement, a live message), not the API round trip |
| A cleanup or retry mechanism that silently goes stale | M-05, M-06 | Prefer mechanisms that need no maintained list; always back off retries |
| Reusing an earlier explanation for a similar-looking report | M-10 | Check the basics again (is anything arriving on the topic?) before reusing a diagnosis |
| A tool's own limitation mistaken for a finding | M-11, M-12 | Confirm the tool can see what you're checking |
| Reasoning about time, environment or limits instead of checking | M-08, M-09, M-14 | Read the live process environment, the real schema, the sim clock |

## Checklist before changing tesla_sim

- [ ] Touching the launch file: is the new node a child of `ros2 launch`, so
      the SIGINT stop covers it?
- [ ] A "commands do nothing" report: is anything arriving on the command
      topic at all? Same `ROS_DOMAIN_ID` and DDS config in every terminal?
- [ ] Citing a hardware number: Verified, Documented or Assumed? See
      [04-knowledge](../04-knowledge/README.md).
- [ ] A Webots/webots_ros2 API "should" work but doesn't: read the installed
      binary or the upstream source before assuming user error.
- [ ] Steering changes: are you changing tesla_sim, or vehicle_bridge's
      shared `RelaySteeringController`? The latter changes the real cart too.
- [ ] Timing anything: are you on sim time?
