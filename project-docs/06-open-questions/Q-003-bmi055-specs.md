# Q-003 · Exact BMI055 range and noise specs

- **Opened:** 2026-09-09 · **Status:** Open · **Priority:** low

The simulated IMU is noise-free with unbounded range. The commonly cited
±4 g and ±1000 °/s are unconfirmed: Intel's and Bosch's spec pages timed out
from the development network (GitHub worked). Fetch the BMI055 datasheet from
another network if a fusion filter is ever tuned to match real noise.
