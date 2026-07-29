from helpers import ValidatorTestCase, add_fixture_tests


class SchemaValidationTests(ValidatorTestCase):
    def test_positive_schema_inventory(self) -> None:
        self.assertAccepted("scripts/validate_skills.py")

    def test_positive_agent_output(self) -> None:
        self.assertAccepted("scripts/validate_skills.py", "--kind", "agent-output", "--document", "tests/fixtures/pr3/documents/valid-agent-output.json")

    def test_positive_handoff(self) -> None:
        self.assertAccepted("scripts/validate_skills.py", "--kind", "handoff", "--document", "tests/fixtures/pr3/documents/valid-handoff.json")

    def test_positive_evidence(self) -> None:
        self.assertAccepted("scripts/validate_skills.py", "--kind", "evidence-label", "--document", "tests/fixtures/pr3/documents/valid-evidence-label.json")

    def test_positive_completion(self) -> None:
        self.assertAccepted("scripts/validate_skills.py", "--kind", "completion-manifest", "--document", "tests/fixtures/pr3/documents/valid-completion-manifest.json")


FIXTURES = {
    "invalid_agent": ("must not be empty", ["scripts/validate_skills.py", "--kind", "agent-output", "--document", "tests/fixtures/pr3/documents/invalid-agent-output.json"]),
    "invalid_handoff": ("missing fields", ["scripts/validate_skills.py", "--kind", "handoff", "--document", "tests/fixtures/pr3/documents/invalid-handoff.json"]),
    "unknown_handoff_field": ("unknown fields", ["scripts/validate_skills.py", "--kind", "handoff", "--document", "tests/fixtures/pr3/documents/invalid-handoff-unknown-field.json"]),
    "malformed_json": ("cannot parse JSON", ["scripts/validate_skills.py", "--kind", "handoff", "--document", "tests/fixtures/pr3/documents/malformed.json"]),
    "invalid_evidence": ("evidence.evidence_level: invalid", ["scripts/validate_skills.py", "--kind", "evidence-label", "--document", "tests/fixtures/pr3/documents/invalid-evidence-label.json"]),
    "invalid_completion": ("must not be empty", ["scripts/validate_skills.py", "--kind", "completion-manifest", "--document", "tests/fixtures/pr3/documents/invalid-completion-manifest.json"]),
    "self_review": ("source and target roles must differ", ["scripts/validate_skills.py", "--kind", "handoff", "--document", "tests/fixtures/pr4/documents/self-review-handoff.json"]),
    "missing_subject": ("exact subject identity required", ["scripts/validate_skills.py", "--kind", "completion-manifest", "--document", "tests/fixtures/pr4/documents/completion-missing-subject.json"]),
    "missing_evidence": ("verified closure requires evidence", ["scripts/validate_skills.py", "--kind", "completion-manifest", "--document", "tests/fixtures/pr4/documents/completion-missing-evidence.json"]),
    "wrong_subject": ("wrong-subject evidence", ["scripts/validate_skills.py", "--kind", "evidence-label", "--document", "tests/fixtures/pr4/documents/wrong-subject-evidence.json"]),
    "stale_evidence": ("stale evidence predates subject change", ["scripts/validate_skills.py", "--kind", "evidence-label", "--document", "tests/fixtures/pr4/documents/stale-evidence.json"]),
    "unknown_truth": ("truth_label: invalid", ["scripts/validate_skills.py", "--kind", "evidence-label", "--document", "tests/fixtures/pr4/documents/unknown-truth-label.json"]),
    "illegal_extension": ("unknown fields", ["scripts/validate_skills.py", "--kind", "handoff", "--document", "tests/fixtures/pr4/documents/illegal-extension.json"]),
    "schema_mismatch": ("expected 1.0.0", ["scripts/validate_skills.py", "--kind", "handoff", "--document", "tests/fixtures/pr4/documents/schema-version-mismatch.json"]),
}
add_fixture_tests(SchemaValidationTests, "schema", FIXTURES)
