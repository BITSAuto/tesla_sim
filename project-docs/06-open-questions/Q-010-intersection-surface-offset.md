# Q-010 · Intersection surfaces sit 10 cm above their collision surface

- **Opened:** 2026-10-02 · **Status:** Open (worked around) · **Priority:** low

Objects spawned inside a `RoadIntersection` sink, thin patches vanish, and
depth sees a 12 cm visual step about 8 m ahead of the start
([world-geometry.md](../04-knowledge/world-geometry.md#surface-quirks)).
Tests drive about 20 m onto a plain road first. A fix would adjust the
intersection's `translation` z or its collision geometry, then re-check that
`cart_driver` and `traversability` see no false step at junctions.
