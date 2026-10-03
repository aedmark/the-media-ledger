# Architecture

How {{PROJECT}} fits together, for a session that has never seen it. This is the map, not the territory: it names
the parts and the rules between them, and leaves the detail to the code. Keep it short enough to read in five
minutes; update it when the shape changes (a module added, moved or merged), not for every change inside one.

Why things are this way lives in [DECISIONS.md](DECISIONS.md); this file says *what* is, and points there.

## The shape, in one paragraph

{{What happens when someone uses it, end to end: e.g. "The browser loads `index.html`, which imports `src/app.js`;
input goes through the parser (`src/parse/`) into a document model, which the renderer draws and the store saves to
IndexedDB. Nothing leaves the device."}}

## Code map

Where to look for what. One row per area a session might need to find; name the entry point, not every file.

| Area | Where | Entry point | Talks to |
| --- | --- | --- | --- |
| {{Parser}} | `{{src/parse/}}` | `{{parse()}}` | {{the model; nothing else}} |
| {{Storage}} | `{{src/store/}}` | `{{open()}}` | {{IndexedDB}} |

## Interfaces and data flow

Describe stable interfaces and the direction data moves. Link to generated API or schema documentation instead of
copying it here.

```text
{{input}} -> {{validation}} -> {{domain operation}} -> {{persistence/output}}
```

| Interface | Producer | Consumer | Contract / compatibility |
| --- | --- | --- | --- |
| {{event, API, file, function}} | {{component}} | {{component}} | {{schema, versioning, error semantics}} |

## Invariants

Rules that hold everywhere and that a change must not break. Each names what enforces it; a rule nothing enforces
says so, and is a candidate for a test or a roadmap item.

- {{e.g. "The parser never touches the DOM." Enforced by: `{{test/structure.js}}`, "parse imports". (D-NNN)}}
- {{e.g. "Every write goes through the store; nothing else calls IndexedDB." Enforced by: nothing yet (P4-NN).}}

## Boundaries

Where outside data comes in (a user, a file, a model, the network) and what is trusted on each side.

| Boundary | Comes in as | Checked by | Rule |
| --- | --- | --- | --- |
| {{User text}} | {{string from the editor}} | {{`sanitize()`}} | {{never on a command line; never as HTML}} |
| {{Model reply}} | {{JSON}} | {{schema check}} | {{a reply that fails the check is refused, not repaired}} |

## Dependencies

Everything the project needs that it did not write. A new one needs {{maintainer approval}}; record it here the same
session.

| Dependency | Version | For | Why this one (and not writing it) |
| --- | --- | --- | --- |
| {{name}} | {{pinned version}} | {{what uses it}} | {{one line, or D-NNN}} |

## State and caches

Everything a run leaves on disk or elsewhere, and what may delete it. Losing a cache nobody knew was there is how a
week of measurements disappears.

| What | Where | Written by | Reset by | Committed? |
| --- | --- | --- | --- | --- |
| {{User data}} | `{{path}}` | {{the app}} | {{`reset` clears it}} | {{no, gitignored}} |
| {{Cached model runs}} | `{{path}}` | {{the harness}} | {{by hand only; `reset` must not touch it}} | {{no}} |

## Failure modes and observability

| Failure | User-visible behaviour | Detection | Recovery / runbook |
| --- | --- | --- | --- |
| {{dependency unavailable}} | {{degraded mode or error}} | {{metric, log, test}} | {{retry, rollback, link}} |

State what may be logged and what must be redacted. Security consequences and reporting belong in
[SECURITY.md](SECURITY.md).

## Claims vs. code

Places where a doc, a name or a comment says more than the code does, so nobody builds on the claim. Remove a row
when the code catches up or the claim is corrected.

- {{e.g. "`physics/` suggests a simulation; it is a set of thresholds feeding prompt text."}}
