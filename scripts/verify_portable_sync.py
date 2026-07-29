#!/usr/bin/env python3
"""Verify cross-platform AEGIS doctrine invariants using only stdlib.

Supported runtime: CPython 3.11 or newer.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

VERDICTS = ("CERTIFIED", "CONDITIONAL", "NOT_CERTIFIED", "INSUFFICIENT_EVIDENCE", "REFUSED")
LEVELS = ("E0", "E1", "E2", "E3", "E4", "E5")


class SyncError(Exception):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SyncError(message)


def load_map(root: Path) -> dict:
    path = root / "portable" / "sync-map.json"
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise SyncError(f"sync map: cannot read {path}: {exc}") from exc
    require(isinstance(value, dict), "sync map must be an object")
    return value


def repository_surfaces(root: Path) -> dict[str, str]:
    paths = {
        "canonical": root / "aegis" / "SKILL.md",
        "codex": root / "portable" / "AGENTS.md",
        "chatgpt": root / "portable" / "AEGIS_CHATGPT_PROJECT_INSTRUCTIONS.md",
        "claude-command": root / "claude-code" / "commands" / "aegis.md",
        "claude-rules": root / "claude-code" / "CLAUDE.md",
        "install": root / "INSTALL.md",
        "operating-team": root / "portable" / "AEGIS_OPERATING_TEAM.md",
    }
    result: dict[str, str] = {}
    for name, path in paths.items():
        try:
            result[name] = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            raise SyncError(f"{name}: cannot read {path}: {exc}") from exc
    return result


def fixture_surfaces(path: Path) -> dict[str, str]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise SyncError(f"{path}: cannot parse fixture: {exc}") from exc
    require(isinstance(value, dict) and set(value) == {"files"}, "fixture must contain only files")
    require(isinstance(value["files"], dict), "fixture files must be an object")
    return value["files"]


def validate(surfaces: dict[str, str], sync_map: dict) -> None:
    required_names = {"canonical", "codex", "chatgpt", "claude-command", "claude-rules", "install", "operating-team"}
    require(set(surfaces) == required_names, f"surface inventory mismatch: {sorted(surfaces)}")
    for name, text in surfaces.items():
        require(isinstance(text, str) and text.strip(), f"{name}: empty surface")

    required_map_keys = {
        "schema_version", "registry_version", "canonical_source",
        "shared_role_surface", "platforms", "role_ids", "evidence_levels",
        "truth_labels", "verdicts", "human_authority", "prohibited_phrases",
    }
    require(set(sync_map) == required_map_keys, "sync map fields drifted")
    require(sync_map["schema_version"] == "1.0.0", "sync map schema version mismatch")
    require(sync_map["registry_version"] == "1.0.0", "sync map registry version mismatch")
    require(set(sync_map["platforms"]) == {"codex", "chatgpt", "claude", "claude-code"}, "platform map incomplete")

    for name in ("canonical", "codex", "chatgpt"):
        text = surfaces[name].upper()
        for token in LEVELS + VERDICTS + ("UNVERIFIED",):
            require(token in text, f"{name}: missing doctrine invariant {token}")

    command = surfaces["claude-command"].upper()
    for token in VERDICTS + ("E0", "E5", "UNVERIFIED"):
        require(token in command, f"claude-command: missing doctrine invariant {token}")

    canonical = surfaces["canonical"].lower()
    require("aegis does not implement" in canonical, "canonical: implementation boundary drift")
    require("implementer  ≠  validator" in surfaces["canonical"], "canonical: independence boundary drift")
    require("no self-certification" in surfaces["codex"].lower(), "codex: self-certification boundary drift")
    require("implementer ≠ validator" in surfaces["chatgpt"].lower(), "chatgpt: independence boundary drift")
    require("no self-certification" in surfaces["claude-rules"].lower(), "claude-rules: self-certification boundary drift")

    install = surfaces["install"]
    for path in (
        "aegis/SKILL.md",
        "portable/AGENTS.md",
        "portable/AEGIS_CHATGPT_PROJECT_INSTRUCTIONS.md",
        "portable/AEGIS_OPERATING_TEAM.md",
    ):
        require(path in install, f"install: missing canonical path {path}")

    operating_team = surfaces["operating-team"]
    for token in (
        tuple(sync_map["role_ids"])
        + tuple(sync_map["evidence_levels"])
        + tuple(sync_map["truth_labels"])
        + tuple(sync_map["verdicts"])
        + tuple(sync_map["human_authority"])
    ):
        require(token.casefold() in operating_team.casefold(), f"operating-team: missing locked invariant {token}")

    combined = "\n".join(surfaces.values()).casefold()
    for phrase in sync_map["prohibited_phrases"]:
        require(phrase.casefold() not in combined, f"portable surfaces contain prohibited contradiction {phrase!r}")

    for platform, paths in sync_map["platforms"].items():
        require(sync_map["shared_role_surface"] in paths, f"{platform}: shared role surface missing")
        require(paths, f"{platform}: no synchronized surfaces")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--fixture", type=Path)
    args = parser.parse_args()
    try:
        root = args.root.resolve()
        surfaces = fixture_surfaces(args.fixture) if args.fixture else repository_surfaces(root)
        validate(surfaces, load_map(root))
    except (SyncError, KeyError, TypeError, ValueError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"FAIL: validator exception: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2
    print("PASS: portable doctrine invariants and installation paths are synchronized")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
