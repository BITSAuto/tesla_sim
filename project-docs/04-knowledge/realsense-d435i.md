# Intel RealSense D435 / D435i

### Optical specs used for calibration
**Documented**: RGB 69° horizontal FOV, up to 1280×720; depth 87°
horizontal FOV, up to 848×480 native, 0.105 m minimum depth at that
resolution, 0.3–3 m "ideal" range, about 10 m usable maximum at reduced
accuracy. These are Intel's D435 datasheet figures, consistent across
sources, but Intel's own page could not be fetched from the development
network to re-check the wording.

### The D435i's IMU is a Bosch BMI055
**Verified** from Intel's `librealsense` repository, `doc/d435i.md`:
"includes a Bosch BMI055 6-axis inertial sensor".

### BMI055 range and noise
**Assumed**: the commonly cited ±4 g accelerometer and ±1000 °/s gyro ranges
are a starting point only. Intel's and Bosch's spec pages timed out from the
development network. See [Q-003](../06-open-questions/Q-003-bmi055-specs.md).

### Depth noise on the real camera
**Verified** on the 2026-10-01 campus recording (by `traversability`): the
height spread of road points grows from about ±4 cm at 0–3 m to about ±30 cm
at 8–12 m, roughly twice the σ_z = c·z² level first assumed. Details in
`traversability`'s book.

### Mount on the cart
**Verified** from the 2026-10-01 campus recording: the camera is about
**1.51–1.53 m** above the road, centred left-right, pitched about **9°**
down. tesla_sim reproduces this (reads 1.518 m, 8.6°;
[D-018](../03-decisions/D-018-camera-mount-from-campus-bag.md)).
