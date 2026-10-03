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

_Last updated: 2026-10-03, session 4, on `test/playwright-suite`, stacked on `fix/search-errors` (P1-05, PR #2 not
yet merged): P4-01 done, pull request open for review. Merge #2 first._

**Where things stand, in one paragraph:** The app works as a single page: search Google Books, save to IndexedDB,
remove, export CSV. P1-01, P1-02, P1-05 (pending merge), P4-01, and P4-03 are done; P1-03 and P1-04 are open. An
automated end-to-end suite now covers the whole smoke test in Chromium and Firefox without touching the network. The
biggest gap: no search has succeeded against the live Google Books API from here (always 429), and three fixtures
are synthetic until recorded (P4-04).

**Verified** (2026-10-03, on `test/playwright-suite`, CachyOS Linux, Python 3.14.7, Playwright 1.63.0)

| Suite | Result |
| --- | --- |
| `python3 tools/check_docs.py` | **0 errors** |
| `.venv/bin/python -m pytest -q` (Chromium and Firefox) | **30 passed**, 2 skipped (live), 2 xfailed (P1-03); same on three runs |
| Mutation: save never writes | 5 tests fail |
| Mutation: escaping removed | 1 test fails (`test_hostile_book_renders_as_text`) |
| Mutation: P1-05 status check and ISBN encoding removed | 3 tests fail |
| `LIVE=1` live test | **skipped**: Google answered 429 |
| CI workflow | not yet run: first run will be on this pull request |

**What works**
- **Search** (D-002). ISBN or title/author; first result only; clear messages for rate limits and HTTP errors.
  Successful searches are verified only against fixtures.
- **Save, list, remove** (D-003). Persists across reloads; duplicates detected only by ISBN.
- **Export CSV**. Title, author, ISBN, year, pages; not yet formula-safe (P1-03, test already written).
- **Escaping** (P1-02). Book text shows as text, including `&`, `'`, and `<>`.

**Not verified**
- A successful live search; the real Tailwind layout under test; Safari and phones.

**Gotchas for the next session**
- Use `commit()` in tests, never a bare click: saving is asynchronous (TESTING.md, "Known pitfalls").
- When P1-03 lands, its strict xfail test will fail the run until its marker is removed. That is intended.
- Another process may hold port 8000; the tests choose their own port.
- After removing the last book, the hidden list keeps its old item until the next render. Invisible; harmless.
- `agent-template/` is the upstream framework copy; leave it alone (AGENTS.md, "Protected areas").

## Next steps (in order)

1. Maintainer: merge PR #2 (P1-05), then this one (P4-01); check that the first CI run passes.
2. Maintainer: run `python3 tools/record_fixtures.py` and `LIVE=1` from your own network (P4-04).
3. P1-03: make CSV export formula-safe; remove the xfail marker.
4. P1-04: drop the "in-memory" and "zero-dependency" wording.

## Open questions for maintainers

- Q-004 How and where Vercel deploys the site; blocks nothing.

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

### Session 4: 2026-10-03: automated end-to-end tests

**Contributor:** Claude Code (Opus 5.5), for gordonk
**Goal:** P4-01, so later work does not depend on Google's rate limits
**Done:** P4-01
**Changed:** added `tests/` (conftest, 15 end-to-end tests, opt-in live test, five fixtures), `pytest.ini`,
`requirements-dev.txt`, `tools/record_fixtures.py`, `.github/workflows/tests.yml`, `.gitignore`; docs updated.
`index.html` unchanged
**Decisions:** D-007; Q-004 asked; P4-04 added
**Verified:** 30 passed in Chromium and Firefox on three runs; three mutation checks each caught; docs check 0 errors
**Not verified:** live API (429); the CI workflow has not run yet
**Problems / surprises:** two tests failed in Chromium only because they clicked Save and carried on before the
IndexedDB write finished; fixed in the `commit()` helper. The two "checks" on PRs are Vercel previews (Q-004). An
empty `.venv/` already existed; the test tools were installed into it
**Corrections:** none
**Left undone:** P1-03, P1-04, P4-04
**Next session should start with:** P1-03, once #2 and this pull request are merged

### Session 3: 2026-10-03: clear search errors

**Contributor:** Claude Code (Opus 5.5), for gordonk
**Goal:** P1-05
**Done:** P1-05
**Changed:** `index.html`: ISBN URL-encoded; non-OK responses report a rate limit (429) or the HTTP status instead
of "No books found"
**Decisions:** none
**Verified:** docs check 0 errors; five stubbed reply types and the ISBN encoding, each failing with the fix stashed;
a live 429 showed the new message
**Not verified:** a successful live search; other browsers
**Problems / surprises:** PR #1 was reported merged before it was; checked with `gh pr view` before branching
**Corrections:** none
**Left undone:** P1-03, P1-04
**Next session should start with:** P1-03

### Session 2: 2026-10-03: escape book fields

**Contributor:** Claude Code (Opus 5.5), for gordonk
**Goal:** P1-02
**Done:** P1-02, P4-03
**Changed:** `index.html`: `escapeHTML()` on every book field rendered via `innerHTML`; remove button wired with
`addEventListener` instead of inline `onclick`
**Decisions:** none
**Verified:** docs check 0 errors; injection check pass, and fails with the fix stashed; smoke test 8/8 with a
stubbed search (Chromium, built-in browser)
**Not verified:** live Google Books search (429); other browsers
**Problems / surprises:** port 8000 already in use by another process; Google Books 429 shown as "No books found"
(P1-05)
**Corrections:** session 1's handoff said the docs were uncommitted on `0fed6b3`; they were merged as `af4256b`
**Left undone:** P1-03, P1-04, P1-05
**Next session should start with:** P1-05

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
