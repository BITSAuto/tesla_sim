# Interfaces

## Command topics (subscribed)

| Topic | Type | Meaning |
| --- | --- | --- |
| `/cmd_ackermann` | `ackermann_msgs/AckermannDrive` | `speed` in **km/h** (kept for the upstream lane follower and the Jetson stack), `steering_angle` in rad, **+ = right**. 0 speed = release throttle and coast |
| `/cmd_vel` | `geometry_msgs/Twist` | `linear.x` m/s, `angular.z` = steering angle in rad (not a yaw rate) |
| `/vehicle/emergency_brake` | `std_msgs/Bool` | `true` stops the car instantly and holds it; `false` releases. The only way to brake |

Steering commands are clamped to ±`maxSteeringDeg` (15°). Negative speeds
reverse; a change of direction coasts through zero first.

## Published topics

| Topic | Type | Notes |
| --- | --- | --- |
| `/vehicle/speed` | `std_msgs/Float32` | measured speed, m/s, from the rear-wheel position sensors |
| `/bitsauto/speed` | `std_msgs/Float32` | the same in km/h, under the real cart's legacy topic name |
| `/steering/angle` | `std_msgs/Float32` | measured left-wheel steering angle in degrees, + = right, under the real cart's topic name |
| `/vehicle/camera/image_color` | `sensor_msgs/Image` | 1280×720 RGB |
| `/vehicle/camera/camera_info` | `sensor_msgs/CameraInfo` | |
| `/vehicle/camera/recognitions` | `vision_msgs/Detection2DArray` | ground-truth object recognition |
| `/vehicle/range_finder/image` | `sensor_msgs/Image` | 32FC1 depth in metres, 848×480; `inf` beyond max range |
| `/vehicle/range_finder/image_registered` | `sensor_msgs/Image` | depth reprojected into the colour camera's framing |
| `/vehicle/range_finder/point_cloud` | `sensor_msgs/PointCloud2` | XYZ cloud from the driver, depth framing |
| `/vehicle/points` | `sensor_msgs/PointCloud2` | XYZRGB cloud in the colour camera's framing (best-effort QoS) |
| `/vehicle/gps` | `geometry_msgs/PointStamped` | ground-truth world position of the GPS, which sits at the front bumper; `frame_id: gps` has no TF ([Q-002](../06-open-questions/Q-002-gps-has-no-tf-frame.md)) |
| `/vehicle/imu` | `sensor_msgs/Imu` | angular velocity and linear acceleration; orientation is always `(0,0,0,1)` |
| `/clock` | `rosgraph_msgs/Clock` | sim time |

All sensor message header stamps are **wall-clock**, not sim time; see
[webots-internals.md](../04-knowledge/webots-internals.md#time-sim-clock-vs-wall-clock-stamps).

## Plugin properties (`resource/tesla.urdf`)

| Property | Default | Meaning |
| --- | --- | --- |
| `cmdTimeout` | `0.0` (off) | with no command for this many seconds, release throttle and coast. Set `1.0` for keyboard teleop |
| `maxSteeringDeg` | `15.0` | steering clamp; the cart's lock |
| `coastDecel` | `0.4` m/s² | deceleration while coasting (placeholder until measured on the cart) |
| `driveTimeConstant` | `1.0` s | first-order lag of the throttle response |

## Launch arguments (`tesla_sim.launch.py`)

| Argument | Default | Meaning |
| --- | --- | --- |
| `world` | `tesla_city.wbt` | world file under `worlds/` |
| `pointcloud` | `true` | run the point-cloud pipeline |
| `colored` | `true` | build the coloured `/vehicle/points` cloud |
| `autonomous` | `false` | also run the upstream lane follower (publishes `/cmd_ackermann`) |
| `rviz` | `false` | open RViz with `config/tesla_sim.rviz` |
| `port` | `1234` | **uncommitted work in progress**, see [05-status/in-progress.md](../05-status/in-progress.md) |
