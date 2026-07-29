# AEGIS skills

Skills are reusable instruction sets. They do not create identities, grant tool
permissions, or activate themselves. Roles may invoke skills only inside their
own authority boundary.

Before adding a skill, search `registry/capabilities.json` by ID, aliases,
responsibility, inputs, outputs, and forbidden actions. Extend an existing skill
when the proposed behavior already has a canonical owner.

Each skill must define:

- activation and non-activation conditions;
- one primary responsibility;
- required inputs and evidence;
- allowed and forbidden actions;
- stop conditions;
- output and handoff contract;
- approval boundaries;
- examples of correct and incorrect behavior.

`aegis` is an independent assessment skill. It cannot be combined with an
implementation role for the same candidate. Installed skills remain dormant
until their activation conditions are met.
