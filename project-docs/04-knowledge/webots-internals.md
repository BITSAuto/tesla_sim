# Webots and webots_ros2 internals

### The `driver` executable steps with `wb_robot_step`, not `wbu_driver_step`
**Verified** (2026-09-08) with `nm -D /opt/ros/humble/lib/webots_ros2_driver/driver`:
it imports `wbu_driver_init`, `wb_robot_step` and
`wbu_driver_initialization_is_possible`, but **not** `wbu_driver_step`. The
vehicle library's cruise controller only runs inside `wbu_driver_step()`, so
`Driver.setCruisingSpeed()`/`setSteeringAngle()` store values
(`getTargetCruisingSpeed()` echoes them) but never produce torque. Hence
[D-003](../03-decisions/D-003-drive-wheel-motors-directly.md).

### A bare `<plugin>` tag reads its config from nested tags only
**Verified** by reading `Ros2SensorPlugin.cpp` in `cyberbotics/webots_ros2`
(branch `master`; there is **no `humble` branch**). `Ros2SensorPlugin::init`
reads `topicName`, `frameName` and `name` from the parsed tag body. For a
`<device reference="...">` tag the device's Webots name fills `name`
automatically; a `name="..."` XML attribute on a bare `<plugin>` tag does
not. An empty name gives the topic `"~/"`, which crashes the driver at
start-up. Set `<topicName>` and `<frameName>` explicitly.

### `Ros2IMU` requirements and the orientation field
**Verified** from `Ros2IMU.hpp/.cpp` (same repo). It needs at least one of
`inertialUnitName`, `gyroName`, `accelerometerName`. It only writes
`Imu.orientation` when `inertialUnitName` is set; otherwise the field keeps
the IDL default `(0,0,0,1)`, a valid identity quaternion. A live message
confirmed this.

### `WebotsController` forwards `**kwargs` to `ExecuteProcess`
**Verified** from `webots_controller.py`. `respawn_delay` (default 0.0) is a
supported option, so `respawn_delay=2.0` is a one-line fix, not a workaround.

### The asset cache key is `sha1(url)`
**Verified**: computing `sha1sum` of a known `EXTERNPROTO` URL gives the
exact file name under `~/.cache/Cyberbotics/Webots/assets/`. This is what
`warm_webots_assets.sh` relies on to pre-fetch assets one at a time, around
Webots' flaky parallel downloader.

### The snap ships no PROTO files
**Verified** by listing `$WEBOTS_HOME`. `webots://` URLs resolve there and
fail on the snap. `EXTERNPROTO`s must be real
`https://raw.githubusercontent.com/...` URLs pinned to the **`R2025a`** tag
(the `develop` branch timed out or failed to resolve). `webots://` would work
on a source build like the Orin's.

### Time: sim clock vs wall-clock stamps
**Verified** (2026-10-08). `/clock` carries sim time, which runs at about
**0.55× real time** on the laptop with perception running. Sensor message
header stamps from `webots_ros2_driver` (camera, depth, GPS, IMU) are
**wall-clock** (e.g. `sec: 1791481645` while `/clock` read 450 s). Measuring
the longitudinal model in wall time made it look about 0.58× too slow.
Anything that times things must run with `use_sim_time` and convert sensor
stamps (`cart_driver`'s `timesync.ClockMap` does this). Whether the driver
should stamp with sim time is [Q-009](../06-open-questions/Q-009-sensor-stamps-are-wall-clock.md).

### Spawning and removing objects at runtime
**Verified** (2026-10-08): `/Ros2Supervisor/spawn_node_from_string`
(`webots_ros2_msgs/SpawnNodeFromString`) spawns a VRML node string, and
publishing a node name on `/Ros2Supervisor/remove_node` removes it. Used by
`traversability`'s test scene and `cart_driver`'s `tools/simtools.py`.
