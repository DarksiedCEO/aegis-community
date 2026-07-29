# Updating and synchronizing AEGIS instructions

This procedure updates the skill layer only.

1. Pin the repository, branch, exact local SHA, upstream, remote SHA, and
   worktree state.
2. Change the canonical doctrine in `aegis/SKILL.md` first.
3. Update platform-specific wording without changing locked semantics.
4. Update `portable/AEGIS_OPERATING_TEAM.md` when role IDs or authority
   boundaries change.
5. Update `portable/sync-map.json` and `registry/VERSION` for intentional
   registry changes.
6. Run `python3.11 tests/run_all.py`.
7. Preserve raw output and bind it to the tested SHA.
8. Obtain independent review before any completion or certification claim.

Synchronization locks evidence levels, truth labels, verdicts, refusal behavior,
role IDs, human authority, implementation prohibitions, and installation paths.
Byte equality is required only for artifacts explicitly designated as copies;
platform-specific files are checked for semantic invariants.

Local success does not prove remote CI. A changed candidate invalidates evidence
from an earlier SHA. Private Enterprise implementation details must never be
copied into Community contracts or fixtures.
