# Google Books replies used by the tests

The tests never call Google: `tests/conftest.py` answers every request to the volumes endpoint from these files.

| File | Answers the query | Source |
| --- | --- | --- |
| `isbn_9780439708180.json` | `isbn:9780439708180` | synthetic, in Google's shape; replace by recording |
| `title_dune_author_frank_herbert.json` | `intitle:Dune+inauthor:Frank Herbert` | synthetic, in Google's shape; replace by recording |
| `empty.json` | anything with no results | synthetic, in Google's shape; replace by recording |
| `no_isbn.json` | a volume without `industryIdentifiers` | synthetic, always; Google cannot be made to return it on demand |
| `hostile.json` | HTML and spreadsheet formulas in every text field | synthetic, always: an attack fixture |

Synthetic volume ids start with `SYNTHETIC-`. To replace the first three with real replies, run
`python3 tools/record_fixtures.py` from a network Google is not rate-limiting, review the diff, and update the
"Source" column. Recorded replies are trimmed to the fields the app reads, so they stay small and stable.
