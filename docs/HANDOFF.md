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

_Last updated: 2026-10-03, session 3, on `fix/search-errors` (from `main` at `ef213e9`, which has P1-02): P1-05
fixed, pull request open for review._

**Where things stand, in one paragraph:** The app works as a single page: search Google Books, save to IndexedDB,
remove, export CSV. P1-01, P1-02, P1-05, and P4-03 are done; P1-03 and P1-04 are open. The biggest gap: no search
has yet succeeded against the live Google Books API from here (it keeps answering 429), and there are no automated
tests.

**Verified** (2026-10-03, on `fix/search-errors`, Linux, built-in Chromium browser, `python3 -m http.server 8123`)

| Suite | Result |
| --- | --- |
| `python3 tools/check_docs.py` | **0 errors** |
| Search error handling, stubbed 429 / 503 / empty / found / network failure | **5/5** right message; fails with the fix stashed |
| ISBN encoding (`978&q=x#y`) | **pass**: sent as `978%26q%3Dx%23y`; unencoded with the fix stashed |
| Live search from this machine | Google answered 429; the app showed the new rate-limit message |
| Injection check, smoke test 8/8 (stubbed search) | carried over from session 2 on `fix/escape-book-fields` |

**What works**
- **Search** (D-002). ISBN or title/author; first result only; clear messages for rate limits and HTTP errors.
  A successful search has been seen only with a stubbed `fetch`.
- **Save, list, remove** (D-003). Persists across reloads; duplicates detected only by ISBN.
- **Export CSV**. Title, author, ISBN, year, pages; not yet formula-safe (P1-03).
- **Escaping** (P1-02). Book text shows as text, including `&`, `'`, and `<>`.

**Not verified**
- A successful live Google Books search; Firefox, Safari, and phones.

**Gotchas for the next session**
- Another process may already hold port 8000; use another port (that is a separate origin with its own ledger).
- Google Books answers 429 from this machine; see TESTING.md "Environment recipes" for the stub.
- After removing the last book, the hidden list keeps its old item until the next render. Invisible; harmless.
- `pkill -f "http.server 8123"` inside a longer shell command also matches that shell and kills it; run it alone.
- `agent-template/` is the upstream framework copy; leave it alone (AGENTS.md, "Protected areas").

## Next steps (in order)

1. Maintainer: review and merge the P1-05 pull request.
2. P1-03: make CSV export formula-safe.
3. P1-04: drop the "in-memory" and "zero-dependency" wording.
4. Run the smoke test against the live API from a normal network.
5. P4-01: automate the smoke test, with the stubbed `fetch` used in sessions 2 and 3.

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
