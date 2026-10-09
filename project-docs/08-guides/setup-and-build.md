# Setup and build

## Laptop: Humble in the `ubuntu22` distrobox, snap Webots
1. Install Webots R2025a on the host as a snap.
2. Inside the distrobox, install `ros-humble-webots-ros2`,
   `ros-humble-ackermann-msgs`, `ros-humble-depth-image-proc`,
   `ros-humble-rviz2` and `ros-humble-rmw-cyclonedds-cpp`.
3. Clone both repos into the workspace (tesla_sim imports vehicle_bridge):
   ```bash
   cd ~/ros2_ws/src
   git clone https://github.com/BITSAuto/tesla_sim.git
   git clone https://github.com/BITSAuto/vehicle_bridge.git
   ```
4. Build inside the distrobox. `PYTHONNOUSERSITE=1` avoids a newer
   `setuptools` in `~/.local` breaking `ament_python`:
   ```bash
   cd ~/ros2_ws && PYTHONNOUSERSITE=1 colcon build --symlink-install --packages-select vehicle_bridge tesla_sim
   ```

## Native Ubuntu 24.04 / Jazzy (e.g. the Orin)
```bash
sudo apt install ros-jazzy-webots-ros2 ros-jazzy-ackermann-msgs ros-jazzy-depth-image-proc ros-jazzy-rviz2
```
Build Webots from source into `$HOME/webots` (no arm64 snap exists), then
clone and build as above. `scripts/run_tesla_sim.sh` detects the source build
and sets `QT_PLUGIN_PATH` if Webots was linked against the system Qt6.
Set `TESLA_SIM_WS` if the workspace isn't `~/ros2_ws`.

## Tests
```bash
cd ~/ros2_ws/src/tesla_sim && python3 -m pytest test
```
