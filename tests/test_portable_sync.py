from helpers import ValidatorTestCase, add_fixture_tests


class PortableSyncTests(ValidatorTestCase):
    def test_positive_portable_surfaces(self) -> None:
        self.assertAccepted("scripts/verify_portable_sync.py")


FIXTURES = {
    "missing_refusal": ("missing doctrine invariant REFUSED", ["scripts/verify_portable_sync.py", "--fixture", "tests/fixtures/pr3/portable/drift.json"]),
    "conflicting_evidence": ("prohibited contradiction", ["scripts/verify_portable_sync.py", "--fixture", "tests/fixtures/pr4/portable/conflicting-evidence-definitions.json"]),
    "weakened_human_authority": ("prohibited contradiction", ["scripts/verify_portable_sync.py", "--fixture", "tests/fixtures/pr4/portable/weakened-human-authority.json"]),
    "missing_operating_team_install": ("missing canonical path portable/AEGIS_OPERATING_TEAM.md", ["scripts/verify_portable_sync.py", "--fixture", "tests/fixtures/pr4/portable/missing-operating-team-install.json"]),
}
add_fixture_tests(PortableSyncTests, "portable", FIXTURES)
