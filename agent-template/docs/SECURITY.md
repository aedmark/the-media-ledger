# Security

This document describes the project's security assumptions and reporting path. It is not a claim that the project
is vulnerability-free.

## Supported versions

| Version / branch | Security fixes |
| --- | --- |
| `{{version or branch}}` | {{supported / end date}} |

## Report a vulnerability

Report suspected vulnerabilities privately to {{security contact or private reporting URL}}. Include affected
versions, impact, reproduction steps, and any known workaround. Do not include real secrets or personal data.

Expected acknowledgement: {{time window}}. Disclosure policy: {{coordinated disclosure expectations}}.

## Assets and boundaries

| Asset or boundary | Sensitivity / threat | Protection and validation | Owner |
| --- | --- | --- | --- |
| {{Credentials}} | {{Account or service compromise}} | {{Secret store; never logged or committed}} | {{role}} |
| {{User input}} | {{Injection, abuse, oversized payloads}} | {{Validation, encoding, limits}} | {{component}} |
| {{Stored data}} | {{Disclosure, corruption, unsafe migration}} | {{Access control, backup, migration checks}} | {{component}} |
| {{Outbound service}} | {{Data leakage, unavailable or malicious response}} | {{Allowlist, timeout, schema validation}} | {{component}} |

Architecture details belong in [ARCHITECTURE.md](ARCHITECTURE.md); this table records the security consequence.

## Secure development rules

- Keep credentials out of code, documentation, prompts, logs, screenshots, fixtures, and error reports.
- Validate at trust boundaries and encode for the destination context. Do not rely on prompt text as a security
  control.
- Use least privilege, explicit timeouts and size limits, and safe failure defaults.
- Pin and review dependencies according to `{{dependency policy source}}`; record accepted exceptions.
- Sanitize production-derived examples and preserve only the minimum data needed for debugging.
- For authentication, authorization, cryptography, or destructive migrations, require targeted review and a
  rollback or recovery plan.

## Security verification

{{List relevant automated checks, manual review, dependency scanning, and where evidence is recorded. State gaps
plainly.}}

## Incident response

If active exploitation or secret exposure is suspected: contain access, preserve evidence without copying sensitive
data into the repository, notify {{role/contact}}, rotate affected credentials, and follow `{{runbook link}}`.
