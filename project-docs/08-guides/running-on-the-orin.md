# Running on the Orin (`~/BITSAuto_All_repo`, Jazzy)

```bash
export ROS_DOMAIN_ID=23          # your own domain; export it, don't prefix the source command
source ~/BITSAuto_All_repo/env.sh
$BITSAUTO_HOME/ros2_ws/src/tesla_sim/scripts/run_tesla_sim.sh                         # tesla_city
$BITSAUTO_HOME/ros2_ws/src/tesla_sim/scripts/run_tesla_sim.sh world:=road_loop.wbt    # narrow road with curbs
```

- **No monitor:** run headless with `WEBOTS_OFFSCREEN=1` and `DISPLAY`
  unset (Webots runs under `xvfb-run`; ~0.3× real time because the sensors are
  rendered without the GPU). With a monitor or dummy plug, `DISPLAY=:1` uses
  the GPU.
- **Watching from a laptop:** start with `TESLA_SIM_STREAM=1`, serve Webots'
  viewer page (`$WEBOTS_HOME/resources/web/streaming_viewer`) with
  `python3 -m http.server 8000`, then on the laptop
  `ssh -N -L 8000:localhost:8000 -L 1234:localhost:1234 bitsauto@bitsauto-orin`
  and open `http://localhost:8000` → Connect. A direct `ws://bitsauto-orin:1234`
  failed from the laptop; the tunnel works.
- **One Webots at a time** on this machine; check `pgrep -a webots` first and
  stop what you start (Ctrl-C in its terminal). Start background launches so
  that SIGINT still works, or stop them by PID.
- The workspace's checkout must be a git branch, not uncommitted edits (M-18).
