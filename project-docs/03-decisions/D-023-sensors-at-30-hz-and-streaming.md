# D-023 · Camera and depth at 30 Hz; optional web streaming

- **Date:** 2026-10-10 (Orin session); committed 2026-10-15
- **Status:** Accepted

- `updateRate 30` on the camera and range finder in `tesla.urdf`, the D435's
  frame rate. They were rendered every 10 ms step (100 Hz), three times more
  than the real camera and very slow on software-rendered displays.
- `TESLA_SIM_STREAM=1` starts Webots' web streaming server (W3D, port 1234),
  so the 3D view can be watched in a browser on another machine instead of a
  slow forwarded X display.
