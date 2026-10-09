# D-005 · Calibrate camera and depth to Intel RealSense D435 specs

- **Date:** 2026-09-08 → 2026-09-09
- **Status:** Accepted

## Context
The demo used arbitrary numbers (360×240, 1 rad FOV, identical camera and
depth). The real cart carries a RealSense D435i. Matching the real hardware
rather than approximating it was an explicit, repeated priority.

## Decision
Use D435 datasheet figures: RGB 69° / 1280×720; depth 87° / 848×480 /
0.105–10 m. (The D435i's optics are the D435's; the "i" adds the IMU.)

## Consequences
- Camera and depth now differ in FOV and resolution, which made the old
  "already registered" point-cloud shortcut wrong and required
  [D-007](D-007-register-depth-with-register-node.md).
- Only the central 69° of the depth cloud has colour, like a real D435.
- The figures are Documented, not re-derived from Intel's primary PDF
  (it could not be fetched); see [realsense-d435i.md](../04-knowledge/realsense-d435i.md).
