# Unit tests

```bash
cd ~/ros2_ws/src/tesla_sim && python3 -m pytest test
```

| File | Covers |
| --- | --- |
| `test/test_longitudinal.py` (6 tests) | throttle lag towards a higher target; coasting at exactly `coast_decel`, never faster; stopping distance; the emergency brake zeroing and holding speed; reversing through zero; parameter validation |

The driver plugin and the world have no automated tests; they're verified in
the running sim (see the other pages here). Adding a headless smoke test
(launch, command 5 km/h, check GPS displacement) is a good next step.
