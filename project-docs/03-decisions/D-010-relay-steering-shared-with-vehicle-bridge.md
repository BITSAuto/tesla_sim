# D-010 · Simulate the relay steering, using the same class as the real bridge

- **Date:** 2026-09-09
- **Status:** Accepted

## Context
The real cart has no proportional steering: a three-state relay (`49` left,
`50` stop, `51` right) with "infinite run-on" (it keeps turning until told
to stop). Closed-loop angle control is done in software from an encoder.
tesla_sim originally steered instantly. The owner's framing: simulate "how
the vehicle actually works", and convert Ackermann commands to 49/50/51
"taking into account the readings of a rotary encoder".

## Decision
- A new package, `vehicle_bridge`, holds the real serial bridge and a shared
  `RelaySteeringController` (hysteresis, 35 ms minimum hold, about
  12.86 °/s).
- tesla_sim's driver imports that same class and applies it to the Webots
  steering motors, with the rack angle as the "encoder".

## Alternatives considered
- **Keep the sim continuous and discretise only in the real bridge:**
  rejected. The sim would be an easier target than the cart, and a
  controller tuned in sim would never see the real step response.
- **Each side implements its own hysteresis:** rejected. They would drift
  apart; one shared class makes parity a property of the import graph.

## Consequences
- tesla_sim depends on vehicle_bridge (it must be in the same workspace).
- Steering geometry moved into `step()`: the relay is re-evaluated every
  tick, like the real controller, not only when a command arrives.
- Changing the shared class changes the real cart's behaviour too. Don't tune
  sim-only behaviour into it.
- The rate comes from real hardware constants
  ([vehicle-model-facts.md](../04-knowledge/vehicle-model-facts.md#relay-steering-rate)).
