# Evidence Coder V3: completed development diagnostic

Derived from the independently authored V2 candidate. Changes respond to observed
development trajectories: the first task read until its 255-second deadline
without editing, while the next task edited source but repeated a successful
print-only reproducer without changing the tree.

V3 changes temperature from 0 to 0.2, restores reasoning retention, reduces
the tool cap from 48 to 32, requires periodic status checks, and adds explicit
stopping and no-repeat rules. The wall-clock cap and base model are unchanged.
These are hypotheses to test, not proven improvements.

The complete 12-task diagnostic resolved 2 tasks (rich_3894 and rich_3278).
The separate published-reference control passed 5 of these 12 tasks; V3 passed
2 of those 5. The full raw result remains 2/12. The other seven tasks are not a
clean accuracy measurement, and reference failures do not prove V3 patches correct.
See development_summary.json, validation_metrics.json and the rendered Kaggle
evidence. One Rich failure is a real missing-return assertion; another reaches
the verification timeout. No hidden leaderboard score is claimed.

Use the V2 isolated environment to run this directory's validate_and_package.py.
The earlier candidates and pre-existing user changes are retained.
