# Results other repos measured in this sim

Details live in each repo's book; this is a pointer list.

| Date | Repo | Result |
| --- | --- | --- |
| 2026-10-02 | traversability | Phase 1 geometry test scene: flat objects 4/4 free, obstacles 4/4 lethal, 0 false lethal (perfect and D435-like noisy depth) |
| 2026-10-06 | traversability | Phase 2 fused test scene with SegFormer-B0/B2 and Mask2Former; phase 3 student trained on 480 sim frames |
| 2026-10-08 | cart_driver | Step 2: speed held at 5.13 km/h; stale perception → coasted, 0 brakes; box in lane → e-brake at 3.2 m, stopped 3.4 m short |
| 2026-10-08 | cart_driver | Step 3: memory map kept a box 8.7 m behind the car within 0.01 m; odometry drift 0.02 m over 20.9 m |
| 2026-10-08 | cart_driver | Step 4: swerved around a box with 0.49 m clearance; drove over flat clutter; late box → e-brake, stopped 2.54 m short |
| 2026-10-08 | cart_driver | Step 5: 584 m loop (more than a lap) at 5.00 km/h, 0 brakes, 0.31 m mean from the route |
