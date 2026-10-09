# Vehicle model facts

### TeslaModel3 PROTO geometry
**Verified** from the cached PROTO file: wheelbase **2.94 m**, front and rear
track **1.72 m**, `TeslaModel3Wheel` tyre radius **0.36 m**. Used for the
Ackermann geometry and for converting wheel speed.

### Drivetrain devices
**Verified** by enumerating devices on a live connection: `left_steer`,
`right_steer` (Motor + PositionSensor); `left_rear_wheel`, `right_rear_wheel`
(Motor + PositionSensor + Brake); `engine_speaker`; six LED groups; plus the
camera, GPS and range finder. Rear-wheel drive (the two rear motors move the
car).

### Reference points on the body
**Verified** (2026-10-08, from the world file and GPS): the robot origin is
the rear axle; the GPS sits at the front bumper, **3.79 m** ahead of the rear
axle; the camera is about **1.67 m** ahead of the rear axle. `cart_driver`'s
`tesla_sim` profile uses these (front overhang 0.85 m, rear overhang 0.95 m,
width 1.85 m).

### Steering sign
**Verified**: in this stack a **positive** steering angle turns **right**, on
`/cmd_ackermann.steering_angle` (rad) and `/steering/angle` (deg). The `d`
(right) teleop key gives a positive angle, and the real encoder code says
"degrees (+right / -left)". Sim and real need only `degrees()`/`radians()`,
no sign flip. Rechecked on 2026-10-08: a positive command turns the car
right (clockwise, negative yaw rate on the IMU).

### Wheel angles vs rack angle
**Verified** live: commanding 0.3 rad (17.19°) put the left wheel's sensor at
**+18.22°**. Correct: for a right turn the left wheel is the inner wheel,
which Ackermann geometry turns more than the bicycle-model angle
(`radius = L / tan(rack)`, `left = atan(L / (radius − track/2))`). This is
why the hysteresis compares the target with the internal rack angle, not the
published wheel angle.

### Relay steering rate
**Verified** from the real hardware constants in `cart_controller/README.md`:
a 35 ms minimum pulse (the motor reacts in about 30 ms) moves the wheels
0.45°, so about **12.86 °/s**. An independent constant in
`rotary_encoder_driver.py` (`SIM_DEG_PER_SEC = 12.0`) agrees. From straight to
±15° takes about 1.2 s.

### Measured longitudinal behaviour (sim time)
**Verified** 2026-10-08 with `use_sim_time`: throttle lag reaches 63 % of
5 km/h in **1.00 s** and holds 4.99 km/h; throttle off coasts at
**0.40 m/s²**, stopping in **3.35 s** after **2.41 m**; the emergency brake
stops the car from 4.9 km/h in about **0.25 s** and holds it while throttle
is still commanded. See
[09-testing-and-results/longitudinal-and-brake.md](../09-testing-and-results/longitudinal-and-brake.md).

### The real cart's coast rate is unknown
**Assumed**: 0.4 m/s² (about 2.4 m from 5 km/h) is a placeholder. See
[Q-007](../06-open-questions/Q-007-cart-dimensions-and-coast-rate.md).
