# AEGIS Ω skill set — installation

Four platforms, one doctrine. `aegis/SKILL.md` is the canonical version; the
portable files restate it for platforms that cannot load skills.

## 1. Claude (claude.ai / desktop / mobile)

Settings → Capabilities → Skills → Upload, and select `aegis.skill`
(or `aegis/SKILL.md` directly).

Once installed it triggers automatically on audit, review, verification,
production-readiness, and certification requests. Invoke it explicitly with
"run an AEGIS assessment of X."

## 2. Claude Code

```bash
mkdir -p ~/.claude/skills/aegis
cp aegis/SKILL.md ~/.claude/skills/aegis/SKILL.md

mkdir -p ~/.claude/commands
cp claude-code/commands/aegis.md ~/.claude/commands/aegis.md
```

Per-repository rules:

```bash
cp claude-code/CLAUDE.md /path/to/repo/CLAUDE.md
```

If the repo already has a `CLAUDE.md`, merge rather than overwrite — keep the
stricter rule wherever they conflict.

Then: `/aegis` for a read-only assessment of the current repo, or
`/aegis <subject>` to scope it.

## 3. ChatGPT

Create a project. Open its custom instructions and paste the full contents of
`portable/AEGIS_CHATGPT_PROJECT_INSTRUCTIONS.md`.

That file carries two platform-specific additions the others don't need: a
reminder that ChatGPT cannot inspect a repository without a connector (so
repository claims are E0 by default), and a reminder that generated files live in
a sandbox that gets deleted.

## 4. Codex

```bash
cp portable/AGENTS.md /path/to/repo/AGENTS.md
```

Codex reads `AGENTS.md` from the repository root automatically. Merge if one
already exists.

---

## Keeping four copies in sync

The doctrine is identical across all four; only platform mechanics differ. When
you change the doctrine, change `aegis/SKILL.md` first, then propagate.

The parts that must stay identical, or the skill set stops being one system:
the E0–E5 definitions, the five verdict strings, the independence rule, and the
mandatory UNVERIFIED section.

## What this skill set is and isn't

It changes how agents reason about evidence and how they are permitted to phrase
completion. That is a real control — most false certifications are phrasing
failures, and this makes the phrasing honest.

It is not a runtime, and it enforces nothing mechanically. An agent following
these instructions can still be wrong; it just can't call a guess a verification
without violating an explicit rule. Mechanical enforcement — CI gates, remote-SHA
checks, signing — is a separate layer that lives in the repositories.

Status of this package, in its own terms:

```
DOCTRINE:                 DEFINED
PLATFORM SKILL FILES:     WRITTEN
MECHANICAL ENFORCEMENT:   NOT INCLUDED
INSTALLED:                NOT YET — requires the steps above
FIELD-TESTED:             NO
```
