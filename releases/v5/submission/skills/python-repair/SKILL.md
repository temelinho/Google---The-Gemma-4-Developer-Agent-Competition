---
name: python-repair
description: Diagnose subtle Python API regressions involving falsey values, iterators, inheritance, serialization, or async cleanup after the failing function has been located.
---

Use this skill for a concrete semantic uncertainty, not as mandatory preparation for every task. Select only the relevant checks in resources/semantics.md. Tie the check to the issue and the inspected implementation, then verify the smallest counterexample and a neighboring valid input. Do not change semantics merely because a checklist item exists.

Keep reproduction scripts in /tmp. Use the repository's real imports and conventions. Inspect import origins if a direct check appears to exercise a different installed version. Keep any behavior correction in the source library; harness configuration and validation tests are not implementation fixes.
