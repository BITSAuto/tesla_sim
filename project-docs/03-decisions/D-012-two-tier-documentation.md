# D-012 · Two-tier documentation: a shared README plus private notes

- **Date:** 2026-09-09
- **Status:** **Superseded by [D-020](D-020-project-docs-replace-private-notes.md)** (2026-10-09)

## Context
Once the project was going to be shared with teammates, the single README had
grown to mix shareable usage notes with personal-machine debugging history.

## Decision (at the time)
Keep a shareable `README.md` and a private, gitignored engineering log
(`private-notes/` in the workspace) with numbered files for brief, decisions,
facts, open questions, bugs, findings and a decision tree.

## Why it was superseded
Private notes weren't visible to collaborators, and nothing kept them up to
date across sessions. Their content has been migrated into this book.
