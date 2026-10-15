# D-022 · Registered depth in its own namespace

- **Date:** 2026-10-15
- **Status:** Accepted

The registered depth image moved from `/vehicle/range_finder/image_registered`
to `/vehicle/range_finder_registered/image` (camera info
`/vehicle/range_finder_registered/camera_info`). On Jazzy the register node's
camera info goes next to its image topic whatever the remap says, so the old
name put the colour camera's intrinsics on `/vehicle/range_finder/camera_info`
([jazzy-and-orin-bugs.md](../07-bugs-and-lessons/jazzy-and-orin-bugs.md)).
Consumers (traversability's sim config) moved in a matching PR.
