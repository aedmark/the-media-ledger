# Roadmap

Item IDs are permanent: `P<phase>-<nn>`. Never renumber; append new items at the end of their phase.
`[ ]` open · `[~]` in progress (who holds it, since when, and what is left) · `[x]` done · `[-]` dropped (say why,
and the decision). An item held `[~]` by someone else is theirs until they or a maintainer release it.

A finished item says what was done, the decision if any, the evidence (the test, or the measurement), and the date.
A new item says where it came from (a test run, a real user, a maintainer) and the date. Keep an item's history in it:
"tried X, measured Y, then did Z" is how the next session avoids trying X again. Bugs are items too, filed under
the phase they belong to.

## Phase 1: Foundations

Goal: the existing app is safe, truthful about itself, and documented well enough to build on.

- [x] P1-01 Adopt the agent project template: AGENTS, roadmap, handoff, architecture, decisions, testing, security,
  contributing, changelog, and `tools/check_docs.py`. Evidence: `python3 tools/check_docs.py` reports 0 errors
  (2026-10-03)
- [x] P1-02 Escape book fields before rendering. Titles, authors, and other Google Books text went into `innerHTML`
  unescaped in `stageBook()` and `updateLedgerUI()`. Found by code reading during P1-01 (2026-10-03). Done: every
  field goes through `escapeHTML()`; the remove button uses a listener, because an id inside an inline `onclick`
  string cannot be made safe by HTML escaping (that also finished P4-03). Evidence: a stored record with
  `<img onerror>` in every field and a quote-breaking id rendered as text and executed nothing; with the fix
  stashed, the same check executed the payload. Chromium (built-in browser), 2026-10-03
- [ ] P1-03 Guard CSV export against spreadsheet formula injection: prefix cells beginning with `=`, `+`, `-`, `@`
  with `'`. Done when such a title opens as text in a spreadsheet. Found by code reading (2026-10-03). Test written
  ahead of the fix: `test_export_neutralises_spreadsheet_formulas`, marked `xfail(strict=True)`
- [ ] P1-04 Make the UI's claims true: the ledger subtitle says "In-memory session storage" but data persists in
  IndexedDB; the title says "Zero-Dependency" but the page loads Tailwind and Google Fonts from CDNs. Drop the false
  wording (D-004). Found by code reading (2026-10-03)
- [x] P1-05 URL-encode the ISBN query and check `response.ok` before parsing, so an HTTP error or rate limit gives a
  clear message instead of "No books found". Found by code reading (2026-10-03); the 429 case was then seen live
  during P1-02. Done: ISBN goes through `encodeURIComponent`; a 429 says Google Books is limiting searches, any other
  HTTP error names its status. Evidence: stubbed 429, 503, empty, found, and network-failure replies each gave the
  right message; a live search here (429) showed the new message; with the fix stashed, the 429 said "No books found"
  and `978&q=x#y` leaked into the URL unencoded. Chromium (built-in browser), 2026-10-03
- [x] P1-06 Search was broken for everyone: Google Books gives keyless requests a quota of 0 per day. Found while
  trying to record fixtures (P4-04), from the 429 body (2026-10-03). Done (D-008): lookups go to Open Library (Books
  API for ISBNs, search for title and author). Evidence: 38 end-to-end tests pass on recorded Open Library replies in
  Chromium and Firefox; the live tests passed 4/4 against openlibrary.org; the old Google code fails 14 tests
  (2026-10-03)

## Phase 2: Core experience

Goal: managing a ledger is quick and forgiving.

- [ ] P2-01 Pick from several search results instead of always taking the first. Done when a title search shows up to
  five candidates to choose from.
- [ ] P2-02 Detect duplicates without an ISBN (match on normalised title and author). Today two "N/A" entries are
  always allowed.
- [ ] P2-03 Edit a saved entry's fields by hand.
- [ ] P2-04 Sort and filter the ledger (title, author, year).

## Phase 3: Output / sharing

- [ ] P3-01 Import a CSV previously exported by the app, without duplicating existing entries.
- [ ] P3-02 Export and import a full JSON backup that round-trips every field.

## Phase 4: Quality: speed, accessibility, robustness

- [x] P4-01 Automated end-to-end smoke test (headless browser, Google Books stubbed) run locally and in CI. Done when
  the manual smoke steps in `docs/TESTING.md` are automated and a deliberately broken save fails it.
  Done (D-007): Playwright for Python with pytest, Chromium and Firefox, Google Books from fixtures, CI on GitHub
  Actions. 15 tests per browser cover the manual smoke steps, error messages (P1-05), and injection (P1-02).
  Evidence: 30 passed three runs in a row; breaking the save failed 5 tests, removing escaping failed 1, removing the
  P1-05 checks failed 3 (2026-10-03)
- [ ] P4-02 Accessibility pass: the remove button has only a `title`, toasts are not announced to screen readers, and
  keyboard focus is unchecked.
- [x] P4-03 Replace the inline `onclick="removeBook(...)"` with an event listener so a Content-Security-Policy can
  forbid inline handlers. Done with P1-02, which needed it (2026-10-03). The Tailwind CDN script still stands
  in the way of a strict policy.
- [x] P4-04 Replace the three synthetic Google Books fixtures with recorded replies: run `tools/record_fixtures.py`
  from a network Google is not rate-limiting, then rerun the suite. Needs the maintainer's network: Google answered
  429 from the agent's (2026-10-03). The maintainer's run also got 429, which exposed P1-06. Done with P1-06: four
  Open Library replies recorded by the agent (2026-10-03); two fixtures stay synthetic by design

## Phase 5: Later: other media and offline

Starts after Phase 4. P5-01 is intended (D-006); the rest is not committed.

- [ ] P5-01 Track collectible visual media: VHS, DVD, Blu-ray, and similar (D-006). Needs a media type on each
  record with a migration from IndexedDB version 1, a lookup source for films, and per-format fields.
- [ ] P5-02 Work offline as an installable app (service worker, self-hosted CSS).

## Phase 6: Non-code items (name, domain, brand)

- [ ] P6-01 Settle the name: "Library Ledger" in the UI versus `the-media-ledger` for the repository, once P5-01 is near (D-006).
