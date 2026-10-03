# Agent project template

A documentation starter for projects developed across short human and coding-agent sessions. Its central rule is
simple: the repository, not a particular chat or tool, carries durable project memory.

The template separates current state, enduring design, planned work, verification, and history so that each fact
has one authoritative home. Delete optional documents that do not earn their upkeep; do not leave empty ceremony.

## Contents

| File | Answers | Update when |
| --- | --- | --- |
| `AGENTS.md` | How should an agent work in this repository? | A durable workflow rule or maintainer preference changes |
| `ROADMAP.md` | What work is planned, active, done, or dropped? | Planned status or scope changes |
| `docs/README.md` | Which document owns each kind of information? | The documentation set changes |
| `docs/HANDOFF.md` | What is true now, and what should happen next? | Work pauses or current state changes materially |
| `docs/ARCHITECTURE.md` | How does the system fit together and what must remain true? | Components, interfaces, data flow, or invariants change |
| `docs/DECISIONS.md` | Why was a durable choice made? | A consequential choice is accepted or superseded |
| `docs/TESTING.md` | How is behaviour verified and what remains unproved? | A suite, command, requirement, or known limitation changes |
| `docs/SECURITY.md` | What is sensitive, trusted, and reportable? | A threat, boundary, secret, or response path changes |
| `docs/CONTRIBUTING.md` | How does a contribution move from idea to merge? | The contribution workflow changes |
| `docs/CHANGELOG.md` | What changed for users? | A user-visible change lands or a release is cut |
| `docs/archive/` | What historical context is no longer current? | Live documents exceed their useful size |
| `tools/check_docs.py` | Are the documentation links and identifiers internally consistent? | Documentation conventions change |

`CLAUDE.md` contains only an import of `AGENTS.md` so tool-specific instructions cannot drift.

## Adopt the template

1. Copy the directory contents to the repository root.
2. Replace every `{{...}}` placeholder. Run `python3 tools/check_docs.py` to find leftovers.
3. Delete inapplicable sections and documents, then remove their links and checker entries. A small truthful set is
   better than a comprehensive abandoned one.
4. Describe the system as it exists. Record inherited choices as accepted decisions instead of pretending they were
   made during the migration.
5. Agree on branch, review, release, dependency, and destructive-action authority in `AGENTS.md`.
6. Seed the roadmap and handoff with the next real piece of work. Run `python3 tools/check_docs.py` again.

For an existing repository, derive claims from code, tests, configuration, and history. Mark unverified assumptions
plainly and turn important gaps into roadmap items.

## Information lifecycle

- **Current truth is rewritten.** Handoff and architecture describe the repository now, not every state it had.
- **History is appended or archived.** Decisions, releases, and session entries preserve why changes happened.
- **Plans have stable references.** Do not renumber roadmap IDs after other documents or commits cite them.
- **Evidence has provenance.** Volatile numbers include a date, commit, environment, and command where useful.
- **Claims include limits.** State what a test or observation does not prove.
- **Important prose becomes enforcement.** Tests, schemas, types, and automation should uphold critical rules.
- **Documentation has update triggers.** `docs/README.md` prevents both stale docs and update-everything busywork.

## Scale it to the project

For a small library, `README`, `AGENTS`, architecture, testing, and a concise handoff may be enough. A service may
also need runbooks, API documentation, data migration notes, service-level objectives, and incident procedures.
Add a document only when it has a clear audience, owner, source of truth, and update trigger.
