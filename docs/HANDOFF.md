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

_Last updated: 2026-10-03, session 6, on `fix/csv-formulas` (from `main` at `7c3348f`, which has P1-02 to P1-06 and
P4-01): P1-03 done, pull request open for review._

**Where things stand, in one paragraph:** Search works (Open Library, D-008), books save and reload, export is
formula-safe, and an automated suite covers it all in Chromium and Firefox without the network. Phase 1 has one item
left: P1-04, the false "in-memory" and "zero-dependency" wording. Nobody has yet checked the deployed site.

**Verified** (2026-10-03, on `fix/csv-formulas`, CachyOS Linux, Python 3.14.7, Playwright 1.63.0)

| Suite | Result |
| --- | --- |
| `python3 tools/check_docs.py` | **0 errors** |
| `.venv/bin/python -m pytest -q` (Chromium and Firefox) | **50 passed**, 4 skipped (live); same on three runs |
| Mutation: no formula prefix | 7 tests fail |
| Mutation: no quote doubling | 1 test fails |
| `LIVE=1` live tests | carried over: 4/4 on 2026-10-03, session 5; export does not touch the network |

**What works**
- **Search** (D-008). ISBN finds that exact edition; title/author finds the first matching work.
- **Save, list, remove** (D-003). Persists across reloads; duplicates detected only by ISBN.
- **Export CSV** (P1-03). Every cell quoted; formula-like cells start with `'`.
- **Escaping** (P1-02). Book text shows as text, including `&`, `'`, and `<>`.

**Not verified**
- The Vercel deployment (Q-004); opening an export in a real spreadsheet program; Safari and phones.

**Gotchas for the next session**
- A 429 is not always a rate limit: Google's was a quota of 0. Read the reply body.
- A title search's ISBN and year belong to the work, not to a particular edition (ARCHITECTURE, "Claims vs. code").
- Use `commit()` in tests, never a bare click; read CSV with `newline=""` (TESTING.md, "Known pitfalls").
- PRs #2 to #4 show as "closed", not "merged", on GitHub; their commits are on `main` unchanged.
- `agent-template/` is the upstream framework copy; leave it alone (AGENTS.md, "Protected areas").

## Next steps (in order)

1. Maintainer: review and merge the P1-03 pull request.
2. P1-04: drop the "in-memory" and "zero-dependency" wording; that finishes Phase 1.
3. Maintainer: try a search and an export on the deployed site (Q-004); open the CSV in a spreadsheet.

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

### Session 6: 2026-10-03: formula-safe CSV export

**Contributor:** Claude Code (Opus 5.5), for gordonk
**Goal:** P1-03
**Done:** P1-03
**Changed:** `index.html`: `csvCell()` quotes every export cell and prefixes formula triggers with `'`; tests: the
xfail test became two real ones (eight cases per browser); `export_csv()` reads with `newline=""`
**Decisions:** none
**Verified:** 50 passed, three runs; two mutation checks caught
**Not verified:** opening the CSV in a spreadsheet program; the deployed site
**Problems / surprises:** the ISBN, year, and pages cells had no quote escaping either; the carriage-return case
first failed because of the test helper, not the app
**Corrections:** none
**Left undone:** P1-04
**Next session should start with:** P1-04

### Session 5: 2026-10-03: switch to Open Library

**Contributor:** Claude Code (Opus 5.5), for gordonk
**Goal:** P4-04 (record real fixtures), which turned into P1-06
**Done:** P1-06, P4-04
**Changed:** `index.html` search now calls Open Library (`bookFromEdition()`, `bookFromWork()`); fixtures moved to
`tests/fixtures/open_library/`, four recorded and three synthetic; `tools/record_fixtures.py` and the live tests
target Open Library; docs updated
**Decisions:** D-008 (supersedes D-002); D-007 updated in place
**Verified:** 36 passed, three runs; live 4/4 against openlibrary.org; two mutation checks caught
**Not verified:** the deployed site; earlier mutation checks not rerun on the new search code
**Problems / surprises:** the maintainer's terminal is on the same machine as the agent, so "try from your network"
could not help
**Corrections:** sessions 2 to 4 called Google's 429 a rate limit, and session 4's summary blamed this machine's IP.
Both were wrong: the reply body shows a daily quota of 0 for all keyless requests (D-008)
**Left undone:** P1-03, P1-04
**Next session should start with:** P1-03, once #2, #3, and this pull request are merged

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
