# Frames and conventions

## Units and signs

| Quantity | Convention | Why |
| --- | --- | --- |
| `/cmd_ackermann.speed` | km/h | Webots car convention, kept for the upstream lane follower and the Jetson stack |
| `/cmd_ackermann.steering_angle` | rad, **+ = right** | matches the real cart's encoder (`+right/-left`); opposite of REP 103 |
| `/steering/angle` | degrees, **+ = right** | the real cart's topic and convention |
| `/vehicle/speed` | m/s | |
| `/bitsauto/speed` | km/h | the real cart's legacy topic |
| IMU angular velocity | rad/s, standard (counter-clockwise +) | |

The sign conversion between sim and real is a plain `degrees()`/`radians()`;
there is **no sign flip** anywhere. Don't "fix" an apparent mismatch; see
[vehicle-model-facts.md](../04-knowledge/vehicle-model-facts.md#steering-sign).

## TF tree

```
camera                      body frame: X forward, Y left, Z up
├── range_finder            identity (the real ~25 mm baseline is ignored)
│   └── range_finder_optical    X right, Y down, Z forward (depth data)
├── camera_optical          X right, Y down, Z forward (image data)
└── imu                     identity
```

Four `static_transform_publisher`s in the launch file publish these. RViz's
fixed frame must be a **body** frame (`camera` or `range_finder`); pointing
it at an `_optical` frame makes clouds render sideways. `gps` is not in the
tree ([Q-002](../06-open-questions/Q-002-gps-has-no-tf-frame.md)).

Other repos add their own frames on top: `traversability` publishes
`<depth frame> → camera_ground` (on the road under the camera) and
`cart_driver` publishes `odom → base_link` (rear axle).

## World coordinates (tesla_city)

- Webots world frame: X east, Y north, Z up (ENU-like). `/vehicle/gps` is in
  this frame.
- The car spawns with its rear axle at (31.44, 47.01), heading yaw = π
  (towards −X). The GPS (front bumper) starts at about (27.66, 47.01).
- Details of the road loop, lane widths and junctions:
  [world-geometry.md](../04-knowledge/world-geometry.md).
