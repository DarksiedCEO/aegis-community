#!/usr/bin/env python3
"""Validate AEGIS registries and authority boundaries using only stdlib.

Supported runtime: CPython 3.11 or newer.
"""

from __future__ import annotations

import argparse
import copy
import json
import re
import sys
from pathlib import Path

ID = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
VERSION = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")
SUPPORTED_VERSION = "1.0.0"
HUMAN_ACTIONS = {
    "scope_approval",
    "merge_approval",
    "release_approval",
    "destructive_action_approval",
    "external_write_approval",
    "final_approval",
}
PRIVATE_MARKERS = (
    "aegis-enterprise/",
    "enterprise-private/",
    "private implementation:",
)


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


def exact_keys(value: dict, keys: set[str], where: str) -> None:
    require(set(value) == keys, f"{where}: expected keys {sorted(keys)}, got {sorted(value)}")


def load_bundle(root: Path) -> dict:
    registry = root / "registry"
    return {
        "agents": load_json(registry / "agents.json"),
        "capabilities": load_json(registry / "capabilities.json"),
        "authority": load_json(registry / "authority-matrix.json"),
        "registry_version": (registry / "VERSION").read_text(encoding="utf-8").strip(),
        "available_contracts": [
            str(path.relative_to(root))
            for path in root.rglob("*")
            if path.is_file()
        ],
        "community_texts": {
            str(path.relative_to(root)): path.read_text(encoding="utf-8")
            for base in ("aegis", "agents", "skills", "registry", "schemas", "portable", "claude-code")
            if (root / base).exists()
            for path in (root / base).rglob("*")
            if path.is_file() and path.suffix in {".md", ".json"}
        },
    }


def apply_fixture(bundle: dict, fixture_path: Path) -> dict:
    fixture = load_json(fixture_path)
    require(isinstance(fixture, dict), f"{fixture_path}: fixture must be an object")
    exact_keys(fixture, {"operations"}, str(fixture_path))
    require(isinstance(fixture["operations"], list) and fixture["operations"], "fixture operations must be non-empty")
    result = copy.deepcopy(bundle)
    for index, operation in enumerate(fixture["operations"]):
        require(isinstance(operation, dict), f"operation {index}: must be an object")
        op = operation.get("op")
        if op == "duplicate_role":
            result["agents"]["roles"].append(copy.deepcopy(result["agents"]["roles"][0]))
        elif op == "duplicate_capability":
            result["capabilities"]["capabilities"].append(copy.deepcopy(result["capabilities"]["capabilities"][0]))
        elif op == "empty_roles":
            result["agents"]["roles"] = []
        elif op == "empty_capabilities":
            result["capabilities"]["capabilities"] = []
        elif op == "duplicate_owner":
            result["capabilities"]["capabilities"][1]["owner"] = result["capabilities"]["capabilities"][0]["owner"]
        elif op == "duplicate_alias":
            result["capabilities"]["capabilities"][1]["aliases"].append(
                result["capabilities"]["capabilities"][0]["aliases"][0]
            )
        elif op == "unknown_owner":
            result["capabilities"]["capabilities"][0]["owner"] = "unknown-role"
        elif op == "missing_contract":
            result["available_contracts"].remove(result["agents"]["roles"][0]["contract"])
        elif op == "set_authority":
            exact_keys(operation, {"op", "role", "field", "value"}, f"operation {index}")
            result["authority"]["roles"][operation["role"]][operation["field"]] = operation["value"]
        elif op == "remove_human_action":
            result["authority"]["human_authority"]["exclusive_actions"].remove(operation["action"])
        elif op == "private_reference":
            result["community_texts"]["agents/fixture.md"] = operation["text"]
        elif op == "registry_version_mismatch":
            result["capabilities"]["registry_version"] = operation["value"]
        else:
            raise ValidationError(f"operation {index}: unsupported op {op!r}")
    return result


