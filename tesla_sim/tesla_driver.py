"""Webots plugin exposing the Tesla's actuators as ROS 2 topics.

Loaded by webots_ros2_driver via the <plugin> tag in resource/tesla.urdf, so it
runs inside the driver process with direct access to the Webots robot API.
Sensors are not handled here -- webots_ros2_driver discovers the camera, range
finder and GPS from the world automatically.

Why this does not use the Webots vehicle API
--------------------------------------------
The obvious implementation is Driver.setCruisingSpeed()/setSteeringAngle(),
which is what the upstream webots_ros2_tesla demo does. It does not work in this
setup: webots_ros2_driver's `driver` executable calls wbu_driver_init() but
steps the simulation with wb_robot_step() instead of wbu_driver_step(), so the
vehicle library's cruise controller never runs. The commands are stored --
getTargetCruisingSpeed() reports them back -- but no torque ever reaches the
wheels and the car just sits there jittering. (The upstream demo has the same
problem here; it never checks that its commands took effect.)

So this drives the rear wheel motors and the steering motors directly, which
goes through the plain Robot API that the driver does step correctly.

Steering itself is further constrained to match the real vehicle: the real
cart has no proportional steering input, only a three-state relay (turn
left / stop / turn right) that "has infinite run-on and does not stop by
itself" (cart_controller/README.md) -- closed-loop angle control is built
entirely in software on top of that, exactly like
road_segmentation/rotary_encoder_driver.py's real controller does with a real
rotary encoder. tesla_sim models the same relay + hysteresis behavior via
vehicle_bridge.relay_steering.RelaySteeringController (shared with the real
serial bridge, vehicle_bridge/serial_bridge_node.py) so a controller's step
response looks the same against either backend. See
private-notes/tesla_sim/02-decision-log.md D-11 and 07-decision-tree.md for
why this replaced the earlier instant/continuous steering implementation.

Interfaces:
  /cmd_vel        geometry_msgs/Twist            linear.x in m/s, angular.z is
                                                 the steering angle in rad
  /cmd_ackermann  ackermann_msgs/AckermannDrive  speed in km/h (Webots Car
                                                 convention, kept so the
                                                 upstream lane follower and the
                                                 Jetson stack work unchanged),
                                                 steering_angle in rad
  /vehicle/speed  std_msgs/Float32               measured speed in m/s, from the
                                                 rear wheel position sensors
  /bitsauto/speed std_msgs/Float32               same measurement, in km/h, under
                                                 the real vehicle's own topic name
                                                 so unmodified real-vehicle control
                                                 code can run against tesla_sim
  /steering/angle std_msgs/Float32               measured steering angle in degrees
                                                 (+right/-left, matching the real
                                                 rotary encoder's convention),
                                                 read from the left steering
                                                 joint's own Webots PositionSensor
                                                 -- real simulated physics, not
                                                 this plugin's internal estimate
"""

import math
import time

import rclpy
from ackermann_msgs.msg import AckermannDrive
from geometry_msgs.msg import Twist
from std_msgs.msg import Float32
from vehicle_bridge.relay_steering import RATE_DEG_S, RELAY_LEFT, RELAY_RIGHT, RelaySteeringController

KMH_TO_MS = 1 / 3.6

# TeslaModel3 PROTO geometry.
WHEEL_RADIUS = 0.36   # m, TeslaModel3Wheel tireRadius
WHEELBASE = 2.94      # m
TRACK = 1.72          # m
MAX_STEERING_ANGLE = 0.5  # rad
MAX_STEERING_DEG = math.degrees(MAX_STEERING_ANGLE)


