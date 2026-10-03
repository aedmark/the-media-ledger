# Testing

How to run every check, what each one proves, and what it cannot. Read this before claiming anything works.
The results themselves live in HANDOFF's "Current state"; this file is how to get them.

## The suites

| Suite | File | Proves | Does not prove | Time, needs |
| --- | --- | --- | --- | --- |
| Docs check | `tools/check_docs.py` | roadmap IDs, decisions, questions, links, and session numbers are consistent | anything about the app | a second, Python 3 |
| Manual smoke test | this file, "Running each suite" | a person's path through the app works in one browser | other browsers; edge cases not listed | five minutes, a browser and network |

There are no automated app tests yet (P4-01).

**The fast set** (before every commit): `python3 tools/check_docs.py`.
**The full set** (any change to `index.html`, and before merging): the fast set plus the manual smoke test.

**Expected results** live in HANDOFF's "Verified" table, with the date and commit they were measured on.

## Before any run

- **Clean state:** use a fresh origin or clear it: devtools > Application > Storage > "Clear site data" for
  `http://localhost:8000`. A leftover ledger can hide a broken load or trip the duplicate check. Never clear site
  data in a browser profile that holds someone's real ledger; use a private window instead.
- **Services it needs:** network access to `www.googleapis.com`, and a local server:
  `python3 -m http.server 8000`. It is up when `http://localhost:8000/` shows the page.

## Running each suite

### Docs check

```bash
python3 tools/check_docs.py
```

- A pass is a final line with `0 error(s)`; exit code 0. Warnings do not fail it.

### Manual smoke test

```bash
python3 -m http.server 8000
```

Open `http://localhost:8000/` in a private window with the devtools console open, then:

1. Search ISBN `9780439708180`; a staged book appears with a title and author.
2. Commit it; it appears in the list and an emerald toast shows.
3. Commit the same ISBN again; an info toast says it is already in the ledger and the list is unchanged.
4. Switch to Title & Author, search `Dune` / `Frank Herbert`, and commit.
5. Reload the page; both books are still listed.
6. Export CSV; the file has a header row and two data rows.
7. Remove one book, reload; only one remains.
8. Search an ISBN that does not exist (`0000000000`); an error toast shows and nothing is staged.

A pass is every step as described and no uncaught errors in the console.

### Injection checks (P1-02; the CSV part waits for P1-03)

Google Books data cannot be chosen, so inject a hostile record directly. In the console on the page:

```js
const t = db.transaction(["books"], "readwrite");
t.objectStore("books").add({id: "x1", title: '<img src=x onerror=alert(1)>', author: '=1+1', isbn: "N/A",
  publishedYear: "2000", pages: 1});
t.oncomplete = () => location.reload();
```

A pass: no alert appears and the title shows as literal text; in the exported CSV the author cell opens as the text
`=1+1`, not `2`. Delete the record afterwards.

### Adding a check

- Until P4-01 lands, add steps to the smoke test above, each with its expected result.
- Assert on what happened (a row in the list, a record in IndexedDB, a cell in the CSV), not on toast wording.
- Before trusting a new check, make it fail: undo the fix (only the fix) and run it.

## Runs that vary

Searches depend on Google Books, which can change its results or rate-limit anonymous use. A failed search step is
first a network question: open the request in devtools and record the HTTP status before blaming the code. Prefer
the injection approach above to rerunning searches until a rare reply appears.

## Change-to-check matrix

| Changed area | Minimum checks | Additional evidence |
| --- | --- | --- |
| Documentation only | `python3 tools/check_docs.py` | none |
| Rendering or search | docs check; smoke test | injection checks |
| Storage or record shape | docs check; smoke test with a ledger saved by the previous version | migration check: save on `main`, switch branch, reload, nothing lost |
| Export | smoke test step 6 | injection checks; open the file in a spreadsheet |

## Manual checks (before a release)

- Smoke test in Chrome, Firefox, and Safari, and on one phone width (devtools device mode at least).

## Environment recipes

- The agent sandbox may block network access: if every search fails with the network toast, record the smoke test as
  "not run: no network" rather than as a failure.
- Google Books may answer `429` to anonymous requests from a sandbox or a shared IP (seen 2026-10-03); the app then
  says Google Books is limiting searches (P1-05). To still exercise steps 1 to 8, replace
  `window.fetch` in the console with a function returning `{ok: true, json: async () => ({totalItems: 1, items:
  [{volumeInfo: {...}}]})}`; record the run as "stubbed search", since it does not prove the live API works.
- To test export without downloading a file, wrap `URL.createObjectURL` to keep the Blob and read it with
  `await blob.text()`.

## Known pitfalls (already hit, already fixed: don't re-discover these)

- **`file://` and `localhost` keep separate ledgers.** A book saved in one is missing in the other; it is not a load
  bug.
- **A mutation check must break the fix, not the test.** Remove just the fix.
