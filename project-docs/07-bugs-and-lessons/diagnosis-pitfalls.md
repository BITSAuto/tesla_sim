# Diagnosis pitfalls

## M-10: "Wedged against a building" reused for an unrelated report
- **Found:** 2026-09-08
- **What happened:** once, `/vehicle/speed` read 30.7 m/s with GPS frozen:
  the car was wedged against a building with its wheels spinning. Later
  "commands do nothing" reports were read the same way. The owner pushed
  back ("it is not wedged right now") and was right: speed read 0.0 and a
  live listener showed **no messages arriving** on the command topic. The
  cause was the domain/DDS confusion (M-08).
- **Rule:** two "car isn't moving" reports can have unrelated causes. First
  check whether commands are arriving at all.

## M-11: A black `scrot` screenshot nearly counted as evidence
- **Found:** 2026-09-09
- **What happened:** checking a "black window" report, `scrot` returned a
  black image. `scrot` can't capture Wayland windows, so the image proved
  nothing. Pixel statistics of a live image message (`min=12, max=255,
  mean=121`) showed the data was fine.
- **Rule:** confirm a tool can see what you're checking. Separate "is the
  data good" from "is the display broken".

## M-12: Anchored `pgrep` made a running process look absent
- **Found:** 2026-09-09
- **What happened:** `pgrep -af "rviz2$"` found nothing because RViz's
  command line has trailing arguments.
- **Rule:** don't anchor `pgrep -f` patterns without checking the full
  command line.

## Verification method that worked: GPS displacement over time
Several false leads came from trusting one instantaneous speed reading. What
worked every time: sample the GPS position, hold a command for N seconds,
sample again, compute the displacement (e.g. about 38 m in 10 s at a
commanded 15 km/h; negative displacement in reverse; a curving track when
steering).
