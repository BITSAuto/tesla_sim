# Roadmap

Nothing is scheduled; these are the known next steps, roughly by value.

| Item | Why | Depends on |
| --- | --- | --- |
| Set `coastDecel` and the body dimensions to the real cart's | Stopping distances and turning in sim should match the cart | Measurements on the cart ([Q-007](../06-open-questions/Q-007-cart-dimensions-and-coast-rate.md)) |
| Merge or drop the multi-instance `port` change | Running two sims side by side | Its owner ([Q-008](../06-open-questions/Q-008-owner-of-the-port-change.md)) |
| A cart-shaped vehicle instead of the Tesla body | Footprint and turning radius would match | Cart dimensions |
| GPS TF frame and optional GPS noise | Route following and localisation tests closer to reality | [Q-002](../06-open-questions/Q-002-gps-has-no-tf-frame.md) |
| Pedestrians and moving obstacles | Safety tests for `cart_driver` | — |
| Stamp sensors with sim time | Removes the wall-clock/sim-time mapping everywhere | [Q-009](../06-open-questions/Q-009-sensor-stamps-are-wall-clock.md) |
| Optional IMU noise and range | Fusion filters tuned in sim would transfer | [Q-003](../06-open-questions/Q-003-bmi055-specs.md) |
