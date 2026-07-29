# Example: implementation handoff

This is a fictional format example, not evidence of executed work.

```json
{
  "schema_version": "1.0.0",
  "registry_version": "1.0.0",
  "handoff_id": "example-handoff-001",
  "source_role": "project-manager",
  "target_role": "test-authenticity-guardian",
  "subject": "commit:0123456789abcdef0123456789abcdef01234567",
  "status": "implemented_not_verified",
  "artifacts": ["example:agents/project-manager.md"],
  "evidence": [],
  "warnings": ["No independent test run has occurred."],
  "unresolved_risks": ["The implementation may not satisfy its contract."],
  "next_required_action": "Run the approved validation command on the exact subject.",
  "approval_required": false
}
```

The example does not say the implementation passed, is complete, or is certified.
