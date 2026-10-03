# Documentation map

This directory stores durable project knowledge. Each fact should have one authoritative home; other documents link
to it instead of copying it.

## Audiences and ownership

| Document | Primary audience | Owns | Does not own |
| --- | --- | --- | --- |
| `../README.md` | Users and newcomers | Purpose, quick start, public entry points | Internal workflow or session state |
| `../AGENTS.md` | Coding agents and maintainers | Standing working rules and repository conventions | Feature history or design rationale |
| `../ROADMAP.md` | Maintainers and contributors | Planned scope and status | Detailed implementation notes |
| `HANDOFF.md` | The next work session | Current state, active context, immediate next steps | Permanent design rules |
| `ARCHITECTURE.md` | Developers | System shape, interfaces, invariants, data flow | Chronological history |
| `DECISIONS.md` | Future decision-makers | Rationale and alternatives for durable choices | Routine implementation detail |
| `TESTING.md` | Contributors and release owners | Verification commands, coverage boundaries, known pitfalls | A duplicate of current test results |
| `SECURITY.md` | Users and developers | Sensitive assets, trust boundaries, reporting, secure defaults | Full operational incident history |
| `CONTRIBUTING.md` | Contributors | Setup, change, review, and submission workflow | Agent-only instructions |
| `CHANGELOG.md` | Users | Released and unreleased user-visible changes | Commit-by-commit history |

## Update triggers

Update documents because a relevant fact changed, not merely because a session ended.

| Change | Required documentation |
| --- | --- |
| User-visible behaviour | README if onboarding changed; CHANGELOG |
| Component, interface, dependency (including a CDN script), or data-flow change | ARCHITECTURE |
| Stored record shape or IndexedDB version | ARCHITECTURE, DECISIONS, and a migration note in CONTRIBUTING |
| Durable tradeoff or reversal | DECISIONS; mark the old decision superseded |
| Test command, coverage, fixture, or environment change | TESTING |
| Untrusted input path, outbound request, or reporting-path change | SECURITY |
| Work pauses with context another session needs | HANDOFF |
| Contribution or release workflow change | CONTRIBUTING and, if agents are affected, AGENTS |
| New planned work | ROADMAP, with origin and acceptance evidence |

## Optional documents

Create these only when the project needs them, and add them to the tables above:

- `docs/data/` for the stored record schema and migrations, once there is more than one IndexedDB version.
- `docs/GLOSSARY.md` when domain vocabulary outgrows the table in `AGENTS.md`.

## Style and evidence

- Lead with the reader's task or the current truth.
- Use exact commands and repository-relative paths; avoid screenshots for procedures when text will remain searchable.
- Label examples as examples. Do not make sample credentials, hosts, or IDs look real.
- Date volatile observations and name the browser and commit when it affects reproducibility.
- Link to the source of truth instead of restating it. If duplication is necessary, identify which copy is canonical.
- Keep secrets, personal information, and anyone's real ledger out of documentation and fixtures.
