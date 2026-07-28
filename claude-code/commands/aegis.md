---
description: Run a read-only AEGIS assessment of this repository or a named subject
---

Run an independent AEGIS assessment. Read-only — change nothing.

Subject: $ARGUMENTS
(If empty, the subject is the current repository at its current HEAD.)

Proceed in this order and do not skip ahead:

1. **Pin the subject.** Branch, HEAD SHA, upstream, working-tree status, remote
   URL, and remote HEAD. Report local-versus-remote divergence explicitly before
   anything else.

2. **Inventory before judging.** What actually exists — files, entry points,
   tests, CI configuration. Count them. An assessment that starts with an opinion
   has skipped this.

3. **Hunt the fake-green catalog.** Placeholder bodies (`pass`, `TODO`, constant
   returns), suppressed failures (`|| true`, `continue-on-error`, disabled tests,
   recently grown ignore files), scanners with zero scanned files, evidence bound
   to a different commit, and any claim whose only provenance is a prior
   conversation.

4. **Grade every claim E0–E5** and evaluate each gate separately against its
   required level. Never aggregate gate results.

5. **Issue one verdict** from the contract: CERTIFIED, CONDITIONAL,
   NOT_CERTIFIED, INSUFFICIENT_EVIDENCE, or REFUSED.

6. **List everything unverified.** This section is mandatory and must not be
   empty.

If the subject cannot be pinned, or evidence contradicts itself, stop and report
rather than proceeding on an assumption.
