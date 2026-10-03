# Security

This document describes the project's security assumptions and reporting path. It is not a claim that the project
is vulnerability-free.

## Supported versions

| Version / branch | Security fixes |
| --- | --- |
| `main` | supported |

## Report a vulnerability

Report suspected vulnerabilities privately through GitHub's private vulnerability reporting on
<https://github.com/aedmark/the-media-ledger/security>. Include the browser, impact, and reproduction steps. Do not
include anyone's real ledger. This is a hobby project: expect an acknowledgement within two weeks, and please allow a
fix before public disclosure.

## Assets and boundaries

| Asset or boundary | Sensitivity / threat | Protection and validation | Owner |
| --- | --- | --- | --- |
| The user's ledger | Reading habits are personal; script injection could read or wipe it | Stays in the browser's IndexedDB; nothing uploads it | storage code |
| Open Library reply | Untrusted text rendered into the page: script injection (stored, since it is saved) | `escapeHTML()` on every field in `stageBook()` and `updateLedgerUI()`; no inline handlers (P1-02) | rendering code |
| Search query | Disclosed to Open Library (Internet Archive) | Inherent to D-008; documented in README | search handler |
| CSV export | Formula injection when opened in a spreadsheet | Quotes doubled; formulas not neutralised (P1-03) | export handler |
| CDN scripts | A compromised CDN runs code with full page access | Unpinned, no Subresource Integrity; pin with the next dependency proposal (D-004) | maintainer |

Architecture details belong in [ARCHITECTURE.md](ARCHITECTURE.md); this table records the security consequence.

## Secure development rules

- Keep credentials out of code, documentation, prompts, logs, screenshots, and fixtures. The app needs none; adding
  an API key to a static public page would publish it.
- Render external or stored text with `textContent` or an escaping helper, never by interpolating into `innerHTML`.
- Encode values for their destination: `encodeURIComponent` for URLs, formula-safe quoting for CSV.
- Any new outbound request or new third-party script needs maintainer approval and an entry in ARCHITECTURE.md.
- Prefer event listeners over inline `onclick` attributes so a Content-Security-Policy stays possible (P4-03, done).

## Security verification

Manual only: code review against the rules above, and the injection checks in [TESTING.md](TESTING.md). No automated
security tests or dependency scanning exist yet (P4-01).

## Incident response

If a vulnerability is being exploited: fix on a branch, ask the maintainer to merge, note it in the CHANGELOG once
fixed, and tell users how to export and check their ledger. There are no credentials to rotate.
