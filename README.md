# AEGIS Community

AEGIS Community is the public cross-platform skill and agent operating layer for
evidence-first engineering assurance. It contains model instructions, role
contracts, strict output schemas, dependency-free validators, and example
workflows for Codex, ChatGPT, Claude, and Claude Code.

It is not the standalone AEGIS platform. This repository contains no production
certification service, API, database, dashboard, cloud infrastructure, signing
system, CLI product, or SDK product.

## Operating model

- Roles own one coordination or control responsibility.
- Skills provide reusable behavior inside a role's authority.
- Completion controllers evaluate closure but do not certify.
- AEGIS independently assesses but does not implement its subject.
- Andre retains material approval authority.

See [the role guide](agents/README.md), [the skill guide](skills/README.md), and
[the operating workflow](docs/OPERATING_WORKFLOW.md).

## Local validation

Requires CPython 3.11 or newer and uses only the standard library:

```bash
python3.11 tests/run_all.py
```

The runner fails if it discovers zero tests, a negative fixture unexpectedly
passes, a required validation family is skipped, or any test raises an exception.
Local validation is local evidence; it is not remote CI or certification.

## Community and Enterprise

Community defines portable public contracts. Private Enterprise overlays may
apply stricter internal instructions but cannot silently redefine Community
capabilities, licensing, role ownership, or AEGIS independence.
