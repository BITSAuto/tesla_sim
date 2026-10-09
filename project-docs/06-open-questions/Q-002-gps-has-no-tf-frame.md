# Q-002 · The GPS has no TF frame

- **Opened:** 2026-09-09 · **Status:** Open · **Priority:** low

`/vehicle/gps` uses `frame_id: gps`, which isn't connected to the TF tree.
Nothing needs it yet: `cart_driver` treats the GPS as the front-bumper point
by convention (3.79 m ahead of the rear axle). If anything ever correlates
GPS with sensor frames, add a static transform from the vehicle origin to the
GPS mount (identity rotation).
