# Jazzy and Orin bugs

## M-17: Colour camera intrinsics on the depth camera_info topic (Jazzy)
- **Found:** 2026-10-15, running cart_driver on the Orin.
- **Symptom:** `/vehicle/range_finder/camera_info` had two publishers (the
  driver with 848×480, `register_depth` with the colour camera's 1280×720).
  traversability's `ground_geometry` alternated between labelling the whole
  road ground and the whole road a drop; cart_driver emergency-braked at the
  start and then stayed blocked.
- **Root cause:** on Jazzy, `depth_image_proc`'s register node publishes the
  registered image's camera info next to the image topic, ignoring the
  `depth_registered/camera_info` remap. The image was at
  `/vehicle/range_finder/image_registered`, so its info went to
  `/vehicle/range_finder/camera_info`. Humble honours the remap, so laptop
  tests passed.
- **Fix:** registered depth in its own namespace
  ([D-022](../03-decisions/D-022-registered-depth-own-namespace.md)).
- **Rule:** after remapping image topics, check each `camera_info` topic has
  exactly one publisher (`ros2 topic info`) on every ROS distro you run.

## M-18: The Orin's tesla_sim fell behind main
- **Found:** 2026-10-15.
- **What:** the Orin workspace was at `0785d4f` (2026-10-06) plus another
  session's uncommitted changes, so it lacked coasting, the emergency-brake
  topic, ±15° steering and the real camera mount. cart_driver runs there
  weren't against the cart-like sim.
- **Fix:** that session's changes committed and merged with main; the Orin
  checks out the result.
- **Rule:** keep shared machines on a branch from git, never on uncommitted
  edits; check `git status`/`git log` there before trusting a result.
