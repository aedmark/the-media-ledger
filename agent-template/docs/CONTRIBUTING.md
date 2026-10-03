# Contributing

Use this file for the workflow shared by human and automated contributors. Agent-specific standing instructions are
in [AGENTS.md](../AGENTS.md).

## Before changing code

1. Read the README, relevant roadmap item, architecture section, and test guidance.
2. Follow the setup in `{{setup source or command}}`.
3. Check `git status` and confirm that your change will not overlap unrelated work.
4. For a large or irreversible change, agree on scope and rollback before implementation.

## Make the change

- Keep each change reviewable and focused on one outcome.
- Preserve compatibility unless the roadmap or an accepted decision explicitly allows a break.
- Add or update tests for changed behaviour. Make a new test fail for the intended reason before trusting it.
- Update documentation according to [the documentation triggers](README.md#update-triggers).
- Do not include credentials, personal data, generated caches, or local configuration.

## Verify

```bash
{{fast verification command}}
{{full verification command}}
```

Follow [TESTING.md](TESTING.md) for prerequisites and suite limitations. Report the exact checks run and any checks
skipped; a partial pass is not a full pass.

## Submit and review

{{Describe branch naming, commit conventions, pull-request requirements, CI, review authority, and merge method.}}

A change is ready when its scope is clear, relevant checks pass, user and migration impact is described, sensitive
data is absent, and the documentation it invalidated has been updated.

## Compatibility and migrations

{{State the compatibility promise. For schema, API, or stored-data changes, require forward steps, rollback or
recovery, and verification. Link to a runbook when one exists.}}

## Reporting security issues

Do not open a public issue for a suspected vulnerability. Follow [SECURITY.md](SECURITY.md).
