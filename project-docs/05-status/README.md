# 05 · Status

Where tesla_sim stands. Update these pages with every piece of work.

| Page | Contents |
| --- | --- |
| [completed.md](completed.md) | Everything finished, with dates, PRs and commits |
| [in-progress.md](in-progress.md) | Work started but not merged, and who owns it |
| [roadmap.md](roadmap.md) | What's planned next and what it depends on |

## Snapshot (2026-10-09)

- **State:** usable digital clone of the cart. `main` = `e9e33dd`
  (PR #1 merged 2026-10-08).
- **Used by:** `traversability` (sim tests, training data) and `cart_driver`
  (all driving tests, including a full 584 m loop with 0 brakes).
- **Open work:** an uncommitted multi-instance `port` launch argument
  ([in-progress.md](in-progress.md)).
- **Biggest unknowns:** the cart's dimensions and coast rate
  ([Q-007](../06-open-questions/Q-007-cart-dimensions-and-coast-rate.md));
  intermittent DDS start-up failures
  ([Q-001](../06-open-questions/Q-001-dds-participant-index-failures.md)).
