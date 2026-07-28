# Repository rules — AEGIS discipline

These rules apply to all work in this repository, whether or not the `aegis`
skill is active. They exist because this project's failure mode is confident
false completion, not missing effort.

## Before any analysis

Record and report, as the first output of any session:

```bash
git rev-parse --abbrev-ref HEAD
git rev-parse HEAD
git status --short --branch
git remote -v
git ls-remote origin HEAD
```

If local HEAD and remote HEAD differ, or the branch has no upstream, say so
before saying anything else. Every subsequent claim about "the repo" is scoped to
whichever of the two you actually examined, and you must name which.

## Read-only by default

Assessment does not require mutation. Do not create, modify, or delete files
during an audit unless the user authorizes that specific change. "I fixed it
while I was in there" destroys the baseline the assessment was measuring.

## Never, during an integrity investigation

`git reset` · `git rebase` · `git clean` · `git checkout --force` ·
`git stash drop` · `git push --force` · squash · history rewrite

These destroy evidence. If one of them seems necessary, stop and ask.

## Failure handling

A failing command is a finding, not an obstacle. Report the exact command, exit
code, and stderr.

Do not retry with reduced scope, added `|| true`, `continue-on-error`, broadened
`except`, or a widened ignore file. A green obtained by weakening the check is
worse than a red, because it will be believed.

## No self-certification

Code written in this session may not be described as verified, tested, passing,
production-ready, or complete by the same session that wrote it. Report what was
built and what remains unvalidated. Validation is a separate pass by a separate
identity.

## Repository is not production

A passing repository check says nothing about deployed state. Never let a claim
about the repo become a claim about production without evidence bound to the
production environment specifically.

## Claim discipline

Every status claim in a commit message, README, PR body, or summary must be
supported by evidence at E3 or above (a reproducible run with preserved raw
output). If it isn't, write what is actually true instead: "implemented, not yet
validated."
