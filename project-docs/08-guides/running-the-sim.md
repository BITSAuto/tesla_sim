# Running the sim

## Start and stop
```bash
distrobox enter ubuntu22 -- ~/ros2_ws/scripts/run_tesla_sim.sh
distrobox enter ubuntu22 -- ~/ros2_ws/scripts/run_tesla_sim.sh autonomous:=true rviz:=true
~/ros2_ws/scripts/stop_tesla_sim.sh
```
On a native setup use `~/ros2_ws/src/tesla_sim/scripts/run_tesla_sim.sh`.

- **Always stop with `stop_tesla_sim.sh`.** It SIGINTs the launch, which
  shuts down every node cleanly. Closing the terminal or killing nodes one by
  one leaves orphans that hold DDS slots. Run the stop script as its own
  command: a `pkill -f` pattern that appears in your own command line kills
  your shell.
- **Domains:** the script uses your shell's `ROS_DOMAIN_ID` and
  `CYCLONEDDS_URI` ([D-004](../03-decisions/D-004-do-not-hardcode-ros-domain-id.md)).
  Export the same values in every terminal that talks to the sim. Prefer a
  domain no other ROS graph uses.
- **Starting from a script:** a background job (`cmd &`) in a
  non-interactive shell ignores SIGINT; wrap it so SIGINT is restored, or
  the launch can't be stopped cleanly.

Launch arguments: `world`, `pointcloud`, `colored`, `autonomous`, `rviz`
([interfaces.md](../02-architecture/interfaces.md#launch-arguments-tesla_simlaunchpy)).

## With perception and the driving stack
In a second terminal on the same domain, inside the distrobox with the
workspace sourced:
```bash
ros2 launch traversability traversability.launch.py semantics:=true      # perception only
ros2 launch cart_driver sim.launch.py                                    # perception + safety + driver
```
`cart_driver`'s launch uses the sim-trained RGB-D student by default. See the
`traversability` and `cart_driver` books for details.

## Restarting from the start pose
There is no reset service in use; stop the sim and start it again to put the
car back at the start pose. `cart_driver`'s emergency brake is latched until
the car is stopped and `~/reset` is called.

## Expect
- Webots runs at about 0.55× real time with perception running.
- Perception takes a minute or two to load models before
  `/traversability/grid` appears.
