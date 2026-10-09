# 2026-10-08 · Make the sim behave like the cart

**Who:** project owner, with Claude Code
**Branch / PR:** `feat/cart-fidelity`, [PR #1](https://github.com/BITSAuto/tesla_sim/pull/1) (merged as `e9e33dd`)
**Goal:** step 1 of the driving plan: coasting instead of instant stops, an emergency-only brake, ±15° steering, the real camera mount.

## What was done
- `longitudinal.py` + 6 tests; `/vehicle/emergency_brake`; `maxSteeringDeg`;
  sensors moved to the bag-measured mount; crossings lowered.
- Fixed the brake-release crash (M-13); learned to measure on sim time (M-14);
  traced a false start-line e-brake to the crossings (M-15).

## Results
- [longitudinal-and-brake.md](../09-testing-and-results/longitudinal-and-brake.md).

## Decisions, facts, questions and bugs recorded
- D-015 to D-019; Q-007, Q-008, Q-009; M-13 to M-15; world geometry and time-stamp facts.

## Left for next time
- Real `coastDecel` and cart dimensions (Q-007).
