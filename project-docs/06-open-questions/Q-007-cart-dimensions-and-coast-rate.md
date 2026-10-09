# Q-007 · The cart's dimensions and coasting deceleration

- **Opened:** 2026-10-08 · **Status:** Open · **Priority:** high (before real-cart driving)

## What is unknown
- **Dimensions:** wheelbase, width, length, overhangs. The owner will supply
  them. Until then the sim body is a Tesla (2.94 m wheelbase), and
  `cart_driver`'s `cart` profile uses placeholders.
- **Coast deceleration:** `coastDecel` is 0.4 m/s² (about 2.4 m from 5 km/h),
  a guess. It sets `cart_driver`'s emergency-brake threshold.
- **Steering lock:** ±15° comes from `cart_controller`'s software limit, not
  a measurement (see vehicle_bridge's book).

## How to resolve
Measure on the cart: tape-measure the dimensions; for the coast rate, hold
5 km/h on a flat road, release the throttle, and time the roll-out over
marked distances (phone video works). Then update `resource/tesla.urdf`,
`cart_driver`'s profile and config, and this page.
