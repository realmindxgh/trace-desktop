# Trace Desktop

Cross-platform qualitative research workspace. Windows is the first shipping target, with macOS and Linux kept in the architecture from the start.

## Current development status

Trace **v0.12.1: UX and Installer Hardening** has completed its automated Windows source and release verification. The verified Windows release is now awaiting real-machine user acceptance, especially interactive maintenance-mode and visual/readability checks.

Before changing application code, installer code, CI, or release behavior, read [`AGENTS.md`](AGENTS.md). It contains the execution plan, priorities, acceptance criteria, testing matrix, release rules, and handoff requirements for coding agents and contributors.

Then read [`PROGRESS.md`](PROGRESS.md). It is the live ledger of what has actually been completed, the exact workflow/artifact evidence, known findings, remaining work, and the next continuation point. Agents making material changes are required to update it before handing off work.

Also review the [`v0.12.1 visual direction guide`](docs/visuals/README.md) alongside `AGENTS.md`. It shows the intended typography, Code and Data workspace hierarchy, inspector behavior, installer maintenance flow, accessibility direction, and upgrade-verification concept.
