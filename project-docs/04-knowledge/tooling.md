# Tooling

### Build with `PYTHONNOUSERSITE=1`
**Verified**: a newer `setuptools` in `~/.local` shadows the system one and
breaks `ament_python` builds (`canonicalize_version() got an unexpected
keyword argument`, or `error: option --uninstall not recognized` from
`setup.py develop`). `PYTHONNOUSERSITE=1 colcon build --symlink-install ...`
works.

### `scrot` can't capture Wayland windows
**Verified**: the desktop session is Wayland; `scrot` uses X11 grab APIs and
returns a black image for Wayland-native windows. Use `gnome-screenshot`, or
better, read the data (pixel statistics of a live image message).

### Anchored `pgrep` patterns miss real processes
**Verified**: `pgrep -af "rviz2$"` missed RViz because its command line has
trailing arguments. Don't anchor with `$` without checking the full command
line.

### RViz hides QoS mismatches
**Verified**: a display with incompatible QoS shows as subscribed with no
data; the only signal is a stderr line about an incompatible QoS offer.
`depth_image_proc`'s coloured cloud is best-effort; the image topics are
reliable. Check each topic with `ros2 topic info -v`; don't blanket-switch
everything to best-effort.
