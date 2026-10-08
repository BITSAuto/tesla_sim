"""Longitudinal (speed) model of the real cart, for the simulated vehicle.

The cart has no proportional braking: its brake stops it instantly and can
damage it, so it is reserved for emergencies. In normal driving, speed is
controlled by throttle alone, and the only way to slow down is to give less
throttle and let friction do the work. This model reproduces that:

  * throttle on (target speed above current): speed rises towards the target
    with a first-order lag (``drive_time_constant``) -- the throttle is
    open-loop on the real cart, so it doesn't arrive instantly either
  * throttle reduced or off (target below current, or 0): speed can only fall
    at the coast deceleration (``coast_decel``), never faster
  * emergency brake: speed goes to zero immediately and stays there while the
    brake is held

Speeds are signed (negative = reverse); a change of direction coasts through
zero first. Pure Python, no Webots or ROS dependency.
"""

import math


class LongitudinalModel:
    def __init__(self, drive_time_constant=1.0, coast_decel=0.4):
        if drive_time_constant <= 0 or coast_decel <= 0:
            raise ValueError('drive_time_constant and coast_decel must be positive')
        self.drive_time_constant = drive_time_constant
        self.coast_decel = coast_decel
        self.speed = 0.0          # m/s, signed

    def update(self, target, dt, brake=False):
        """Advance by ``dt`` seconds towards ``target`` (m/s, signed)."""
        if brake:
            self.speed = 0.0
            return self.speed
        coasting = (target == 0.0 or abs(target) < abs(self.speed) or
                    math.copysign(1.0, target) != math.copysign(1.0, self.speed) and self.speed != 0.0)
        if coasting:
            # Friction only: shrink |speed| towards |target| (or 0 if the
            # target is the other way), at no more than coast_decel.
            floor = abs(target) if math.copysign(1.0, target) == math.copysign(1.0, self.speed) else 0.0
            magnitude = max(floor, abs(self.speed) - self.coast_decel * dt)
            self.speed = math.copysign(magnitude, self.speed)
        else:
            alpha = min(1.0, dt / self.drive_time_constant)
            self.speed += (target - self.speed) * alpha
        return self.speed

    def coast_distance(self, speed=None):
        """Distance (m) to roll to a stop from ``speed`` (default: current)."""
        v = abs(self.speed if speed is None else speed)
        return v * v / (2.0 * self.coast_decel)
