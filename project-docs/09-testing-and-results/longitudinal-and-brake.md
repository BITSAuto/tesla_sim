# Longitudinal model and emergency brake (2026-10-08)

Measured in the running sim on **sim time** (`use_sim_time`), for
[PR #1](https://github.com/BITSAuto/tesla_sim/pull/1). Timing in wall-clock
seconds gives wrong numbers (M-14).

| Check | Expected | Measured |
| --- | --- | --- |
| Throttle lag to 5 km/h | τ = 1 s | 63 % of 5 km/h at **1.00 s**; holds **4.99 km/h** |
| Coast from 5 km/h (throttle released) | 0.4 m/s², ~2.4 m | **0.40 m/s²**, stopped in **3.35 s** after **2.41 m** |
| Emergency brake at ~5 km/h | instant | stopped from 4.9 km/h in **≈0.25 s** (wheels lock instantly; the body skids briefly); held while throttle was still commanded |
| Steering clamp | ±15° | about ±15° on `/steering/angle` |
| Camera mount | 1.52 m, 9° down | ground-plane fit reads **1.518 m**, **8.6°** |
| Brake release | no crash | fixed after M-13; engage and release both logged |
