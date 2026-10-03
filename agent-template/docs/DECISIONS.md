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

## D-001 {{The first architectural choice, e.g. "Static site, no build step"}}  ({{YYYY-MM-DD}}, status: accepted)
**Context:** {{...}}
**Decision:** {{...}}
**Alternatives:** {{...}}
**Consequences:** {{...}}

## Open questions

Questions requiring maintainer or stakeholder input. This is their one home: HANDOFF and the roadmap refer to them by ID. Numbers are
permanent; an answered question stays, with the answer and its date.

```
- **Q-NNN** The question. (asked YYYY-MM-DD, by whom; blocks P1-NN; recommendation: ...)
- **Q-NNN** ~~The question.~~ Answered YYYY-MM-DD: the answer, D-NNN.
```

- **Q-001** {{A question not answered yet.}} ({{asked YYYY-MM-DD; blocks which item; recommendation}})
