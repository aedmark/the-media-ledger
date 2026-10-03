# Testing

How to run every check, what each one proves, and what it cannot. Read this before claiming anything works.
The results themselves live in HANDOFF's "Current state"; this file is how to get them.

## The suites

| Suite | File | Proves | Does not prove | Time, needs |
| --- | --- | --- | --- | --- |
| Docs check | `tools/check_docs.py` | roadmap IDs, decisions, questions, links, and session numbers are consistent | anything about the app | a second, Python 3 |
| End to end | `tests/test_app.py` | a user's path through the app (search, save, reload, duplicate, remove, export, error messages, injection) in headless Chromium and Firefox, with Google Books answered from fixtures | that Google's real replies still look like the fixtures; Safari; phones; layout | ten seconds, `.venv` with `requirements-dev.txt`, Playwright browsers; no network |
| Live | `tests/test_live.py` | one real ISBN search against Google Books works today | that it works every time; anything a 429 hides | a few seconds, network; skipped unless `LIVE=1` |
| Manual | this file, "Manual checks" | what looks right to a person in a real browser | anything not looked at | ten minutes, a browser |

**The fast set** (before every commit): `python3 tools/check_docs.py` and `.venv/bin/python -m pytest -q`.
**The full set** (before merging a change to `index.html`, and before a release): the fast set, plus `LIVE=1`
once from a normal network, plus the manual checks for the area changed.

CI (`.github/workflows/tests.yml`) runs the fast set on every pull request and on pushes to `main`.

**Expected results** live in HANDOFF's "Verified" table, with the date and commit they were measured on.

## Before any run

- **Setup, once:**

  ```bash
  python3 -m venv .venv
  .venv/bin/python -m pip install -r requirements-dev.txt
  .venv/bin/python -m playwright install chromium-headless-shell firefox
  ```

  Browsers go to `~/.cache/ms-playwright/` (outside the repo, shared between projects).
- **Clean state:** nothing to do for the automated suites. Each test gets a fresh browser context, so IndexedDB
  starts empty, and the tests serve the repo on their own random port. For manual checks, use a private window:
  never clear site data in a browser profile that holds someone's real ledger.
- **Network:** the end-to-end suite needs none and refuses to use it: `tests/conftest.py` answers Google Books from
  `tests/fixtures/google_books/`, replaces the Tailwind CDN with the one rule the app's logic needs (`.hidden`),
  drops font requests, and fails any test whose page tries to reach anything else.

## Running each suite

### Docs check

```bash
python3 tools/check_docs.py
```

- A pass is a final line with `0 error(s)`; exit code 0. Warnings do not fail it.

### End to end

```bash
.venv/bin/python -m pytest -q
```

- Runs every test in Chromium and Firefox (`pytest.ini`). One browser: `-o addopts="" --browser chromium`.
  One test: `-k duplicate`. Watch it: `--headed --slowmo 300`.
- A pass is a final line with `N passed`, no `failed` or `error`. Expected skips: the live test (2, one per
  browser). Expected `xfailed`: tests for open roadmap items, marked `xfail(strict=True)` with the item ID; when the
  fix lands they pass, strict mode fails the run, and the marker must be removed.
- Output: nothing in the repo; downloads and traces go to a temporary directory, `test-results/` only with
  `--tracing on` (gitignored).

### Live

```bash
LIVE=1 .venv/bin/python -m pytest -q -rs -o addopts="" --browser chromium tests/test_live.py
```

- One request to Google. A 429 skips with "rate limited"; that is not a pass. Record the result in HANDOFF with the
  date and network.

### Recording fixtures

Three fixtures are synthetic stand-ins in Google's shape until someone records the real replies:

```bash
python3 tools/record_fixtures.py
```

Three requests, from a network Google is not rate-limiting. Review the diff, update the table in
`tests/fixtures/google_books/README.md`, and rerun the end-to-end suite: a test that now fails has found a
difference between the stand-in and the real thing.

### Adding a check

- Add tests to `tests/test_app.py`, using its helpers (`search_isbn`, `search_title`, `commit`, `saved_records`,
  `reload`, `export_csv`). To make Google answer something new, add a fixture file and
  `google.reply_with(query, file)`; for an HTTP error, `google.next_status = 503`.
- Assert on what happened (a record in IndexedDB, a row in the list, a cell in the CSV, the URL the app requested);
  check toast wording only when the message itself is the behaviour under test.
- Before trusting a new check, make it fail: undo the fix (only the fix) and run it.
- Write the test for an open roadmap item first, marked `@pytest.mark.xfail(strict=True, reason="P1-NN: ...")`.

## Runs that vary

Only the live test depends on something outside the code. One run proves little: a pass says Google answered today,
a 429 says nothing about the code. The end-to-end suite should be deterministic; a test that passes and fails on
the same commit is a bug in the test (see "Known pitfalls").

## Change-to-check matrix

| Changed area | Minimum checks | Additional evidence |
| --- | --- | --- |
| Documentation only | `python3 tools/check_docs.py` | none |
| Rendering or search | fast set | live test once; a look in a real browser |
| Storage or record shape | fast set | migration check: save a ledger on `main`, switch branch, reload, nothing lost |
| Export | fast set | open the file in a spreadsheet |
| Tests or fixtures only | fast set | a mutation check for any new test |

## Manual checks (before a release)

- Search, save, reload, and export in Safari and on one phone (or devtools device mode at least): not automated.
- The page looks right with the real Tailwind CDN: the tests replace it, so they never see layout.

## Environment recipes

- **Arch and other distributions Playwright does not list:** `playwright install` prints "not officially supported"
  and uses its Ubuntu 24.04 build; Chromium and Firefox both ran this way (CachyOS, 2026-10-03).
- **The agent sandbox:** Google Books answered 429 to every anonymous request (2026-10-03). Use the end-to-end suite;
  record the live test as "skipped: 429".
- **Port 8000 is often taken** on the maintainer's machine; the automated suites pick a free port themselves.

## Known pitfalls (already hit, already fixed: don't re-discover these)

- **Saving is asynchronous.** Clicking "Commit to Ledger" returns before IndexedDB has written. Reloading at once
  cancels the write in Chromium (Firefox happened to finish), and searching at once lets the save's reset hide the
  newly staged book. The `commit()` helper waits for the save to finish; use it rather than clicking directly.
- **Tailwind's `hidden` class carries logic.** Without the CDN, nothing ever hides; the test stub keeps that one
  rule. If the app starts depending on another utility class for behaviour, add it to `TAILWIND_STUB`.
- **`file://` and `localhost` keep separate ledgers.** A book saved in one is missing in the other; it is not a load
  bug.
- **A mutation check must break the fix, not the test.** Remove just the fix.
