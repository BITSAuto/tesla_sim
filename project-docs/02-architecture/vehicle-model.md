# Vehicle model

The car is meant to behave like the cart, not like a Tesla. Three parts do
that: the longitudinal model, the emergency brake and relay steering.

## Speed: throttle and coasting (`longitudinal.py`)

| Situation | Behaviour |
| --- | --- |
| commanded speed above current | first-order lag towards it, time constant `driveTimeConstant` (1 s) |
| commanded speed below current, or 0 | throttle released: speed falls at `coastDecel` (0.4 m/s²), never faster |
| `cmdTimeout` expired | coast (as if 0 were commanded) |
| direction change | coasts through zero first |
| emergency brake held | speed is 0 immediately and stays 0 |

The model's speed sets both rear-wheel velocities (`speed / 0.36 m`). The
published speed is measured independently from the wheel position sensors,
so wheel slip or a wedged car shows up as a mismatch.

Measured in sim time on 2026-10-08 (see
[09-testing-and-results/longitudinal-and-brake.md](../09-testing-and-results/longitudinal-and-brake.md)):
lag τ = 1.00 s; coasting at 0.40 m/s² rolls 2.41 m from 5 km/h in 3.35 s;
the emergency brake stops the car from about 5 km/h in about 0.25 s (the
wheels lock instantly and the body skids briefly).

Why: [D-015](../03-decisions/D-015-cart-like-longitudinal-model.md) and
[D-016](../03-decisions/D-016-emergency-brake-is-the-only-brake.md).

## Steering: the relay

The real cart's steering motor only accepts left, stop or right, and keeps
turning until told to stop. tesla_sim runs the same
`RelaySteeringController` as `vehicle_bridge`:

1. Every step, the controller compares the target angle with the current
   **rack (bicycle-model) angle** and returns left, stop or right, with
   hysteresis and a minimum hold of 35 ms.
2. The rack angle moves at `RATE_DEG_S` (≈12.86 °/s, from the real motor's
   0.45° per 35 ms pulse) while the relay is on, clamped to ±15°.
3. Ackermann geometry turns the rack angle into the two wheel angles (the
   inner wheel turns more), using wheelbase 2.94 m and track 1.72 m.
4. `/steering/angle` publishes the **left wheel's** measured angle, like the
   real encoder.

The controller compares against the rack angle, not the measured wheel
angle, because the inner and outer wheels differ from the rack angle by a
turn-direction-dependent amount. Comparing against a wheel angle would bias
the hysteresis ([vehicle-model-facts.md](../04-knowledge/vehicle-model-facts.md#wheel-angles-vs-rack-angle)).

Going from straight to full lock takes about 1.2 s, or about 1.6 m of travel
at 5 km/h. A step change in the command ramps; this is intentional.

Why: [D-010](../03-decisions/D-010-relay-steering-shared-with-vehicle-bridge.md),
[D-017](../03-decisions/D-017-clamp-steering-to-15-degrees.md).
