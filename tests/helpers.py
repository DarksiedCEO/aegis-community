"""Shared test helpers for dependency-free AEGIS validation."""

from __future__ import annotations

import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PYTHON = "python3.11"


class ValidatorTestCase(unittest.TestCase):
    maxDiff = None

    def run_command(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [PYTHON, *arguments],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
            timeout=30,
        )

    def assertAccepted(self, *arguments: str) -> str:
        result = self.run_command(*arguments)
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("PASS:", result.stdout)
        return result.stdout

    def assertRejected(self, expected_reason: str, *arguments: str) -> str:
        result = self.run_command(*arguments)
        if result.returncode == 0:
            self.fail(f"UNEXPECTED_PASS: {' '.join(arguments)}\n{result.stdout}")
        self.assertIn(expected_reason, result.stdout)
        return result.stdout


def add_fixture_tests(
    case: type[ValidatorTestCase],
    prefix: str,
    fixtures: dict[str, tuple[str, list[str]]],
) -> None:
    for name, (reason, arguments) in fixtures.items():
        def test(self: ValidatorTestCase, expected: str = reason, args: list[str] = arguments) -> None:
            self.assertRejected(expected, *args)

        setattr(case, f"test_negative_{prefix}_{name}", test)
