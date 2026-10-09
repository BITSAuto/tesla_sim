# D-013 · tesla_sim becomes its own repository

- **Date:** 2026-09-13
- **Status:** Accepted

## Context
tesla_sim started untracked inside the developer's `~/ros2_ws` workspace
repository, which has no remote. Other team packages
(`cart_contorller`, `road_segmentation`) are separate repositories cloned into
the workspace.

## Decision
Publish it as [BITSAuto/tesla_sim](https://github.com/BITSAuto/tesla_sim)
(public), alongside [BITSAuto/vehicle_bridge](https://github.com/BITSAuto/vehicle_bridge).

## Consequences
- Changes go through branches and PRs.
- Resolved the earlier open question about spinning it out.
