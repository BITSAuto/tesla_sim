# D-002 · Depth from a `RangeFinder` (ground truth), not simulated stereo

- **Date:** 2026-09-08
- **Status:** Accepted

## Context
The real D435i computes depth on the device by active-stereo IR matching. The
team's Jetson world used two `Camera`s and stereo matching.

## Decision
Use Webots' `RangeFinder`, which reads the depth buffer directly.

## Alternatives considered
- **Two cameras plus stereo matching:** closer to how the sensor works, but
  reproducing its noise and dropout faithfully is a large, separate effort.
  What downstream code needs is realistic FOV, resolution and range.

## Consequences
- Depth is perfect. Perception adds D435-like noise itself
  (`traversability`'s `depth_noise` node) when testing robustness.
- Standard practice in robot simulators (Gazebo and Isaac Sim do the same).
- If a task ever needs real stereo artefacts, the stereo path is still open.
