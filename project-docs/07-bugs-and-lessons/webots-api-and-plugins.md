# Webots API and plugin bugs

## M-01: The Webots vehicle Driver API is a silent no-op
- **Found:** 2026-09-08
- **Symptom:** `Driver.setCruisingSpeed()`/`setSteeringAngle()` stored and
  echoed their values, the gear sat at 0, and the car didn't move (or drifted
  0.01–0.7 m/s by GPS, not growing with the command).
- **Root cause:** `webots_ros2_driver`'s `driver` steps with `wb_robot_step()`,
  never `wbu_driver_step()`, so the cruise controller never runs
  ([webots-internals.md](../04-knowledge/webots-internals.md)). The upstream
  demo has the same bug and never notices.
- **Dead end:** a separate plain extern controller couldn't attach
  (`Cannot connect to Webots instance`) because the ROS driver already
  occupied the robot. `nm -D` on the binary gave the answer in one command.
- **Fix:** drive the wheel and steering motors directly
  ([D-003](../03-decisions/D-003-drive-wheel-motors-directly.md)).
- **Rule:** a value that is stored and read back correctly hasn't
  necessarily done anything. Verify the physical effect.

## M-02: A bare `<plugin>` tag's `name=` attribute is not a parameter
- **Found:** 2026-09-09
- **Symptom:** the driver crashed at start-up (`InvalidTopicNameError` →
  `terminate()` → SIGABRT) after adding `Ros2IMU`.
- **Root cause:** `<plugin type="...Ros2IMU" name="imu">` left the plugin's
  `name` parameter empty, so the topic became `"~/"`. Only `<device>` tags get
  their name filled in automatically.
- **Fix:** nested `<topicName>~/imu</topicName>` and `<frameName>imu</frameName>`.
- **Rule:** read the plugin's parameter-parsing code instead of assuming
  device-style defaults apply.

## M-03: IMU orientation documented as invalid before checking a live message
- **Found:** 2026-09-09
- **Symptom:** comments and README said `Imu.orientation` would be an
  "invalid zero quaternion".
- **Root cause:** reasoning from the code path. A live message showed
  `(0, 0, 0, 1)`: valid, just never updated. That fails silently downstream
  ("no rotation, forever"), which is a different warning to give.
- **Fix:** corrected in place in the code comment and the README.
- **Rule:** when documenting a field's behaviour, read a real message.

## M-04: Point cloud rendered sideways in RViz
- **Found:** 2026-09-09
- **Symptom:** clouds stood vertically against RViz's grid; a URDF rotation
  was suspected.
- **Diagnosis:** the centre pixel of a live `/vehicle/points` message was
  `x=0, y=0, z=75.4`: depth on Z, i.e. camera-optical convention, not a
  rotation bug. The URDF has no link geometry to rotate.
- **Fix:** optical frames plus static transforms back to body frames, the
  standard ROS camera pattern ([frames-and-conventions.md](../02-architecture/frames-and-conventions.md)).
  RViz's fixed frame must be a body frame.
- **Rule:** read one raw data point before theorising.
