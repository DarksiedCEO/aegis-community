from helpers import ValidatorTestCase, add_fixture_tests


class AuthorityBoundaryTests(ValidatorTestCase):
    def test_positive_canonical_authority(self) -> None:
        self.assertAccepted("scripts/validate_registry.py")


FIXTURES = {
    "aegis_implementation": ("AEGIS implementation authority is forbidden", ["scripts/validate_registry.py", "--fixture", "tests/fixtures/pr3/registry/aegis-implementation-authority.json"]),
    "project_manager_certification": ("Project Manager certification authority is forbidden", ["scripts/validate_registry.py", "--fixture", "tests/fixtures/pr3/registry/project-manager-certification.json"]),
    "completion_certification": ("Completion Controller certification authority is forbidden", ["scripts/validate_registry.py", "--fixture", "tests/fixtures/pr3/registry/completion-controller-certification.json"]),
    "evidence_signing": ("Evidence Guardian signing authority is forbidden", ["scripts/validate_registry.py", "--fixture", "tests/fixtures/pr3/registry/evidence-guardian-signing.json"]),
    "evidence_certification": ("Evidence Guardian certification authority is forbidden", ["scripts/validate_registry.py", "--fixture", "tests/fixtures/pr3/registry/evidence-guardian-certification.json"]),
    "human_override": ("human approval authority cannot be overridden", ["scripts/validate_registry.py", "--fixture", "tests/fixtures/pr3/registry/human-authority-override.json"]),
    "enterprise_leakage": ("private Enterprise implementation reference", ["scripts/validate_registry.py", "--fixture", "tests/fixtures/pr3/registry/community-enterprise-leakage.json"]),
}
add_fixture_tests(AuthorityBoundaryTests, "authority", FIXTURES)
