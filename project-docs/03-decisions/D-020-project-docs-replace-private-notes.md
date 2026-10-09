# D-020 · A shared `project-docs/` book in every repository replaces private notes

- **Date:** 2026-10-09
- **Status:** Accepted
- **Supersedes:** [D-012](D-012-two-tier-documentation.md)

## Context
Engineering history lived in private, gitignored notes on one laptop. The
owner wants a shared context between themselves and collaborators, kept
current by everyone.

## Decision
Every BITSAuto repository we created (`tesla_sim`, `vehicle_bridge`,
`traversability`, `cart_driver`) has a `project-docs/` folder structured as a
book: numbered chapter directories, each with a `README.md` index and one
page per topic, plus a top-level index. Every piece of work updates it in the
same PR. `AGENTS.md`/`CLAUDE.md` and the PR template enforce this.

## Consequences
- The private notes' content was migrated here (personal machine details
  removed, since this repo is public).
- Three code comments that pointed at the private notes now point here.
