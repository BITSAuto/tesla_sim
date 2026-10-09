# D-007 · Register depth to colour with `depth_image_proc register_node`

- **Date:** 2026-09-09
- **Status:** Accepted

## Context
After [D-005](D-005-calibrate-sensors-to-d435.md), camera and depth no longer
share FOV and resolution. The point-cloud pipeline assumed pixel-for-pixel
correspondence and silently produced a wrong coloured cloud.

## Decision
Insert `register_node` before `point_cloud_xyzrgb_node`. It reprojects depth
into the colour camera's framing (`/vehicle/range_finder/image_registered`).

## Consequences
- Same architecture as the real RealSense SDK's `align_depth`.
- Needed a real TF between the two optical frames, hence the four static
  transforms and the optical/body frame split
  ([frames-and-conventions.md](../02-architecture/frames-and-conventions.md)).
- `traversability` uses the registered depth for RGB-D models.
