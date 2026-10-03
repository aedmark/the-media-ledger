# Session Handoff

Read this first when resuming unfinished work. Rewrite the top half whenever current state changes materially or work
pauses with context another session needs.
The session log below it is append-only history. "Current state" fits on a screen or two ({{about 80 lines}});
what does not fit is history, and belongs in the session log.

Protocol: see [AGENTS.md](../AGENTS.md) (`CLAUDE.md` imports it). Plan: [ROADMAP.md](../ROADMAP.md).
Architecture: [ARCHITECTURE.md](ARCHITECTURE.md). Decisions: [DECISIONS.md](DECISIONS.md).
Tests: [TESTING.md](TESTING.md). Security: [SECURITY.md](SECURITY.md).
Changes: [CHANGELOG.md](CHANGELOG.md). Older sessions: [archive/](archive/README.md).

---

## Current state

_Last updated: {{YYYY-MM-DD}}, session {{N}}, on `{{branch and commit}}`: {{what changed and what remains uncommitted,
unmerged, or externally blocked}}._

**Where things stand, in one paragraph:** {{Which phases are done, what is left, and the biggest gap (often not
code: "nothing has been tried on a real phone yet").}}

**Verified** ({{YYYY-MM-DD}}, on `{{commit}}`, {{environment: machine, browser and version, runtime}})

Every row was run this session unless it explicitly says it was carried over, with the earlier date.

| Suite | Result |
| --- | --- |
| `{{command}}` | **{{N/N}}** |
| `{{command}}`, several runs | {{tally, e.g. 6/7, 7/7, 7/7; what the misses were}} |

**What works**
- **{{Feature}}** ({{IDs, decisions; main files}}). {{What a user can do, in plain words; its limits.}}

**Not verified** (say what has only run in tests, and what nobody has seen)
- {{e.g. "Only run in headless Chromium: not seen in Firefox or on a real phone."}}

**Gotchas for the next session**
- {{Traps a fresh session would fall into: flaky tests and why, tools that mangle files, environment limits.
  Pitfalls that are about tests go in TESTING.md's list instead.}}

## Next steps (in order)

1. {{The next concrete action, with its item ID or blocker.}}
2. {{Any required human or environment-specific check: where, how, and expected result.}}
3. {{Later candidates, one line each, ordered by value or dependency.}}

## Open questions for maintainers

The ones that block the next steps, by ID; the questions themselves live in DECISIONS.md, "Open questions".

- Q-001 {{one line, and what it blocks}}

## Session log

Newest first. Copy the template for each new session. Work done between sessions (a maintainer's commits, another
agent) gets a short entry too, written by whoever notices it, so the log has no gaps. Past {{10}} entries, move the
oldest to `docs/archive/` and leave a pointer here.

### Template

```
### Session N: YYYY-MM-DD: short title

**Contributor:** person or agent/tool
**Goal:**
**Done:** roadmap IDs
**Changed:** files / behaviour
**Decisions:** D-numbers added
**Verified:** tests and their counts; mutation results if performed; for runs that vary, the tally
**Not verified:** checks skipped or environments unavailable
**Problems / surprises:**
**Corrections:** earlier notes (here or in other docs) found wrong, and what was actually true
**Left undone:**
**Next session should start with:**
```
