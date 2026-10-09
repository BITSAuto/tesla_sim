# Spawning test objects

The Ros2Supervisor can add and remove Webots nodes at runtime.

- **traversability's test scene:** `ros2 run traversability spawn_test_scene`
  (paint, newspaper, oil stain and grass patch, plus a brick, curb, box and
  barrel, 3.5–9 m ahead); remove with
  `--ros-args -p remove_only:=true`.
- **cart_driver's helper:** `python3 tools/simtools.py spawn NAME AHEAD LEFT SX SY SZ [--flat] [--color "r g b"]`
  places a box relative to the GPS (front bumper); `--flat` makes drivable
  clutter lying on the road with no physics. `simtools.py remove NAME...`
  removes it.
- **Raw service:** `/Ros2Supervisor/spawn_node_from_string`
  (`webots_ros2_msgs/srv/SpawnNodeFromString`) with a VRML string, and
  `/Ros2Supervisor/remove_node` (`std_msgs/String`) with the node's name.

**Don't spawn inside the start intersection.** Its visible surface is about
10 cm above its collision surface, so objects sink. Drive about 20 m ahead
onto `road(5)` first ([world-geometry.md](../04-knowledge/world-geometry.md)).
