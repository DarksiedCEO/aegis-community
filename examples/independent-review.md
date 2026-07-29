# Example: independent review

This is a fictional workflow example, not evidence of an executed review.

The implementer hands exact candidate
`commit:0123456789abcdef0123456789abcdef01234567` to a different validation
identity. The validator records the command, environment, exit status, discovered
test count, raw output location, and candidate SHA. Evidence and Truth Guardian
labels the resulting recorded execution E3. It does not upgrade it to E4 because
another environment has not independently reproduced it.

AEGIS then checks independence, subject binding, required gates, and unverified
claims. If necessary evidence is missing, the bounded verdict is
`INSUFFICIENT_EVIDENCE`; missing evidence never becomes a pass.
