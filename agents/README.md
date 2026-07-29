# AEGIS operating-team roles

Roles describe who owns a decision or coordination responsibility. Skills
describe reusable behavior that a role may invoke. A role is not a service,
daemon, model identity, or permission grant.

Every registered role has exactly one primary responsibility and one canonical
owner entry in `registry/capabilities.json`. Before adding a role:

1. Search both registries for the proposed responsibility and aliases.
2. Extend an existing contract when the responsibility already has an owner.
3. Add a role only when its responsibility and authority boundary are distinct.
4. Add or update validation fixtures proving forbidden overlaps are rejected.

## Authority classes

- **Assistant:** prepares, coordinates, checks, or labels work.
- **Control:** blocks unsupported progress but cannot certify.
- **Independent authority:** issues a bounded verdict without implementing the
  subject. `aegis` is the only independent certification role in this registry.
- **Human authority:** Andre retains scope, merge, release, destructive-action,
  external-write, and final approval authority.

## Activation

Activate the smallest sufficient set. A role activates only when its trigger is
present and required inputs are available. Installed roles are dormant by
default. Stop when the subject, authority, scope, or evidence cannot be pinned.

## Forbidden combinations

- An implementer cannot validate or certify its own output.
- `project-manager` cannot certify.
- `completion-controller` cannot certify.
- `evidence-truth-guardian` cannot sign or certify.
- `blueprint-compiler` cannot invent or approve requirements.
- No role can silently override Andre's approval authority.

All handoffs must use the shared handoff contract once it is introduced.
