# tesla_sim

Webots Tesla Model 3 in a city, with an RGB camera and a depth camera, driven
over ROS 2 topics. Derived from the upstream `webots_ros2_tesla` demo, with the
depth sensor, a GPS, a working control interface and local launch plumbing
added.

## Running

Everything ROS-side lives in the **ubuntu22 distrobox** (ROS 2 Humble). Webots
itself is the host snap install (R2025a), reached from inside the container
through `/run/host`.

```bash
distrobox enter ubuntu22 -- ~/ros2_ws/scripts/run_tesla_sim.sh
distrobox enter ubuntu22 -- ~/ros2_ws/scripts/run_tesla_sim.sh autonomous:=true rviz:=true
~/ros2_ws/scripts/stop_tesla_sim.sh
```

`stop_tesla_sim.sh` sends `SIGINT` to the `ros2 launch` process itself first
(the same as pressing Ctrl-C in the launch's terminal), which cascades a clean
shutdown to every node the launch manages -- including ones added to the
launch file later, with nothing to keep in sync. A fixed list of process-name
patterns is kept as a fallback in case anything survives the graceful path (or
is left over from a run that wasn't stopped through this script). Always stop
the sim with this script rather than closing its terminal or killing
individual node processes by hand -- see **Troubleshooting** below for what
happens when things get killed piecemeal instead.

`run_tesla_sim.sh` does not set `ROS_DOMAIN_ID` or `CYCLONEDDS_URI` -- it
inherits whatever your shell provides. This is deliberate: don't add either
override to the script without checking first, since different setups on the
team manage these differently and a hardcoded value in the script would
silently override that. Every terminal you use with tesla_sim -- teleop, a
manual `ros2 topic pub`, `ros2 topic echo` -- needs to agree on the same
`ROS_DOMAIN_ID` as whichever terminal launched the sim, or they simply won't
see each other. If your shell profile also runs another, larger ROS graph on
the same default domain (e.g. `cart_controller`/nav2), sharing that domain
with tesla_sim is not free: bare, generic topic names like `/cmd_vel` can
collide with that graph's own nodes, and a crowded DDS domain with unrelated
discovery traffic has been observed to cause intermittent flakiness --
commands that get lost or match late, which looks like the sim randomly
starting and stopping responding with no code change involved. If that shows
up, try picking an unused `ROS_DOMAIN_ID` (export it consistently in every
terminal you use for that run) to rule it out -- see **Troubleshooting**
below for more if that alone doesn't fix it.

Launch arguments: `world` (default `tesla_city.wbt`), `pointcloud` (default
true), `colored` (default true), `autonomous` (default false, runs the upstream
lane follower), `rviz` (default false).

## Driving it

| Topic | Type | Meaning |
| --- | --- | --- |
| `/cmd_vel` | `geometry_msgs/Twist` | `linear.x` m/s, `angular.z` steering angle in rad |
| `/cmd_ackermann` | `ackermann_msgs/AckermannDrive` | `speed` in **km/h**, `steering_angle` in rad |
| `/vehicle/speed` | `std_msgs/Float32` | measured speed in m/s, from the rear wheel encoders |
| `/bitsauto/speed` | `std_msgs/Float32` | same measurement, in km/h, under the real vehicle's own global topic name |
| `/steering/angle` | `std_msgs/Float32` | measured steering angle in degrees (+right/-left), under the real vehicle's own global topic name |

`/cmd_ackermann` is in km/h rather than m/s to stay compatible with the upstream
lane follower and with the Jetson's `stereo_driving` stack. Steering is clamped
to ±0.5 rad. Negative speeds reverse.

**Steering is not instant.** The real vehicle has no proportional steering
input -- only a three-state relay (left/stop/right) that runs continuously
until explicitly stopped. tesla_sim models that same relay + hysteresis
behavior (`vehicle_bridge.relay_steering.RelaySteeringController`, shared with
the real vehicle's own serial bridge, package `vehicle_bridge`) rather than
snapping to a commanded angle instantly, so a controller's step response in
sim matches what it'll see on real hardware. Commanding a step change in
`steering_angle` will ramp toward it at a fixed rate rather than arriving
immediately -- this is intentional, not lag. `/steering/angle` and
`/bitsauto/speed` publish under the real vehicle's exact global topic names
(not namespaced under `/vehicle/...` like this package's other topics) so
that control code written for the real vehicle can run against tesla_sim with
zero changes -- see `vehicle_bridge`'s README for the full protocol this
mirrors and what's calibrated against real hardware versus still unverified.

```bash
ros2 topic pub -r 10 /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 8.0}, angular: {z: 0.1}}"
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

For keyboard teleop, set `<cmdTimeout>1.0</cmdTimeout>` in `resource/tesla.urdf`
so the car coasts to a stop when you stop pressing keys.

`tesla_sim` also ships its own keyboard teleop, `ackermann_teleop_keyboard`,
publishing `AckermannDrive` directly instead of `Twist` -- useful for staying
in km/h/steering-angle terms rather than converting through `Twist`, and for
matching what the Jetson's `stereo_driving` stack expects on the wire:

```bash
distrobox enter ubuntu22 -- bash -c 'source /opt/ros/humble/setup.bash; source ~/ros2_ws/install/setup.bash; ros2 run tesla_sim ackermann_teleop_keyboard'
```

`w`/`s` change speed, `a`/`d` steer, space centres the steering, `x` stops,
`+`/`-` change step size, `q` quits. It publishes once per keypress rather
than on a timer -- Webots holds the last commanded wheel velocity, so a single
keypress produces sustained motion; there's no need to hold a key down.

## Sensing

The camera and depth sensor are calibrated to **Intel RealSense D435i** specs
(the real vehicle's actual hardware), not made-up numbers. The D435i's
camera/depth module is the same as the plain D435 -- the "i" only adds an
IMU -- so the optical specs below are D435 datasheet figures either way.

| Sensor | FOV (horizontal) | Resolution | Range |
| --- | --- | --- | --- |
| RGB (`camera`) | 69 deg | 1280x720 | -- |
| Depth (`range_finder`) | 87 deg | 848x480 | 0.105-10 m |

Both figures come from Intel's D435 datasheet: 0.105 m is the Min-Z at this
resolution, 0.3-3 m is the datasheet's "ideal" accurate range, 10 m is the
commonly cited usable max at reduced accuracy. The two sensors are placed at
the identical translation in the world file -- real hardware offsets them by
about 25mm, which is negligible against the meters-scale distances this
vehicle cares about, so that offset is approximated as zero. One consequence
of the FOV mismatch, matching real D435 point clouds: `/vehicle/points` has
colour only in the central ~69 degrees; the outer edges of the 87-degree
depth field have no corresponding colour pixel and come through uncoloured.

| Topic | Type | Notes |
| --- | --- | --- |
| `/vehicle/camera/image_color` | `sensor_msgs/Image` | 1280x720 RGB |
| `/vehicle/camera/recognitions` | `vision_msgs/Detection2DArray` | ground-truth object recognition |
| `/vehicle/range_finder/image` | `sensor_msgs/Image` | 32FC1 depth in metres, 848x480 |
| `/vehicle/range_finder/point_cloud` | `sensor_msgs/PointCloud2` | XYZ cloud, published by the driver itself, depth-camera resolution/framing |
| `/vehicle/points` | `sensor_msgs/PointCloud2` | XYZRGB cloud, registered onto the RGB camera's framing |
| `/vehicle/gps` | `geometry_msgs/PointStamped` | ground-truth position |
| `/vehicle/imu` | `sensor_msgs/Imu` | linear acceleration + angular velocity, from a simulated D435i IMU |

The D435i's onboard IMU is a Bosch BMI055 (confirmed via Intel's own
documentation), a raw 6-DoF sensor with no absolute-orientation output --
unlike Webots' `InertialUnit` device, which reports ground-truth orientation
directly and would not match real hardware. `/vehicle/imu` is built from
Webots `Gyro` + `Accelerometer` devices only, deliberately leaving out
`InertialUnit`, for fidelity to what the real sensor actually provides. One
consequence: the message's `orientation` field is permanently frozen at
`(0, 0, 0, 1)` -- a *valid* identity quaternion, just one that never updates
and silently reads as "no rotation" forever, not an obviously-broken value.
Ignore that field entirely; most fusion tools expect
`orientation_covariance[0] == -1` as the signal to do the same, which this
message does not set, so a relay node may be needed to add that if a
downstream tool insists on checking it. Values are noise-free and
unbounded-range (Webots defaults); if you need the BMI055's actual full-scale
range/noise modelled, commonly-cited defaults are +/-4g accel and +/-1000
deg/s gyro, but that could not be verified against Bosch's or Intel's current
spec pages from this environment -- treat those two numbers as a starting
point, not a confirmed spec.

Since the camera and depth sensor now have different FOVs/resolutions, the
depth image is not already registered to the colour image the way it would be
for two identical co-located sensors -- `depth_image_proc`'s `register_node`
reprojects depth into the camera's framing first (`/vehicle/range_finder/
image_registered`), the same thing the real RealSense SDK's `align_depth`
does, before `point_cloud_xyzrgb_node` builds the coloured cloud from that.
`/vehicle/range_finder/point_cloud` (the driver's own native cloud, no
`depth_image_proc` involved) is unaffected and stays in the depth sensor's own
framing throughout.

This package has one TF tree: `camera` (body frame, X forward/Y left/Z up,
matching the vehicle) is the parent of `range_finder` (identity transform,
approximating the negligible real baseline above) and of `camera_optical`;
`range_finder` is in turn the parent of `range_finder_optical`. The two
`_optical` frames hold the sensors' actual data in camera-optical convention
(X right, Y down, Z forward/depth) -- the standard split every ROS
camera/depth driver uses, needed because `register_node` requires a real
transform between the sensors to reproject, not merely identical framing.
RViz's fixed frame should be a body frame (`camera` or `range_finder`, already
set to the latter in `config/tesla_sim.rviz`), never one of the `_optical`
frames directly -- pointing RViz at a raw optical frame is what makes a cloud
render sideways, with "forward" running vertically against the grid instead
of lying flat on it.

## Troubleshooting

**The vehicle API does not actuate anything here.** The obvious way to drive a
Webots car is `Driver.setCruisingSpeed()`, which is what the upstream demo does.
`webots_ros2_driver`'s `driver` executable calls `wbu_driver_init()` but steps
the simulation with `wb_robot_step()` rather than `wbu_driver_step()`, so the
vehicle library's cruise controller never runs: commands are stored and read
back correctly, but no torque reaches the wheels. `tesla_driver.py` therefore
drives the rear wheel motors and steering motors directly through the plain
Robot API, with Ackermann geometry taken from the PROTO (wheel radius 0.36 m,
wheelbase 2.94 m, track 1.72 m).

**Building needs `PYTHONNOUSERSITE=1`.** A newer setuptools in `~/.local`
shadows the system one and breaks `ament_python` builds with
`canonicalize_version() got an unexpected keyword argument`:

```bash
distrobox enter ubuntu22 -- bash -c 'cd ~/ros2_ws && PYTHONNOUSERSITE=1 ./scripts/build.sh --packages-select tesla_sim'
```

**`rmw_create_node: failed to create domain` / `Failed to find a free
participant index` / `webots_controller_vehicle` aborting in a loop.** This is
CycloneDDS running out of local DDS participant slots on the domain in use,
surfacing here as an uncaught C++ exception (`terminate()` -> `SIGABRT`) rather
than a clean error, since `rclcpp` doesn't handle a failed node-creation
gracefully. A few distinct contributing causes were found and fixed while
chasing this:

- *Orphaned nodes from an incomplete stop.* Before `stop_tesla_sim.sh` sent
  `SIGINT` to the launch process itself (see **Running** above), it only
  killed a fixed list of process names -- any node added to the launch file
  after that list was written (this happened twice: `register_node` and four
  `static_transform_publisher`s, added for the D435/D435i work) was silently
  left running on every single stop, each holding a participant slot forever.
  Fixed by switching to the SIGINT-cascade approach, which doesn't need a
  process list kept in sync with the launch file.
- *A crash-storm with no backoff.* `WebotsController` is launched with
  `respawn=True` and, until fixed, the default `respawn_delay=0.0` -- instant
  retry. If the driver can't create its DDS node for any reason, it aborts via
  the uncaught-exception path above rather than shutting down cleanly, and
  likely leaks that failed attempt's own half-initialized participant slot.
  Instant retry turns one transient failure into a storm that can burn through
  the remaining slot pool in seconds, guaranteeing it can never recover on its
  own. Fixed with `respawn_delay=2.0`.
- *Stray one-off diagnostic commands.* A `ros2 topic echo` (or similar) left
  running in another terminal holds a participant slot for as long as it
  runs. `pgrep -af "ros2 topic echo|ros2 topic hz|ros2 topic info"` (adjust to
  taste) will find these; they don't show up in the launch's own process tree
  so `stop_tesla_sim.sh` intentionally does not kill them -- doing so from a
  generic "stop the sim" script would risk killing an unrelated diagnostic
  session you're legitimately running in another window.

If you hit this and none of the above apply, check `ps aux | grep -i ros2` for
anything unexpected still running on your domain, and consider whether a
recent crash's sockets are still in the kernel's `TIME_WAIT` state (up to
~60s) -- waiting a minute before retrying is a reasonable first thing to try
before digging further. If your shell sets a custom `CYCLONEDDS_URI` (e.g. for
a multi-machine setup unrelated to this simulation), also consider whether
that config's discovery style is a factor -- tesla_sim is purely local and
doesn't need any custom DDS config at all, so testing with a plain shell (no
custom `CYCLONEDDS_URI`) is a reasonable way to rule that out specifically.

## World assets

The snap ships no PROTO files: R2025a resolves them from GitHub and hash-caches
them under `~/.cache/Cyberbotics/Webots/assets`. `tesla_city.wbt` pins every
`EXTERNPROTO` to the `R2025a` tag so it matches the installed simulator. Webots'
own downloader opens many parallel streams and intermittently drops some; if a
world loads with missing nodes, fill the gaps with:

```bash
grep -o "Cannot download '[^']*'" sim.log | cut -d"'" -f2 | ~/ros2_ws/scripts/warm_webots_assets.sh
```

Note that `webots://` URLs do **not** work with the snap — they resolve to
`$WEBOTS_HOME`, which contains no PROTOs. They would work on a source install
like the Jetson's.
