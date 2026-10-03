# Changelog

User-visible changes, newest first, in plain words: what someone using Library Ledger would notice. This is not a
copy of the git log or session log, which serve developers. Add to "Unreleased" as changes land; on a release, rename
it to the version tag and date and start a new section. The version bump itself is not an entry (D-005).

## Unreleased

<!-- Keep only headings that contain entries. Security-sensitive fixes may need coordinated wording and timing. -->

### Added
- Look up books by ISBN or by title and author, save them to a ledger kept in your browser, remove them, and export
  the ledger as CSV.

### Fixed
- Book details containing HTML could run script in the page; they are now always shown as plain text.
- Searching works again. Google Books stopped answering requests without a key, so every search failed; books are
  now looked up at Open Library. Titles may use the library catalogue's capitalisation.
- When the book service is busy or returns an error, the app now says so instead of "No books found".
- ISBN searches containing characters such as `&` or `#` are now sent correctly.