class TeslaDriver:
    def init(self, webots_node, properties):
        self.__robot = webots_node.robot
        self.__timestep = int(self.__robot.getBasicTimeStep())

        # Rear-wheel drive: velocity control needs an unbounded position target.
        self.__wheels = [self.__robot.getDevice(name)
                         for name in ('left_rear_wheel', 'right_rear_wheel')]
        for wheel in self.__wheels:
            wheel.setPosition(float('inf'))
            wheel.setVelocity(0.0)

        self.__steers = [self.__robot.getDevice(name)
                         for name in ('left_steer', 'right_steer')]

        # Steering position sensor, purely for the /steering/angle publisher --
        # real simulated physics for any external consumer to close its own
        # loop against, independent of __rack_angle_deg below (this plugin's
        # own actuation target, not a sensor reading -- see module docstring).
        self.__steer_sensor = self.__robot.getDevice('left_steer_sensor')
        self.__steer_sensor.enable(self.__timestep)

        # Wheel encoders, differentiated for the measured speed.
        self.__encoders = [self.__robot.getDevice(name)
                           for name in ('left_rear_sensor', 'right_rear_sensor')]
        for encoder in self.__encoders:
            encoder.enable(self.__timestep)
        self.__last_encoder = None

        # Relay-steering state. __target_steer_deg is the last commanded
        # bicycle-model angle (same space as an AckermannDrive.steering_angle);
        # __rack_angle_deg is this plugin's own open-loop estimate of the
        # actuator's current angle in that same space, advanced by
        # RATE_DEG_S per step while a relay direction is engaged. Kept
        # separate from the real left/right *wheel* angles (which differ from
        # each other and from this bicycle-model angle by the Ackermann
        # geometry below) specifically so the hysteresis comparison in
        # RelaySteeringController.update() compares like with like.
        self.__steering_relay = RelaySteeringController()
        self.__target_steer_deg = 0.0
        self.__rack_angle_deg = 0.0

        # Optional dead-man: if no command arrives for this many seconds the car
        # coasts to a stop. 0.0 (default) disables it, which is what the
        # autonomous lane follower wants; teleop is nicer with ~1.0.
        self.__cmd_timeout = float(properties.get('cmdTimeout', 0.0))
        self.__last_cmd_time = None

        rclpy.init(args=None)
        self.__node = rclpy.create_node('tesla_driver')
        self.__node.create_subscription(Twist, 'cmd_vel', self.__on_cmd_vel, 1)
        self.__node.create_subscription(AckermannDrive, 'cmd_ackermann', self.__on_cmd_ackermann, 1)
        self.__speed_publisher = self.__node.create_publisher(Float32, 'vehicle/speed', 1)
        # Absolute (leading-slash) topic names: these two intentionally match
        # the real vehicle's global topic names exactly (road_segmentation's
        # rotary_encoder_driver.py subscribes to both under these names, not
        # under any /vehicle/... namespace), so that control code written
        # against the real vehicle can run against tesla_sim unmodified.
        self.__bitsauto_speed_publisher = self.__node.create_publisher(Float32, '/bitsauto/speed', 1)
        self.__steer_angle_publisher = self.__node.create_publisher(Float32, '/steering/angle', 1)

        self.__node.get_logger().info(
            'Tesla driver ready: /cmd_vel (m/s) and /cmd_ackermann (km/h), '
            f'cmd_timeout={self.__cmd_timeout}s')

    def __apply(self, speed_ms, steering_angle):
        for wheel in self.__wheels:
            wheel.setVelocity(speed_ms / WHEEL_RADIUS)

        steering_angle = max(-MAX_STEERING_ANGLE, min(MAX_STEERING_ANGLE, steering_angle))
        self.__target_steer_deg = math.degrees(steering_angle)
        self.__last_cmd_time = self.__node.get_clock().now()

    def __on_cmd_vel(self, message):
        self.__apply(message.linear.x, message.angular.z)

    def __on_cmd_ackermann(self, message):
        self.__apply(message.speed * KMH_TO_MS, message.steering_angle)

    def __update_steering(self, dt):
        """Advance the relay-steering state by one step and actuate it.

        Runs every step() regardless of whether a new command just arrived --
        matching the real controller, which re-evaluates its hysteresis
        decision on a fixed tick, not only on new setpoints.
        """
        relay = self.__steering_relay.update(
            self.__target_steer_deg, self.__rack_angle_deg, time.monotonic())
        if relay == RELAY_RIGHT:
            self.__rack_angle_deg = min(MAX_STEERING_DEG, self.__rack_angle_deg + RATE_DEG_S * dt)
        elif relay == RELAY_LEFT:
            self.__rack_angle_deg = max(-MAX_STEERING_DEG, self.__rack_angle_deg - RATE_DEG_S * dt)
        # else RELAY_STOP: __rack_angle_deg unchanged.

        rack_rad = math.radians(self.__rack_angle_deg)
        if abs(rack_rad) < 1e-4:
            left = right = 0.0
        else:
            # Ackermann geometry: the inside wheel turns more than the outside.
            radius = WHEELBASE / math.tan(rack_rad)
            left = math.atan(WHEELBASE / (radius - TRACK / 2))
            right = math.atan(WHEELBASE / (radius + TRACK / 2))
        self.__steers[0].setPosition(left)
        self.__steers[1].setPosition(right)

    def __measured_speed(self):
        positions = [encoder.getValue() for encoder in self.__encoders]
        if any(math.isnan(p) for p in positions):
            return 0.0
        speed = 0.0
        if self.__last_encoder is not None:
            delta = sum(p - q for p, q in zip(positions, self.__last_encoder)) / len(positions)
            speed = delta * WHEEL_RADIUS / (self.__timestep / 1000.0)
        self.__last_encoder = positions
        return speed

    def step(self):
        rclpy.spin_once(self.__node, timeout_sec=0)

        self.__update_steering(self.__timestep / 1000.0)

        measured_speed_ms = self.__measured_speed()
        self.__speed_publisher.publish(Float32(data=float(measured_speed_ms)))
        self.__bitsauto_speed_publisher.publish(Float32(data=float(measured_speed_ms * 3.6)))

        sensor_rad = self.__steer_sensor.getValue()
        if not math.isnan(sensor_rad):
            self.__steer_angle_publisher.publish(Float32(data=float(math.degrees(sensor_rad))))

        if self.__cmd_timeout > 0.0 and self.__last_cmd_time is not None:
            age = (self.__node.get_clock().now() - self.__last_cmd_time).nanoseconds / 1e9
            if age > self.__cmd_timeout:
                for wheel in self.__wheels:
                    wheel.setVelocity(0.0)
