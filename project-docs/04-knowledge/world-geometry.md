# tesla_city world geometry

All **Verified** from `worlds/tesla_city.wbt` and runs in the sim
(2026-10-02 to 2026-10-08).

### Road layout
- Every road is 21.5 m wide with **4 lanes of 5.375 m** (2 each way), with
  barriers along the road edges.
- The roads form two overlapping rounded-rectangle loops that share two
  `RoadIntersection`s, at (45, 45) and (−45, −45) (each rotated 45°).
- **Loop A** (the one `cart_driver` drives): centre line x ∈ [−45, 105],
  y ∈ [−105, 45], corner radius 40.5 m, corner centres (−4.5, 4.5),
  (−4.5, −64.5), (64.5, −64.5), (64.5, 4.5). Centre-line length about
  530 m.
- **Loop B:** x ∈ [−105, 45], y ∈ [−45, 105], same radius.
- Lane centres sit 2.69 m (inner) and 8.06 m (kerb-side) from the centre
  line. Driving loop A anticlockwise, the kerb-side left lane is a 480 m loop
  with 32.4 m corner radius.
- A recording made by following the yellow centre line matched this geometry
  to 0.24 m on average, but drifted up to 1.7 m at junctions where the line
  is missing.

### Start pose
The car's rear axle spawns at (31.44, 47.01), yaw π (heading −x), on
`road(5)` (y = 45) just west of the (45, 45) intersection. The GPS (front
bumper) reads about (27.66, 47.01): 2 m right of the centre line, i.e. in an
oncoming-traffic lane under keep-left rules.

### Surface quirks
- **Intersections:** a `RoadIntersection`'s visible surface sits about
  **10 cm above its collision surface**. Objects spawned there sink, thin
  patches vanish, and there is a **12 cm visual step** about 8 m ahead of the
  start. Tests that spawn objects first drive about 20 m onto `road(5)`.
- **Road segments:** collision surface about 2 cm below the visible one.
- **Pedestrian crossings** were visual-only slabs about 0.095 m proud of the
  road until [D-019](../03-decisions/D-019-lower-pedestrian-crossings.md)
  lowered them.
- **No holes:** Webots roads can't have holes cut in them, so drops and
  potholes can't be tested.
