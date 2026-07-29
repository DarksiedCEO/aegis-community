import json
import shutil
import tempfile
from pathlib import Path

from helpers import ROOT, ValidatorTestCase, add_fixture_tests


class SkillContractTests(ValidatorTestCase):
    def test_positive_repository_contracts_and_examples(self) -> None:
        self.assertAccepted("scripts/validate_skills.py")

    def test_negative_empty_required_directory(self) -> None:
        descriptor = json.loads((ROOT / "tests/fixtures/pr4/directories/empty-required-directory.json").read_text())
        with tempfile.TemporaryDirectory() as temporary:
            copy = Path(temporary) / "repo"
            shutil.copytree(ROOT, copy, ignore=shutil.ignore_patterns(".git", "__pycache__"))
            target = copy / descriptor["directory"]
            for path in target.rglob("*"):
                if path.is_file():
                    path.unlink()
            self.assertRejected("empty required directory represented as complete", "scripts/validate_skills.py", "--root", str(copy))

    def test_negative_zero_discovery_protection(self) -> None:
        self.assertRejected("zero tests discovered", "tests/run_all.py", "--pattern", "no_tests_match.py")

    def test_negative_required_family_skip(self) -> None:
        self.assertRejected("required validation families missing", "tests/run_all.py", "--pattern", "test_registry_deduplication.py")


FIXTURES = {
    "missing_activation": ("missing ## Activate when", ["scripts/validate_skills.py", "--contract", "tests/fixtures/pr4/role-contracts/missing-activation.md", "--role-id", "invalid-role"]),
    "missing_forbidden": ("missing ## Forbidden", ["scripts/validate_skills.py", "--contract", "tests/fixtures/pr4/role-contracts/missing-forbidden.md", "--role-id", "invalid-role"]),
    "missing_stop": ("missing ## Stop conditions", ["scripts/validate_skills.py", "--contract", "tests/fixtures/pr4/role-contracts/missing-stop.md", "--role-id", "invalid-role"]),
    "missing_handoff": ("missing ## Handoff", ["scripts/validate_skills.py", "--contract", "tests/fixtures/pr4/role-contracts/missing-handoff.md", "--role-id", "invalid-role"]),
    "skeleton_example": ("skeleton example", ["scripts/validate_skills.py", "--example", "tests/fixtures/pr4/examples/skeleton.md"]),
    "placeholder_example": ("placeholder marker", ["scripts/validate_skills.py", "--example", "tests/fixtures/pr4/examples/placeholder.md"]),
}
add_fixture_tests(SkillContractTests, "contract", FIXTURES)
