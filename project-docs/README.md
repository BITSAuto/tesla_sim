# tesla_sim · Project docs

The shared engineering record for **tesla_sim**, the Webots digital clone of
the BITSAuto cart. Everything someone joining the project needs to know is
meant to be findable from here: what exists, why it is the way it is, what
is finished, what is in progress and what is still unknown.

This book is organised in chapters (directories). Each chapter has a
`README.md` listing its pages. The usage summary is the repo's top-level
[README](../README.md); this book holds the depth.

## Start here

| If you are... | Read |
| --- | --- |
| new to the project | [01-overview](01-overview/README.md), then [05-status](05-status/README.md) |
| about to change code | the [decisions](03-decisions/README.md) and [bugs-and-lessons](07-bugs-and-lessons/README.md) for that area, and the relevant [open questions](06-open-questions/README.md) |
| trying to run something | [08-guides](08-guides/README.md) |
| an AI agent | [AGENTS.md](../AGENTS.md), then this page |

## Status at a glance (2026-10-09)

Working digital clone of the cart: coast-only speed, emergency-only brake,
relay steering at ±15°, D435i sensors at the real mount. Used by
`traversability` and `cart_driver` for all simulation testing. Main unknowns:
the cart's dimensions and coast rate. Details: [05-status](05-status/README.md).

## Contents

1. **[Overview](01-overview/README.md)** —
   [project brief](01-overview/project-brief.md) ·
   [system map](01-overview/system-map.md) ·
   [hardware and environment](01-overview/hardware-and-environment.md) ·
   [glossary](01-overview/glossary.md)
2. **[Architecture](02-architecture/README.md)** —
   [components](02-architecture/components.md) ·
   [interfaces](02-architecture/interfaces.md) ·
   [frames and conventions](02-architecture/frames-and-conventions.md) ·
   [vehicle model](02-architecture/vehicle-model.md) ·
   [sensors](02-architecture/sensors.md)
3. **[Decisions](03-decisions/README.md)** — D-001 to D-020, one page each
4. **[Knowledge](04-knowledge/README.md)** —
   [Webots internals](04-knowledge/webots-internals.md) ·
   [vehicle model facts](04-knowledge/vehicle-model-facts.md) ·
   [RealSense D435i](04-knowledge/realsense-d435i.md) ·
   [world geometry](04-knowledge/world-geometry.md) ·
   [ROS and DDS environment](04-knowledge/ros-and-dds-environment.md) ·
   [tooling](04-knowledge/tooling.md)
5. **[Status](05-status/README.md)** —
   [completed](05-status/completed.md) ·
   [in progress](05-status/in-progress.md) ·
   [roadmap](05-status/roadmap.md)
6. **[Open questions](06-open-questions/README.md)** — Q-001 to Q-010
7. **[Bugs and lessons](07-bugs-and-lessons/README.md)** —
   [Webots API and plugins](07-bugs-and-lessons/webots-api-and-plugins.md) ·
   [process cleanup and DDS](07-bugs-and-lessons/process-cleanup-and-dds.md) ·
   [diagnosis pitfalls](07-bugs-and-lessons/diagnosis-pitfalls.md) ·
   [cart-fidelity bugs](07-bugs-and-lessons/cart-fidelity-bugs.md)
8. **[Guides](08-guides/README.md)** —
   [setup and build](08-guides/setup-and-build.md) ·
   [running the sim](08-guides/running-the-sim.md) ·
   [driving and teleop](08-guides/driving-and-teleop.md) ·
   [spawning test objects](08-guides/spawning-test-objects.md) ·
   [world assets](08-guides/world-assets.md) ·
   [troubleshooting](08-guides/troubleshooting.md)
9. **[Testing and results](09-testing-and-results/README.md)** —
   [unit tests](09-testing-and-results/unit-tests.md) ·
   [longitudinal and brake](09-testing-and-results/longitudinal-and-brake.md) ·
   [sensor and driving verification](09-testing-and-results/sensor-and-driving-verification.md) ·
   [downstream results](09-testing-and-results/downstream-results.md)
10. **[Worklog](10-worklog/README.md)** — one page per work session

## How to keep this book current

This book is only useful if it is never stale. **Every piece of work updates
it in the same branch or PR** as the work itself: code, experiments,
debugging, field tests, measurements, and decisions made in a meeting or a
chat. A PR without a docs update is incomplete (the PR template has the
checklist).

| When you... | Update |
| --- | --- |
| do any work at all | add a page to `10-worklog/` (copy the template in its README) and adjust `05-status/` |
| decide something (including "we won't do X") | add `03-decisions/D-NNN-slug.md` and a row in its index. To reverse a decision, add a new one that supersedes it and mark the old one *Superseded by D-NNN*; don't delete it |
| verify a fact (measurement, datasheet, reading source code, a live test) | add it to the right page in `04-knowledge/` with a confidence tag and *how* it was checked |
| hit something unknown that matters | add `06-open-questions/Q-NNN-slug.md` and a row in its index |
| answer an open question | set its status to *Resolved*, say what resolved it and link to where the answer now lives; keep the page |
| find a bug (yours or anyone's) | record it in `07-bugs-and-lessons/`: symptom, root cause, fix, and the rule that would have prevented it |
| change how to build, run, deploy or calibrate | update `08-guides/` |
| get a new test or scenario result | update `09-testing-and-results/` |
| change architecture, topics, parameters or conventions | update `02-architecture/` |

**Writing rules**
- **Append, don't rewrite history.** If something written here turns out to be
  wrong, add a dated *Correction (YYYY-MM-DD):* under it. Knowing that
  something was believed and then disproved is useful.
- **Say how you know.** Confidence tags: **Verified** (checked directly
  against source code, a live system or a measurement; say which),
  **Documented** (from a datasheet or other docs, not re-checked here),
  **Assumed** (a guess, placeholder or inference; must also appear in open
  questions if it matters). Never let repetition upgrade an assumption.
- **Date everything** (YYYY-MM-DD) and link PRs, commits and issues.
- **One topic per page.** Add pages rather than growing one page forever.
  Each chapter's `README.md` lists its pages; keep that list in sync.
- **Link, don't duplicate.** Facts about another repo's component belong in
  that repo's book; link to it.
- **No secrets or personal details.** No passwords, tokens, private IPs,
  personal machine configs or e-mail addresses. Three of our repos are
  public.
- **Write for someone who wasn't there.** Spell out the why, not just the
  what.
