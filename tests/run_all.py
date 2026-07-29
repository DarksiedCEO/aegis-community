#!/usr/bin/env python3
"""Deterministic dependency-free AEGIS skill-layer test runner."""

from __future__ import annotations

import argparse
import sys
import unittest

sys.dont_write_bytecode = True

REQUIRED_FAMILIES = {
    "test_skill_contracts",
    "test_registry_deduplication",
    "test_authority_boundaries",
    "test_portable_sync",
    "test_schema_validation",
}


class AegisResult(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.negative_verified = 0
        self.unexpected_passes = 0

    def addSuccess(self, test):
        super().addSuccess(test)
        if ".test_negative_" in test.id():
            self.negative_verified += 1

    def addFailure(self, test, err):
        super().addFailure(test, err)
        if "UNEXPECTED_PASS:" in self._exc_info_to_string(err, test):
            self.unexpected_passes += 1


class AegisRunner(unittest.TextTestRunner):
    resultclass = AegisResult


def iter_tests(suite):
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            yield from iter_tests(item)
        else:
            yield item


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pattern", default="test_*.py")
    args = parser.parse_args()

    suite = unittest.defaultTestLoader.discover("tests", pattern=args.pattern, top_level_dir="tests")
    discovered = suite.countTestCases()
    if discovered == 0:
        print("TESTS DISCOVERED: 0")
        print("TESTS EXECUTED: 0")
        print("TESTS PASSED: 0")
        print("TESTS FAILED: 1")
        print("EXPECTED-FAILURE FIXTURES VERIFIED: 0")
        print("UNEXPECTED PASSES: 0")
        print("FAIL: zero tests discovered")
        return 2

    families = {test.id().split(".", 1)[0] for test in iter_tests(suite)}
    missing_families = REQUIRED_FAMILIES - families
    if missing_families:
        print(f"TESTS DISCOVERED: {discovered}")
        print("TESTS EXECUTED: 0")
        print("TESTS PASSED: 0")
        print("TESTS FAILED: 1")
        print("EXPECTED-FAILURE FIXTURES VERIFIED: 0")
        print("UNEXPECTED PASSES: 0")
        print(f"FAIL: required validation families missing: {sorted(missing_families)}")
        return 2

    result = AegisRunner(verbosity=2).run(suite)
    failed = len(result.failures) + len(result.errors) + len(result.unexpectedSuccesses)
    passed = result.testsRun - failed - len(result.skipped)
    print(f"TESTS DISCOVERED: {discovered}")
    print(f"TESTS EXECUTED: {result.testsRun}")
    print(f"TESTS PASSED: {passed}")
    print(f"TESTS FAILED: {failed}")
    print(f"EXPECTED-FAILURE FIXTURES VERIFIED: {result.negative_verified}")
    print(f"UNEXPECTED PASSES: {result.unexpected_passes}")
    if result.skipped:
        print(f"FAIL: skipped tests are not permitted: {len(result.skipped)}")
        return 1
    return 0 if result.wasSuccessful() and result.testsRun == discovered else 1


if __name__ == "__main__":
    raise SystemExit(main())
