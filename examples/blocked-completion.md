# Example: blocked completion

This is a fictional status example, not evidence of a real blocker.

```text
SUBJECT: commit:0123456789abcdef0123456789abcdef01234567
STATUS: blocked
REQUIREMENT: REQ-TEST-001
OBSERVATION: zero tests were discovered
TRUTH LABEL: OBSERVED
EVIDENCE LEVEL: E3
STOP CONDITION: required validation family did not execute
NEXT ACTION: correct discovery configuration and rerun without suppression
```

The execution may have exited successfully, but zero discovery blocks completion.
The controller must not relabel this state `verified` or `closed`.
