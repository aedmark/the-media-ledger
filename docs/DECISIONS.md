# Decisions

Short, append-only record of choices that a future session might otherwise re-litigate. One entry per decision.
Newest at the bottom. To reverse a decision, add a new entry that supersedes it; the old one keeps its text and only
its status changes ("superseded by D-MMM"). An "Update, same session" note at the end of an entry is fine while it is
still on the working branch.

Record pre-existing choices too, the first time a session has to understand them ("status: accepted, recorded
YYYY-MM-DD"): the reason something is the way it is gets lost faster than the code.

Format:

```
## D-NNN Title  (YYYY-MM-DD, status: proposed | accepted | rejected | superseded by D-MMM)
**Context:** why this came up (the roadmap item, the bug, the measurement).
**Decision:** what we chose (numbered points if there are several).
**Alternatives:** what else was considered, and why not (one line each). Optional, but it is what stops the
re-litigation.
**Consequences:** what it costs or constrains; what was left out and why.
**Review trigger:** an event that should cause reconsideration. Optional.
```

---

## D-001 One static HTML file, no build step  (2026-08-20, status: accepted, recorded 2026-10-03)
**Context:** The app was created as a single `index.html` in the second commit (`0fed6b3`). Recorded during P1-01.
**Decision:** Markup, styles, and script live in `index.html`. No framework, bundler, or npm runtime dependencies.
Styling uses Tailwind via its CDN script.
**Alternatives:** A Vite/npm project (more tooling than a one-screen app needs); separate `.js`/`.css` files (worth
it once the script outgrows one screen; ask the maintainer first).
**Consequences:** Anyone can run it by opening a file or serving the folder. Code cannot be unit-tested in isolation
without extracting it; tests drive the page in a browser (TESTING.md). The Tailwind Play CDN is not meant for
production (Q-001).
**Review trigger:** the inline script passes about 600 lines, or a second page is needed.

## D-002 Google Books API without a key  (2026-08-20, status: superseded by D-008, recorded 2026-10-03)
**Context:** The app needs book metadata from an ISBN or a title. The code comment says the API was chosen as
"highly reliable, CORS friendly, and requires no key for basic queries".
**Decision:** Query `https://www.googleapis.com/books/v1/volumes` directly from the browser, unauthenticated, and use
the first result.
**Alternatives:** Open Library (also keyless; not evaluated yet); a keyed API (would put a secret in a public page).
**Consequences:** Subject to Google's anonymous rate limits; the search text is sent to Google. No secret ever needs
to be handled.
**Review trigger:** frequent rate-limit errors, or a wish to stop sending queries to Google.

## D-003 Ledger stored in IndexedDB, schema version 1  (2026-08-20, status: accepted, recorded 2026-10-03)
**Context:** Saved books must survive a reload without a server.
**Decision:** Database `LibraryLedgerDB`, version 1, object store `books` with `keyPath: "id"`; record shape as in
ARCHITECTURE.md "Interfaces and data flow". `id` is `Date.now()` as a string.
**Alternatives:** `localStorage` (synchronous, small quota, strings only).
**Consequences:** Data is per browser and per origin (`file://` and `http://localhost` are different ledgers). Any
change to names or record shape needs an `onupgradeneeded` migration from version 1.

## D-004 Outside dependencies by proposal  (2026-10-03, status: accepted)
**Context:** Q-001; the page title claimed "zero-dependency" while loading two CDNs.
**Decision:** 1. Outside dependencies (libraries, CDN scripts, fonts, APIs) are allowed when they earn their place.
2. An agent proposes one with what it is for, its size, and the alternative of writing it; the maintainer approves
before it is added. 3. Approved ones are recorded in ARCHITECTURE.md "Dependencies", pinned to a version. 4. The UI
stops calling itself zero-dependency (P1-04).
**Alternatives:** strict zero-dependency (self-host everything; more work than the app needs today).
**Consequences:** D-001's "no npm runtime dependencies" now means "none without approval"; a build step is still a
separate decision.

## D-005 Version numbers for git, not for users  (2026-10-03, status: accepted)
**Context:** Q-002.
**Decision:** 1. Releases are annotated git tags `vMAJOR.MINOR.PATCH` on `main` (semantic versioning; `v0.x` until
the stored data shape is considered stable). 2. The maintainer cuts tags. 3. A release renames CHANGELOG's
"Unreleased" to the version and date; the version bump itself is never a changelog entry, a UI notice, or a
"what's new" message.
**Alternatives:** no versions (harder to say which build a bug was seen on); a version shown in the UI (not wanted).
**Consequences:** HANDOFF and bug reports cite a tag or commit.

## D-006 Books first, then collectible visual media  (2026-10-03, status: accepted)
**Context:** Q-003; the repository is `the-media-ledger` but the app only handles books.
**Decision:** 1. Phases 1 to 4 are books only. 2. VHS, DVD, Blu-ray, and other collectible visual media are an
intended later scope (P5-01), not a maybe. 3. Until then, book work should not make that harder: avoid baking
"book" into new stored field names or shared helpers where a neutral name costs nothing.
**Alternatives:** generalise now (premature: no second lookup source chosen); stay books-only forever (not wanted).
**Consequences:** P5-01 will need a `mediaType` on records, a database version bump with migration (D-003), and a
lookup source for films; the product name is revisited with it (P6-01).

## D-007 End-to-end tests with Playwright for Python, Google Books answered from fixtures  (2026-10-03, status: accepted)
**Context:** P4-01. Google Books answered 429 to every anonymous request from the development machine, so manual
searches could not verify anything; the maintainer asked for testing that does not depend on Google.
**Decision:** 1. Tests drive the real `index.html` in headless Chromium and Firefox through Playwright for Python
with pytest, pinned in `requirements-dev.txt`. 2. Every request to Google Books is answered from JSON fixtures;
Tailwind is stubbed; any other outside request fails the test. 3. One live test, skipped unless `LIVE=1`, checks the
real API; a 429 skips it. 4. GitHub Actions runs the docs check and the suite on pull requests and on `main`.
5. Development tools only: users load none of it, and `index.html` has no test hooks.
**Alternatives:** Playwright for Node (adds a Node toolchain to a repo that already uses Python); hand-pasted console
stubs (manual, unrepeatable); a Google API key for tests (still networked, and a secret to manage).
**Consequences:** Developers need a virtualenv and about 650 MB of cached browsers. Fixtures can drift from Google's
real replies; `tools/record_fixtures.py` refreshes them, and the live test catches a changed shape. Safari is not
covered (WebKit is not installed by default).
**Update, same session:** the 429s were not a rate limit (D-008). The design is unchanged, but the fixtures,
recorder, and live test now cover Open Library instead of Google Books.

## D-008 Open Library replaces Google Books  (2026-10-03, status: accepted)
**Context:** Every keyless Google Books request answered 429. The reply body showed why: the shared project that
keyless calls count against has a limit of **0 queries per day** (`quota_limit_value: "0"`, `defaultPerDayPerProject`,
project 624717413613), so search was broken for every user on every network, not rate-limited. Found during P4-04.
**Decision:** 1. Look books up at Open Library (`openlibrary.org`), keyless; it allows requests from any web page.
2. ISBN: the Books API (`/api/books?bibkeys=ISBN:...&jscmd=data`), which returns that exact edition. 3. Title and
author: `search.json` with `title`/`author`, first result. It returns a *work*, so the saved ISBN is one of the work's
editions (an ISBN-13 if any), and the year is the work's first publication. 4. The stored record shape is unchanged
(D-003).
**Alternatives:** Google with an API key restricted to the Books API and the site's domains (needs a Cloud account; the
key ships in the page); Open Library with Google as a fallback (two sources to maintain and test).
**Consequences:** Data quality is Open Library's: titles keep their catalogue casing ("Harry Potter and the sorcerer's
stone"), and page counts can be odd (784 for that edition). Search text is now disclosed to the Internet Archive instead
of Google. Open Library asks heavy users to identify themselves; a browser cannot set a User-Agent, which is fine at
this scale.
**Review trigger:** Open Library rate limits real users, or missing books are reported often.

