# 2026-10-15 · Orin / Jazzy support

**Who:** project owner, with Claude Code
**Branch:** `feat/orin-jazzy-support`

## What was done
- Running cart_driver on the Orin: the car braked at the start and stayed
  blocked. Traced to `/vehicle/range_finder/camera_info` carrying the colour
  camera's intrinsics on Jazzy (M-17); fixed by moving the registered depth to
  its own namespace (D-022).
- Found the Orin's tesla_sim at an old commit plus uncommitted work from the
  road_follower session (M-18). Committed that work (raw relay input, 30 Hz
  sensors, streaming, paths; D-021, D-023), merged with main, and added
  `road_loop.wbt` with the real camera mount (D-024).
