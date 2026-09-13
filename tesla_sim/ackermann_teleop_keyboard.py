#!/usr/bin/env python3
"""Keyboard teleop publishing ackermann_msgs/AckermannDrive on /cmd_ackermann.

Modeled on ros-humble-teleop-twist-keyboard, but emits Ackermann directly
instead of Twist, for stacks (like the Jetson's stereo_driving, or tesla_sim's
own driver) that expect steering angle + speed-in-km/h rather than a Twist.

Keys:
  w/s   increase/decrease speed (km/h)
  a/d   steer left/right
  space steering to centre
  x     stop (speed to 0, steering held)
  q     quit
Speed and steering step size scale with +/- (shift of w/s a/d is not used to
keep this to a plain terminal, no curses).
"""
import sys
import termios
import tty

import rclpy
from ackermann_msgs.msg import AckermannDrive
from rclpy.node import Node

MAX_STEERING_ANGLE = 0.5  # rad, matches tesla_driver.py's clamp

INSTRUCTIONS = """
Ackermann keyboard teleop -- publishing on /cmd_ackermann
---------------------------------------------------------
   w        increase speed (km/h)
a  s  d     steer left / decrease speed / steer right
space       centre steering
x           stop (speed -> 0)
+ / -       change step size
q           quit
CTRL-C to quit
"""

MOVE_BINDINGS = {
    'w': (1, 0),
    's': (-1, 0),
    'a': (0, -1),
    'd': (0, 1),
    'x': (0, 0),
}


def get_key(settings):
    tty.setraw(sys.stdin.fileno())
    key = sys.stdin.read(1)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key


def main():
    settings = termios.tcgetattr(sys.stdin)
    rclpy.init()
    node = Node('ackermann_teleop_keyboard')
    pub = node.create_publisher(AckermannDrive, 'cmd_ackermann', 1)

    speed = 0.0
    steering = 0.0
    speed_step = 5.0     # km/h per keypress
    steering_step = 0.05  # rad per keypress

    print(INSTRUCTIONS)
    try:
        while True:
            key = get_key(settings)
            if key == 'q' or key == '\x03':
                break
            elif key == '+':
                speed_step *= 1.5
                steering_step = min(MAX_STEERING_ANGLE, steering_step * 1.5)
            elif key == '-':
                speed_step /= 1.5
                steering_step /= 1.5
            elif key == ' ':
                steering = 0.0
            elif key == 'x':
                speed = 0.0
            elif key in MOVE_BINDINGS:
                d_speed, d_steer = MOVE_BINDINGS[key]
                speed += d_speed * speed_step
                steering = max(-MAX_STEERING_ANGLE,
                               min(MAX_STEERING_ANGLE, steering + d_steer * steering_step))

            msg = AckermannDrive()
            msg.speed = speed
            msg.steering_angle = steering
            pub.publish(msg)
            print(f'\rspeed={speed:6.1f} km/h  steering={steering:+.2f} rad  '
                  f'(step {speed_step:.1f} km/h / {steering_step:.2f} rad)   ', end='', flush=True)
    finally:
        msg = AckermannDrive()
        msg.speed = 0.0
        msg.steering_angle = steering
        pub.publish(msg)
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
        node.destroy_node()
        rclpy.shutdown()
        print()


if __name__ == '__main__':
    main()
