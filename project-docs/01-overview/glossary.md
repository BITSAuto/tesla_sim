# Glossary

| Term | Meaning |
| --- | --- |
| **Cart** | The BITSAuto campus golf cart, the real vehicle this simulator imitates |
| **Digital clone** | This simulator's goal: behave like the cart closely enough that code tuned here works there |
| **Relay steering** | The cart's steering motor only accepts left / stop / right (`49`/`50`/`51`) and keeps turning until told to stop; angle control is done in software from an encoder reading |
| **Hysteresis controller** | `RelaySteeringController` in vehicle_bridge: turns the relay on when the angle error is large, off when small, with a minimum hold time |
| **Rack angle / bicycle-model angle** | The single steering angle of a bicycle model; the inner and outer wheels turn by different amounts around it (Ackermann geometry) |
| **Coast / coasting** | Throttle released (byte 50 on the real cart); friction slows the vehicle |
| **Emergency brake (e-brake)** | `/vehicle/emergency_brake`; stops instantly; emergency use only |
| **`coastDecel`** | Deceleration while coasting, 0.4 m/s² (placeholder) |
| **`driveTimeConstant`** | First-order lag of the throttle response, 1 s |
| **`cmdTimeout`** | Dead-man timer: with no command for this long, the car coasts |
| **RangeFinder** | Webots depth sensor reading its own depth buffer (ground truth) |
| **Optical frame** | Camera convention X right, Y down, Z forward; ROS body frames are X forward, Y left, Z up |
| **RTF** | Real-time factor: sim seconds per wall second (about 0.55 here) |
| **PROTO** | Webots' reusable node definitions (e.g. `TeslaModel3`), fetched from GitHub |
| **Participant index** | CycloneDDS's per-process slot on a domain; running out of them stops nodes starting |
| **D435i** | Intel RealSense depth camera with an IMU; the cart's camera |
| **BMI055** | The Bosch 6-axis IMU inside the D435i |
| **Orin** | Nvidia Jetson Orin AGX on the cart |