## Open questions

Questions requiring maintainer or stakeholder input. This is their one home: HANDOFF and the roadmap refer to them by ID. Numbers are
permanent; an answered question stays, with the answer and its date.

```
- **Q-NNN** The question. (asked YYYY-MM-DD, by whom; blocks P1-NN; recommendation: ...)
- **Q-NNN** ~~The question.~~ Answered YYYY-MM-DD: the answer, D-NNN.
```

- **Q-001** ~~Should "zero-dependency" be made true or dropped from the title?~~ Answered 2026-10-03 by the
  maintainer: outside dependencies are fine when proposed and approved; drop the wording, D-004.
- **Q-002** ~~Is a version number or release process wanted?~~ Answered 2026-10-03 by the maintainer: versions for
  git tracking, not advertised to users, D-005.
- **Q-003** ~~Books only, or all media?~~ Answered 2026-10-03 by the maintainer: books first; VHS, DVD, Blu-ray and
  other collectible visual media later, D-006.
- **Q-004** How is the site deployed? Vercel posts preview deployments on every pull request (seen on #1 and #2),
  but nothing in the repository configures it. Is `main` deployed to production, and at what address? (asked
  2026-10-03, by Claude during P4-01; blocks nothing; recommendation: record the answer in ARCHITECTURE and AGENTS)
