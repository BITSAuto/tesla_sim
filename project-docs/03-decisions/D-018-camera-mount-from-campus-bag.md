# D-018 · Mount the sensors where the cart's camera is, measured from the campus bag

- **Date:** 2026-10-08
- **Status:** Accepted ([PR #1](https://github.com/BITSAuto/tesla_sim/pull/1))

## Context
The owner asked for the camera height to be taken from the 2026-10-01 campus
recording, centred on the vehicle. Processing that bag with
`traversability`'s ground-plane fit gave a camera 1.51–1.53 m above the road,
pitched about 9° down.

## Decision
Move the camera, range finder, accelerometer and gyro to
`translation -2.12 0 1.115`, `rotation 0 1 0 0.157` in the front sensor slot.
The sim reads 1.518 m and 8.6° down afterwards.

## Consequences
- The bonnet hides the road out to about 2.7 m; perception sees about
  2.7–10 m ahead. Perception and stopping distances now transfer to the cart.
- `traversability`'s sim config needed its bonnet mask to match.
