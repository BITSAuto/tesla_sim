# D-011 · Publish `/steering/angle` and `/bitsauto/speed` under the real cart's names

- **Date:** 2026-09-09
- **Status:** Accepted

## Context
Real-cart control scripts (`road_segmentation/rotary_encoder_driver.py`)
subscribe to the global topics `/steering/angle` (degrees, + right) and
`/bitsauto/speed` (km/h). The owner's guidance: if these are the same values
the sim already has, "just rename".

## Decision
tesla_sim publishes the measured steering angle and speed under exactly those
absolute names, not under `/vehicle/...` like its other topics.

## Consequences
- Control code written for the real cart runs against the sim unchanged.
- Running the sim and the real cart's publishers on one ROS domain would
  collide. That is intended: run one vehicle at a time.
