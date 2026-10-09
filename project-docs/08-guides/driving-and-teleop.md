# Driving and teleop

## By topic
```bash
ros2 topic pub -r 10 /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 3.0}, angular: {z: 0.1}}"
ros2 topic pub -r 10 /cmd_ackermann ackermann_msgs/msg/AckermannDrive "{speed: 5.0, steering_angle: 0.0}"
ros2 topic pub --once /cmd_ackermann ackermann_msgs/msg/AckermannDrive "{}"     # release throttle: coast
ros2 topic pub --once /vehicle/emergency_brake std_msgs/msg/Bool "{data: true}"  # emergency stop (instant)
ros2 topic pub --once /vehicle/emergency_brake std_msgs/msg/Bool "{data: false}" # release
```
- `/cmd_ackermann.speed` is **km/h**; `steering_angle` is rad, **+ = right**.
- Speed 0 coasts (about 2.4 m from 5 km/h); it never brakes.
- Steering ramps at about 12.9 °/s and stops at ±15°.

## Keyboard
```bash
ros2 run tesla_sim ackermann_teleop_keyboard
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```
`ackermann_teleop_keyboard`: `w`/`s` speed, `a`/`d` steer, space centres,
`x` stops (coasts), `+`/`-` step size, `q` quits. It publishes once per key
press; the sim holds the last command. For `teleop_twist_keyboard`, set
`<cmdTimeout>1.0</cmdTimeout>` in `resource/tesla.urdf` so the car coasts
when you stop pressing keys.

## Check that it really moves
Don't trust a single speed reading. Record `/vehicle/gps`, hold a command for
some seconds, and compare positions
([diagnosis-pitfalls.md](../07-bugs-and-lessons/diagnosis-pitfalls.md)).
