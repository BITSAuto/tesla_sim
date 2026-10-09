# ROS and DDS environment

### CycloneDDS `MaxAutoParticipantIndex` defaults to 99
**Verified** from the XSD schema in `eclipse-cyclonedds/cyclonedds`
(`etc/cyclonedds.xsd`). This ruled out "too few slots" as the cause of
participant-index failures ([Q-001](../06-open-questions/Q-001-dds-participant-index-failures.md)).

### `/dev/shm/fastrtps_port*` files are not CycloneDDS's
**Verified**: they belong to `rmw_fastrtps_cpp`, used by background
`ros2-daemon` processes; tesla_sim's nodes run `rmw_cyclonedds_cpp` (checked
in each process's environment). Probably unrelated to Q-001, but reasoned
rather than proven.

### `distrobox enter ... -- bash -c '...'` sources `~/.bashrc`
**Verified** by reading a launched process's `/proc/<pid>/environ`: variables
set only in `~/.bashrc` (`ROS_DOMAIN_ID`, `CYCLONEDDS_URI`) were present.
A plain non-interactive `bash -c` outside distrobox does not source it;
distrobox's wrapper does. Check a live process's environment rather than
reasoning about shell semantics.

### Generic topic names collide across graphs
**Verified** (2026-09-08): sharing a domain with another ROS graph that also
uses `/cmd_vel` made teleop commands go to the wrong consumer. Use a domain of
your own for the sim (exported in every terminal).

### `ros2 topic info`/`echo` can return stale results
**Verified** once: a live topic reported `Unknown topic` until `ros2 daemon
stop` (it restarts on the next command).

### Background jobs in a non-interactive shell ignore SIGINT
**Verified** (2026-10-08): `cmd &` in a non-interactive bash starts `cmd`
with SIGINT ignored, so `ros2 launch` started that way can't be stopped with
Ctrl-C/`kill -INT` and leaves orphans. Wrap it so SIGINT is reset to default
first (e.g. a small `exec` wrapper that sets `signal.SIGINT` to `SIG_DFL`).

### `pkill -f` / `pgrep -f` can match the calling shell
**Verified** (2026-10-08): a stop command whose own text contains the pattern
kills the shell running it. Run the stop script as its own command.
