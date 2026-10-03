# {{PROJECT}}

{{One paragraph: what the project is, who it serves, and its technical shape.}}

This is the canonical instruction file for coding agents. `CLAUDE.md` imports it; do not duplicate these rules in
tool-specific files. Project facts belong in the documents linked below, not in an agent's private memory.

## Start here

1. Read `docs/HANDOFF.md` for the current state, active work, and gotchas.
2. Read the relevant roadmap item and the parts of `docs/ARCHITECTURE.md` and `docs/TESTING.md` that apply.
3. Inspect `git status` and recent history. Do not overwrite work you did not create.
4. Verify important inherited claims before relying on them. Use the fastest relevant check first.
5. State the intended scope briefly, then work on one independently reviewable change at a time.

If the repository is new or unfamiliar, read `README.md` and `docs/README.md` first. If the request conflicts with
these instructions or the working tree contains overlapping edits, stop and ask the maintainer.

## While working

- Reference roadmap or issue IDs where one exists. Do not invent an ID for an incidental, self-contained fix.
- Keep changes scoped. Do not mix opportunistic refactors with requested work.
- Preserve user changes. Never reset, clean, or rewrite history without explicit permission.
- Record a decision in `docs/DECISIONS.md` when reasonable maintainers could revisit the choice later.
- Update documentation in the same change when behaviour, interfaces, commands, risks, or project structure change.
- Distinguish observed facts from inference. Include the command, date, environment, or source behind volatile claims.
- Prefer enforcement to prose: important invariants should have a test, type, schema, linter, or runtime check.
- Treat all external input as untrusted at its boundary. Never expose secrets in logs, fixtures, prompts, or commits.
- Add newly discovered work to `ROADMAP.md` only when it is genuinely out of scope for the current change.

## Finishing a change

1. Run the checks appropriate to the change, following `docs/TESTING.md`. Record failures and anything not run.
2. Review the diff for unrelated edits, generated files, credentials, stale names, and documentation drift.
3. Update `docs/HANDOFF.md` if work will continue in another session or if the repository's current state changed.
4. Update the roadmap item, decision record, architecture, security notes, and changelog only when their documented
   update trigger applies (see `docs/README.md`).
5. Run `python3 tools/check_docs.py` and report the result.

Do not manufacture ceremony: typo-only or mechanical changes do not need a decision, changelog entry, or handoff
rewrite unless they alter a claim those documents make.

## Working agreement

{{Choose one workflow and delete the others: pull request; maintainer-reviewed branch; direct-to-main. State who may
commit, push, merge, publish, add dependencies, delete data, and perform migrations.}}

- Default branch: `{{main}}`.
- Working branch pattern: `{{feature/<topic>}}`.
- Commit format: {{format and whether IDs are required}}.
- Release/version scheme: {{scheme and source of truth}}.

Never force-push, rewrite shared history, publish, or rotate/delete production data without explicit permission.

## Maintainer preferences

Record durable preferences here so they survive agent and session changes. Keep temporary task instructions in the
task or handoff instead.

- **Writing:** {{voice, terminology, and formatting preferences}}.
- **Code comments:** {{what comments should explain and expected density}}.
- **Asking vs. doing:** {{actions that require confirmation}}.
- **Reporting:** {{desired result and verification format}}.

## Protected areas

Things an agent must not change without explicit permission. Every rule includes its reason or decision.

| Path or thing | Rule | Why |
| --- | --- | --- |
| {{e.g. `docs/CREDITS.md`}} | {{Do not edit}} | {{Maintainer-owned content}} |

## Names and terms

| Canonical term | Meaning | Formerly / not to be confused with |
| --- | --- | --- |
| {{Product}} | {{What it names}} | {{Old name or nearby concept}} |

Move a large domain vocabulary into `docs/GLOSSARY.md` and link it here.

## Repository map

| Path | Purpose |
| --- | --- |
| `{{path}}` | {{What it owns}} |
| `AGENTS.md` | Canonical agent instructions |
| `ROADMAP.md` | Planned work with stable IDs |
| `docs/README.md` | Documentation map and update triggers |
| `docs/HANDOFF.md` | Current state, next steps, gotchas, and bounded session history |
| `docs/ARCHITECTURE.md` | Components, boundaries, invariants, state, and failure modes |
| `docs/DECISIONS.md` | Append-only architectural and product decisions; open questions |
| `docs/TESTING.md` | Test strategy, commands, limitations, and environment recipes |
| `docs/SECURITY.md` | Assets, trust boundaries, secret handling, and reporting |
| `docs/CONTRIBUTING.md` | Human and agent contribution workflow |
| `docs/CHANGELOG.md` | User-visible release notes |
| `docs/archive/` | Historical material no longer current |
| `tools/check_docs.py` | Documentation consistency checks |

## Engineering conventions

- {{Language, formatting, linting, and framework rules.}}
- {{Supported platforms and explicit non-targets.}}
- {{Key architectural invariants; keep the full list in ARCHITECTURE.md.}}
- {{Data ownership, retention, migration, and compatibility rules.}}
- {{Dependency policy and approval threshold.}}
- {{Generated files: how to regenerate them and whether they are committed.}}

## Environments

| Environment | Can access | Cannot access / caveats |
| --- | --- | --- |
| {{Local development}} | {{services, browsers, sibling repos}} | {{sandbox or network limits}} |
| {{CI}} | {{services and secrets available}} | {{missing capabilities}} |

## Run and verify

- Setup: `{{command}}`.
- Run: `{{command}}`.
- Fast checks: `{{command}}`.
- Full checks: `{{command}}`.
- Detailed test guidance: `docs/TESTING.md`.
