# Example: cross-platform workflow

This is a fictional coordination example, not evidence of model execution.

1. Codex reads `AGENTS.md`, the canonical registry, and the operating-team
   appendix before preparing a bounded implementation.
2. Claude Code reads `CLAUDE.md`, the canonical AEGIS skill, and the same
   operating-team appendix before conducting a separate review.
3. ChatGPT uses its project instructions and the appendix to inspect supplied
   evidence without claiming filesystem access it does not have.
4. Claude uses the canonical skill and appendix to perform an independent
   assessment within available tool access.
5. Every environment uses the same role IDs, E0–E5 levels, truth labels, verdict
   strings, and human approval boundary.

No environment may treat another model's summary as raw evidence or silently
convert local validation into remote CI.
