# Candidate selection and measurement limits

The 12-task development slice was fixed before running candidates, with
per-repository counts 4 FastAPI, 4 Rich, 3 Requests, 1 HTTPX. Within each repository
the tasks were selected by sorting SHA-256(instance_id). The evaluator iterates
in the original published file order. V2 was stopped early after three completed
tasks because its trajectories repeatedly reran checks; its incomplete run is
not a paired twelve-task baseline.

V3 and V4 are intended to finish the same twelve-task slice. V4 changes both
model and prompt, so any difference cannot be attributed to model size alone.
Selection should consider completed repair results, patch production, timeouts,
and execution time. A single small slice is not a hidden-test rank estimate.

Final V3/V4/V5 comparison rule, recorded before the new candidates' Rich
outcomes: rank by resolved count on the same five reference-passing tasks,
then by lower total elapsed time on those five tasks. Preserve complete raw
12-task V3/V4 results separately; V5 has no 12-task raw result. Do not imply
that any selected candidate is statistically proven to generalize better.

A separate verification-only control applies each task's published reference
patch through the same official verification function, in a separate notebook.
The candidate agent never receives these reference patches. A reference failure
means that this task's end-to-end result needs log inspection before it can be
interpreted as a clean measure of agent correctness. It does not prove that an
agent-generated patch is correct. Do not remove reference failures from raw
reported totals. Report any conditional diagnostic denominator explicitly.

All archive validation uses the official adk-submission 0.2.13 compiler and
google-adk 1.36.1. Local signature fixtures test compilation, tool declaration
and loading only. Real inference runs on Kaggle L4 x4 through the official
offline starter runtime. No local CUDA is available. No secret or hidden task
answers, repository-specific answer lookup, or scoring bypass is included.

Keep the original submitted ZIP bytes and SHA-256. The runtime notebook embeds
those bytes and asserts their hash before extracting. Notebooks, experiment
logs and public reference patches are never part of the candidate submission.
