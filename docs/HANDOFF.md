# Session Handoff

Read this first when resuming unfinished work. Rewrite the top half whenever current state changes materially or work
pauses with context another session needs.
The session log below it is append-only history. "Current state" fits on a screen or two (about 80 lines);
what does not fit is history, and belongs in the session log.

Protocol: see [AGENTS.md](../AGENTS.md) (`CLAUDE.md` imports it). Plan: [ROADMAP.md](../ROADMAP.md).
Architecture: [ARCHITECTURE.md](ARCHITECTURE.md). Decisions: [DECISIONS.md](DECISIONS.md).
Tests: [TESTING.md](TESTING.md). Security: [SECURITY.md](SECURITY.md).
Changes: [CHANGELOG.md](CHANGELOG.md). Older sessions: [archive/](archive/README.md).

---

## Current state

_Last updated: 2026-10-03, session 1, on `main` at `0fed6b3`: project documentation and `tools/check_docs.py` added,
uncommitted. `index.html` unchanged._

**Where things stand, in one paragraph:** The app works as a single page: search Google Books, save to IndexedDB,
remove, export CSV. Phase 1's documentation item (P1-01) is done; its four code fixes are open, and the most urgent
is P1-02, an HTML-injection hole in how book text is rendered. There are no automated tests, and nobody has recorded
a run of the app in any browser yet.

**Verified** (2026-10-03, on `0fed6b3` plus the uncommitted docs, Linux, Python 3.14.7)

| Suite | Result |
| --- | --- |
| `python3 tools/check_docs.py` | **0 errors** |

**What works** (from reading the code, not from a recorded run)
- **Search** (D-002; `index.html` submit handler). ISBN or title/author; takes the first result only.
- **Save, list, remove** (D-003). Persists across reloads; duplicates detected only by ISBN.
- **Export CSV**. Title, author, ISBN, year, pages.

**Not verified**
- The manual smoke test has not been run in any browser.

**Gotchas for the next session**
- Book text is inserted with `innerHTML`; do not add new rendering that way (P1-02).
- `file://` and `http://localhost:8000` hold separate ledgers.
- `agent-template/` is the upstream framework copy; leave it alone (AGENTS.md, "Protected areas").

## Next steps (in order)

1. P1-02: escape book fields; verify with the injection checks in TESTING.md.
2. Run the manual smoke test in a real browser and record the result here.
3. P1-03, P1-05, P1-04.
4. P4-01: automate the smoke test so later phases have a safety net.

## Open questions for maintainers

- None open. Q-001 to Q-003 answered 2026-10-03 (D-004 to D-006).

## Session log

Newest first. Copy the template for each new session. Work done between sessions (a maintainer's commits, another
agent) gets a short entry too, written by whoever notices it, so the log has no gaps. Past 10 entries, move the
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

### Session 1: 2026-10-03: adopt the agent project template

**Contributor:** Claude Code (Opus 5.5), for gordonk
**Goal:** Set up the development workflow and documentation from `agent-template/`.
**Done:** P1-01
**Changed:** added `AGENTS.md`, `CLAUDE.md`, `README.md`, `ROADMAP.md`, `docs/` set, `tools/check_docs.py` (now
checks AGENTS.md's "Repository map" table; the upstream copy looks for a "Layout" heading the template does not have)
**Decisions:** D-001, D-002, D-003 recorded for choices made on 2026-08-20; Q-001 to Q-003 opened and answered by
the maintainer the same day, giving D-004 (dependencies by proposal), D-005 (git version tags), D-006 (books, then
visual media)
**Verified:** `python3 tools/check_docs.py`: 0 errors
**Not verified:** the app was not run; behaviour descriptions come from reading `index.html`
**Problems / surprises:** UI text claims "in-memory" storage and "zero-dependency"; both are false (P1-04)
**Corrections:** none
**Left undone:** all code fixes; nothing committed
**Next session should start with:** P1-02
