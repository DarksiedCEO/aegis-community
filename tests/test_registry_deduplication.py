from helpers import ValidatorTestCase, add_fixture_tests


class RegistryDeduplicationTests(ValidatorTestCase):
    def test_positive_canonical_registry(self) -> None:
        self.assertAccepted("scripts/validate_registry.py")


FIXTURES = {
    "duplicate_role": ("duplicate role IDs", ["scripts/validate_registry.py", "--fixture", "tests/fixtures/pr3/registry/duplicate-role-id.json"]),
    "duplicate_capability": ("duplicate capability IDs", ["scripts/validate_registry.py", "--fixture", "tests/fixtures/pr3/registry/duplicate-capability-id.json"]),
    "duplicate_owner": ("duplicate capability ownership", ["scripts/validate_registry.py", "--fixture", "tests/fixtures/pr3/registry/duplicate-capability-owner.json"]),
    "unknown_owner": ("unknown owner", ["scripts/validate_registry.py", "--fixture", "tests/fixtures/pr3/registry/unknown-capability-owner.json"]),
    "missing_contract": ("missing contract", ["scripts/validate_registry.py", "--fixture", "tests/fixtures/pr3/registry/missing-role-contract.json"]),
    "empty_roles": ("agent registry must not be empty", ["scripts/validate_registry.py", "--fixture", "tests/fixtures/pr3/registry/empty-role-registry.json"]),
    "empty_capabilities": ("capability registry must not be empty", ["scripts/validate_registry.py", "--fixture", "tests/fixtures/pr3/registry/empty-capability-registry.json"]),
    "duplicate_alias": ("duplicate canonical capability aliases", ["scripts/validate_registry.py", "--fixture", "tests/fixtures/pr4/registry/duplicate-alias.json"]),
    "version_mismatch": ("registry version mismatch", ["scripts/validate_registry.py", "--fixture", "tests/fixtures/pr4/registry/version-mismatch.json"]),
}
add_fixture_tests(RegistryDeduplicationTests, "registry", FIXTURES)
