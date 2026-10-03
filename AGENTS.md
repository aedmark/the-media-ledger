# Library Ledger

Library Ledger (repository: `the-media-ledger`) is a personal book tracker that runs entirely in the browser. A user
looks a book up by ISBN or by title and author through the public Open Library API, saves it to a ledger kept in the
browser's IndexedDB, and can export the ledger as CSV. It is one static `index.html` with inline JavaScript: no build
step, no server, no account.

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

- Reference roadmap IDs (`P1-03`) where one exists. Do not invent an ID for an incidental, self-contained fix.
- Keep changes scoped. Do not mix opportunistic refactors with requested work.
- Preserve user changes. Never reset, clean, or rewrite history without explicit permission.
- Record a decision in `docs/DECISIONS.md` when reasonable maintainers could revisit the choice later.
- Update documentation in the same change when behaviour, interfaces, commands, risks, or project structure change.
- Distinguish observed facts from inference. Include the command, date, browser, or source behind volatile claims.
- Prefer enforcement to prose: important invariants should have a test or runtime check.
- Treat every Open Library response and every stored record as untrusted text: never insert it with `innerHTML`
  unescaped (see `docs/SECURITY.md`). Never put an API key in the repository.
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

Workflow: **pull request**. Agents work on a branch and open a pull request against `main`; the maintainer
(aedmark) reviews and merges. Agents may commit and push their own working branch. Only the maintainer merges to
`main`, cuts release tags, or approves a new dependency. Agents may propose dependencies (D-004).

- Default branch: `main`.
- Working branch pattern: `<type>/<topic>`, e.g. `fix/escape-titles`, `feat/edit-entry`, `docs/handoff`.
- Commit format: imperative subject under 72 characters; prefix the roadmap ID when there is one
  (`P1-01 Escape book fields before rendering`).
- Release/version scheme: annotated git tags `vMAJOR.MINOR.PATCH` on `main` (D-005). Versions are for tracking;
  never announce a bump in the UI or as a changelog entry.

The maintainer deletes each branch once it is merged, and GitHub may then show its pull request as "closed" rather
than "merged". Check `main` for the commits, not the pull request's label.

Never force-push, rewrite shared history, publish, or change the IndexedDB schema version without explicit permission.

## Maintainer preferences

Record durable preferences here so they survive agent and session changes. Keep temporary task instructions in the
task or handoff instead.

- **Writing:** plain, short sentences; British or American spelling is fine, but be consistent within a file.
- **Code comments:** explain why, not what; match the existing light density in `index.html`.
- **Asking vs. doing:** propose a dependency when it earns its place, and wait for approval before adding it
  (D-004); ask before splitting `index.html` into several files (D-001), changing
  stored data shape, or deleting anything.
- **Reporting:** lead with the result; list the checks run and their outcome, and what was not checked.

## Protected areas

Things an agent must not change without explicit permission. Every rule includes its reason or decision.

| Path or thing | Rule | Why |
| --- | --- | --- |
| `LICENSE` | Do not edit | Maintainer-owned legal text |
| IndexedDB name `LibraryLedgerDB`, store `books`, version `1` | Do not rename or bump without a migration plan | Existing users' ledgers live there; a rename silently empties them (D-003) |
| `agent-template/` | Do not edit | Upstream copy of the documentation framework this repo follows |

## Names and terms

| Canonical term | Meaning | Formerly / not to be confused with |
| --- | --- | --- |
| Library Ledger | The product name shown in the UI | `the-media-ledger` is the repository name only |
| Ledger | The user's saved list of books (IndexedDB store `books`) | Not a financial ledger |
| Staged book | A search result shown in "Ready to Save", not yet saved | A saved entry |
| Commit to Ledger | The UI action that saves the staged book | A git commit |

## Repository map

| Path | Purpose |
| --- | --- |
| `index.html` | The whole application: markup, styles, and script |
| `LICENSE` | MIT licence |
| `AGENTS.md` | Canonical agent instructions |
| `CLAUDE.md` | Imports `AGENTS.md` for Claude Code |
| `README.md` | What the project is and how to run it |
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
| `tools/record_fixtures.py` | Records real Open Library replies into the test fixtures |
| `tests/` | End-to-end tests (`test_app.py`), the opt-in live tests, and Open Library fixtures |
| `pytest.ini` | Test settings: which browsers run by default |
| `requirements-dev.txt` | Pinned test tools (D-007) |
| `.github/workflows/tests.yml` | CI: docs check and tests on pull requests and `main` |
| `agent-template/` | The unmodified documentation framework this setup was derived from |

## Engineering conventions

- Plain HTML, CSS (Tailwind utility classes via CDN), and browser JavaScript, with no build step (D-001). Outside
  dependencies are welcome by proposal (D-004).
- Books only for now; collectible visual media (VHS, DVD, Blu-ray) come later, so prefer media-neutral names for new
  stored fields and shared helpers (D-006).
- Supported: current desktop and mobile versions of Chrome, Firefox, and Safari. Not supported: Internet Explorer,
  browsers without IndexedDB.
- Book data comes only from Open Library (`/api/books` for ISBNs, `/search.json` for titles), without a key (D-008).
- Data stays on the device. Nothing is sent anywhere except the search query to Open Library.
- Stored records keep the shape `{id, title, author, isbn, publishedYear, pages}`; a change needs a migration (D-003).
- No generated files are committed.
- New behaviour gets an end-to-end test in `tests/test_app.py`; tests never touch the real network (D-007).

## Environments

| Environment | Can access | Cannot access / caveats |
| --- | --- | --- |
| Local development | Any browser; `python3 -m http.server` for a local origin; Open Library over the network | IndexedDB is per origin: data saved under `file://` is not visible at `http://localhost:8000` |
| Agent sandbox | Python 3, `.venv` with the test tools, cached Playwright Chromium and Firefox; possibly the built-in browser | Open Library reachable (2026-10-03); prefer the fixtures, and run live tests sparingly |
| CI (GitHub Actions) | Ubuntu, Python 3.13, Playwright Chromium and Firefox | No network use by the tests; no secrets |
| Vercel | Preview deployment per pull request | Configured outside the repository; production unknown (Q-004) |

## Run and verify

- Setup: none to run the app; for tests, the three commands in `docs/TESTING.md`, "Before any run".
- Run: `python3 -m http.server 8000` (or any free port), then open `http://localhost:8000/`.
- Fast checks: `python3 tools/check_docs.py` and `.venv/bin/python -m pytest -q`.
- Full checks: the fast checks plus the live test and manual checks in `docs/TESTING.md`.
- Detailed test guidance: `docs/TESTING.md`.