def validate_bundle(bundle: dict) -> None:
    agents = bundle["agents"]
    capabilities = bundle["capabilities"]
    authority = bundle["authority"]

    exact_keys(agents, {"schema_version", "registry_version", "roles"}, "agents registry")
    exact_keys(capabilities, {"schema_version", "registry_version", "capabilities"}, "capability registry")
    exact_keys(
        authority,
        {"schema_version", "registry_version", "human_authority", "roles", "forbidden_combinations"},
        "authority matrix",
    )
    versions = {
        agents["schema_version"],
        agents["registry_version"],
        capabilities["schema_version"],
        capabilities["registry_version"],
        authority["schema_version"],
        authority["registry_version"],
    }
    require(all(isinstance(value, str) and VERSION.fullmatch(value) for value in versions), "versions must be semver")
    require(bundle["registry_version"] == SUPPORTED_VERSION, "registry/VERSION must identify the supported registry version")
    require(versions == {bundle["registry_version"]}, "registry version mismatch")
    require(agents["roles"], "agent registry must not be empty")
    require(capabilities["capabilities"], "capability registry must not be empty")

    role_ids: list[str] = []
    for index, role in enumerate(agents["roles"]):
        exact_keys(
            role,
            {"id", "contract", "class", "primary_responsibility", "may_certify"},
            f"roles[{index}]",
        )
        require(isinstance(role["id"], str) and ID.fullmatch(role["id"]), f"roles[{index}]: invalid id")
        require(role["class"] in {"assistant", "control", "independent-authority"}, f"roles[{index}]: invalid class")
        require(isinstance(role["primary_responsibility"], str) and role["primary_responsibility"].strip(), f"roles[{index}]: empty responsibility")
        require(isinstance(role["may_certify"], bool), f"roles[{index}]: may_certify must be boolean")
        require(role["contract"] in bundle["available_contracts"], f"roles[{index}]: missing contract {role['contract']}")
        role_ids.append(role["id"])
    require(len(role_ids) == len(set(role_ids)), "duplicate role IDs")

    capability_ids: list[str] = []
    owners: list[str] = []
    aliases: list[str] = []
    for index, capability in enumerate(capabilities["capabilities"]):
        exact_keys(capability, {"id", "owner", "aliases"}, f"capabilities[{index}]")
        require(isinstance(capability["id"], str) and ID.fullmatch(capability["id"]), f"capabilities[{index}]: invalid id")
        require(capability["owner"] in role_ids, f"capabilities[{index}]: unknown owner {capability['owner']}")
        require(isinstance(capability["aliases"], list), f"capabilities[{index}]: aliases must be an array")
        require(len(capability["aliases"]) == len(set(capability["aliases"])), f"capabilities[{index}]: duplicate alias")
        capability_ids.append(capability["id"])
        owners.append(capability["owner"])
        aliases.extend(alias.casefold() for alias in capability["aliases"])
    require(len(capability_ids) == len(set(capability_ids)), "duplicate capability IDs")
    require(len(owners) == len(set(owners)), "duplicate capability ownership")
    require(len(aliases) == len(set(aliases)), "duplicate canonical capability aliases")
    require(not set(aliases).intersection(item.casefold() for item in capability_ids), "capability alias collides with canonical ID")
    require(set(owners) == set(role_ids), "every role must own exactly one canonical capability")

    exact_keys(authority["human_authority"], {"id", "exclusive_actions"}, "human authority")
    require(authority["human_authority"]["id"] == "andre", "human approval authority must remain Andre")
    require(set(authority["human_authority"]["exclusive_actions"]) == HUMAN_ACTIONS, "human approval authority cannot be overridden")
    require(set(authority["roles"]) == set(role_ids), "authority roles must match registered roles")
    for role_id, permissions in authority["roles"].items():
        exact_keys(permissions, {"implement", "validate", "certify", "sign"}, f"authority.{role_id}")
        require(all(isinstance(value, bool) for value in permissions.values()), f"authority.{role_id}: permissions must be boolean")

    permissions = authority["roles"]
    require(not permissions["aegis"]["implement"], "AEGIS implementation authority is forbidden")
    require(permissions["aegis"]["certify"], "AEGIS must retain bounded assessment authority")
    require(not permissions["aegis"]["sign"], "signing is outside the skill-only phase")
    require(not permissions["project-manager"]["certify"], "Project Manager certification authority is forbidden")
    require(not permissions["completion-controller"]["certify"], "Completion Controller certification authority is forbidden")
    require(not permissions["evidence-truth-guardian"]["certify"], "Evidence Guardian certification authority is forbidden")
    require(not permissions["evidence-truth-guardian"]["sign"], "Evidence Guardian signing authority is forbidden")
    require(
        [role_id for role_id, item in permissions.items() if item["certify"]] == ["aegis"],
        "AEGIS must be the only certifying role",
    )
    require(not any(item["sign"] for item in permissions.values()), "cryptographic signing is outside this phase")

    for path, text in bundle["community_texts"].items():
        lowered = text.lower()
        for marker in PRIVATE_MARKERS:
            require(marker not in lowered, f"{path}: private Enterprise implementation reference {marker!r}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--fixture", type=Path)
    args = parser.parse_args()
    try:
        bundle = load_bundle(args.root.resolve())
        if args.fixture:
            bundle = apply_fixture(bundle, args.fixture)
        validate_bundle(bundle)
    except (ValidationError, KeyError, IndexError, TypeError, ValueError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"FAIL: validator exception: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2
    print("PASS: registry IDs, ownership, contracts, authority, human approval, and Community boundaries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
