#!/usr/bin/env python3
"""Validate AEGIS schemas, role contracts, and example documents.

Supported runtime: CPython 3.11 or newer. No third-party packages are used.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

VERSION = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")
ROLE_ID = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LEVELS = {"E0", "E1", "E2", "E3", "E4", "E5"}
LABELS = {"ASSERTED", "OBSERVED", "REPRODUCED", "INDEPENDENTLY_REPRODUCED", "ATTESTED", "UNVERIFIED"}
STATUSES = {"planned", "blocked", "in_progress", "implemented_not_verified", "verified", "closed"}
PLACEHOLDER = re.compile(r"(?im)^\s*(?:[-*]\s*)?(?:TODO|FIXME|TBD)(?:\s*:|\s*$)|lorem ipsum")


class ValidationError(Exception):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def load_json(path: Path) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValidationError(f"{path}: cannot parse JSON: {exc}") from exc


def object_with_exact_keys(value: object, required: set[str], optional: set[str], where: str) -> dict:
    require(isinstance(value, dict), f"{where}: must be an object")
    missing = required - set(value)
    unknown = set(value) - required - optional
    require(not missing, f"{where}: missing fields {sorted(missing)}")
    require(not unknown, f"{where}: unknown fields {sorted(unknown)}")
    return value


def nonempty_string(value: object, where: str) -> None:
    require(isinstance(value, str) and bool(value.strip()), f"{where}: must be a non-empty string")


def string_array(value: object, where: str, *, nonempty: bool = False) -> None:
    require(isinstance(value, list), f"{where}: must be an array")
    require(not nonempty or bool(value), f"{where}: must not be empty")
    require(all(isinstance(item, str) for item in value), f"{where}: must contain strings")


def validate_handoff(value: object) -> None:
    required = {
        "schema_version", "registry_version", "handoff_id", "source_role", "target_role", "subject",
        "status", "artifacts", "evidence", "warnings", "unresolved_risks",
        "next_required_action", "approval_required",
    }
    item = object_with_exact_keys(value, required, {"extensions"}, "handoff")
    require(VERSION.fullmatch(item["schema_version"]), "handoff.schema_version: invalid")
    require(VERSION.fullmatch(item["registry_version"]), "handoff.registry_version: invalid")
    for key in ("handoff_id", "subject", "next_required_action"):
        nonempty_string(item[key], f"handoff.{key}")
    for key in ("source_role", "target_role"):
        require(isinstance(item[key], str) and ROLE_ID.fullmatch(item[key]), f"handoff.{key}: invalid role ID")
    require(item["status"] in STATUSES, "handoff.status: invalid")
    for key in ("artifacts", "evidence", "warnings", "unresolved_risks"):
        string_array(item[key], f"handoff.{key}")
    require(isinstance(item["approval_required"], bool), "handoff.approval_required: must be boolean")
    if "extensions" in item:
        require(isinstance(item["extensions"], dict), "handoff.extensions: must be an object")


def validate_evidence(value: object) -> None:
    required = {"schema_version", "registry_version", "role_id", "subject", "claim", "evidence_level", "truth_label", "producer", "observed_at", "gaps"}
    item = object_with_exact_keys(value, required, {"artifacts"}, "evidence")
    require(VERSION.fullmatch(item["schema_version"]), "evidence.schema_version: invalid")
    require(VERSION.fullmatch(item["registry_version"]), "evidence.registry_version: invalid")
    require(ROLE_ID.fullmatch(item["role_id"]), "evidence.role_id: invalid")
    for key in ("subject", "claim", "producer"):
        nonempty_string(item[key], f"evidence.{key}")
    require(item["evidence_level"] in LEVELS, "evidence.evidence_level: invalid")
    require(item["truth_label"] in LABELS, "evidence.truth_label: invalid")
    nonempty_string(item["observed_at"], "evidence.observed_at")
    try:
        datetime.fromisoformat(item["observed_at"].replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValidationError("evidence.observed_at: invalid date-time") from exc
    string_array(item["gaps"], "evidence.gaps")
    if "artifacts" in item:
        string_array(item["artifacts"], "evidence.artifacts")


def validate_completion(value: object) -> None:
    required = {
        "schema_version", "registry_version", "subject", "status", "requirements",
        "prohibited_actions", "stop_conditions", "approval_boundaries",
    }
    item = object_with_exact_keys(value, required, set(), "completion")
    require(VERSION.fullmatch(item["schema_version"]), "completion.schema_version: invalid")
    require(VERSION.fullmatch(item["registry_version"]), "completion.registry_version: invalid")
    nonempty_string(item["subject"], "completion.subject")
    require(item["status"] in STATUSES, "completion.status: invalid")
    require(isinstance(item["requirements"], list) and item["requirements"], "completion.requirements: must not be empty")
    ids: list[str] = []
    for index, requirement in enumerate(item["requirements"]):
        entry = object_with_exact_keys(
            requirement,
            {"id", "owner", "acceptance_criteria", "required_evidence_level", "status"},
            {"evidence_references"},
            f"completion.requirements[{index}]",
        )
        for key in ("id", "owner", "acceptance_criteria"):
            nonempty_string(entry[key], f"completion.requirements[{index}].{key}")
        require(entry["required_evidence_level"] in LEVELS, f"completion.requirements[{index}]: invalid evidence level")
        require(entry["status"] in STATUSES, f"completion.requirements[{index}]: invalid status")
        ids.append(entry["id"])
    require(len(ids) == len(set(ids)), "completion.requirements: duplicate IDs")
    for key in ("prohibited_actions", "stop_conditions", "approval_boundaries"):
        string_array(item[key], f"completion.{key}", nonempty=True)


def validate_agent_output(value: object) -> None:
    required = {
        "schema_version", "registry_version", "role_id", "capability_id", "subject", "status", "truth_label",
        "evidence_level", "findings", "authority", "prohibited_actions", "stop_conditions", "handoff",
    }
    item = object_with_exact_keys(value, required, {"extensions"}, "agent-output")
    require(VERSION.fullmatch(item["schema_version"]), "agent-output.schema_version: invalid")
    require(VERSION.fullmatch(item["registry_version"]), "agent-output.registry_version: invalid")
    require(ROLE_ID.fullmatch(item["role_id"]), "agent-output.role_id: invalid")
    require(ROLE_ID.fullmatch(item["capability_id"]), "agent-output.capability_id: invalid")
    nonempty_string(item["subject"], "agent-output.subject")
    require(item["status"] in STATUSES, "agent-output.status: invalid")
    require(item["truth_label"] in LABELS, "agent-output.truth_label: invalid")
    require(item["evidence_level"] in LEVELS, "agent-output.evidence_level: invalid")
    for key in ("findings", "prohibited_actions", "stop_conditions"):
        string_array(item[key], f"agent-output.{key}", nonempty=key != "findings")
    string_array(item["authority"], "agent-output.authority", nonempty=True)
    validate_handoff(item["handoff"])


VALIDATORS = {
    "agent-output": validate_agent_output,
    "completion-manifest": validate_completion,
    "evidence-label": validate_evidence,
    "handoff": validate_handoff,
}


def validate_repository(root: Path) -> None:
    schema_dir = root / "schemas"
    expected = {
        "agent-output.schema.json",
        "completion-manifest.schema.json",
        "evidence-label.schema.json",
        "handoff.schema.json",
        "registry.schema.json",
    }
    found = {path.name for path in schema_dir.glob("*.json")}
    require(found == expected, f"schema inventory mismatch: expected {sorted(expected)}, got {sorted(found)}")
    for path in schema_dir.glob("*.json"):
        schema = load_json(path)
        require(isinstance(schema, dict), f"{path}: schema must be an object")
        require(schema.get("$schema") == "https://json-schema.org/draft/2020-12/schema", f"{path}: wrong JSON Schema draft")
        require(schema.get("title"), f"{path}: missing title")

    expected_roles = json.loads((root / "registry" / "agents.json").read_text(encoding="utf-8"))["roles"]
    for role in expected_roles:
        contract = root / role["contract"]
        require(contract.is_file(), f"{contract}: missing role contract")
        text = contract.read_text(encoding="utf-8")
        require(text.strip(), f"{contract}: empty role contract")
        require(not PLACEHOLDER.search(text), f"{contract}: placeholder marker")
        if role["id"] != "aegis":
            for marker in ("Primary responsibility:", "## Activate when", "## Forbidden", "## Stop conditions", "## Handoff"):
                require(marker in text, f"{contract}: missing {marker}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--kind", choices=sorted(VALIDATORS))
    parser.add_argument("--document", type=Path)
    args = parser.parse_args()
    try:
        if bool(args.kind) != bool(args.document):
            raise ValidationError("--kind and --document must be supplied together")
        if args.document:
            VALIDATORS[args.kind](load_json(args.document))
        else:
            validate_repository(args.root.resolve())
    except (ValidationError, KeyError, IndexError, TypeError, ValueError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"FAIL: validator exception: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2
    print("PASS: schemas and skill-layer contracts")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
