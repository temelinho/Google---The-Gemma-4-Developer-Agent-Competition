# Evidence Coder V2

This candidate uses the competition's Gemma 4 31B quantized base model,
without a LoRA adapter. It replaces the earlier draft's multi-agent navigation
with one coder, bounded investigation, targeted tests, and an optional Python
semantic diagnosis skill. No trained weights or resolution-rate improvement
are claimed.

## Upload artifact

`submission.zip` is produced by `validate_and_package.py`. Its root contains
`agent.yaml`, `eval_config.yaml`, `configs/`, `prompts/`, and `skills/`.
Only the contents of `submission/` go into the upload; the validator environment,
downloaded compiler, reports, and this document do not.

The earlier `../../submission/` draft and earlier ZIP are preserved, including
pre-existing local changes to their sampling and evaluation configs.

## Design choices and limits

- One 31B agent with all nine harness workspace/graph tools.
- Optional semantic skill for tricky falsey values, iterators, inheritance,
  parsing, serialization and async cleanup.
- Explicit strategy to switch away from failed edit-file calls, avoid repeated
  graph queries, cap test commands and retain a valid patch when time is short.
- 1,024 thinking tokens per turn, 8,192 maximum generated tokens, no reasoning
  retention in message history, and deterministic generation settings.
- 4.25 minutes, 48 tool calls and 64 turns per task, with a 60-second command
  timeout. 120 tasks at the full per-task limit consume 8.5 hours of agent-loop
  time; 3.5 hours remain in the 12-hour envelope for other overhead. This is
  budget planning, not a measured runtime guarantee. Hidden task count and
  infrastructure overhead may differ.

## Validation

The official compiler wheel was downloaded from the competition's public
[wheelhouse](https://www.kaggle.com/datasets/metric/gemma-4-developer-agent-wheelhouse).
The configuration was checked with `adk-submission==0.2.13` and
`google-adk==1.36.1`. `validation_report.json` records exact archive and file
hashes, tool declarations, compilation results and validation limitations.
Compilation fixtures never call an inference endpoint or execute workspace
tools. Archive guards reject a nested root, traversal and forbidden binaries.

To reproduce on Windows from the repository root:

```powershell
releases\v2\validator-env\Scripts\python.exe -X utf8 releases\v2\validate_and_package.py
```

No CUDA device is available locally. Real Gemma inference and hidden evaluation
are separate from these structural checks. Do not interpret successful
compilation as a benchmark score.

## GPU development check

A private Kaggle notebook named `Gemma Evidence Coder V2 - Validation` is based
on the official
[Getting Started notebook](https://www.kaggle.com/code/ryanholbrook/getting-started-gemma-4-developer-agent).
It embeds the exact candidate ZIP and checks its SHA-256 before extraction.
The proposed 12-task development slice is selected before looking at results:
sort each repository's instance IDs by SHA-256, take four FastAPI, four Rich,
three Requests and the single HTTPX task. No gold patches are included in
the submission or shown to the agent.

The slice is deliberately small and repository-balanced, so its aggregate is
not an unbiased estimate of the full development set or the private test set.
Track resolved tasks, patch production, tool errors, elapsed time and test
collection failures separately. Public development dependencies can differ
from the hidden evaluator. Model quality remains unmeasured until that run
actually completes.

## References checked

- [Competition and evaluation contract](https://www.kaggle.com/competitions/gemma-4-developer-agent)
- [Technical harness guide and dataset](https://www.kaggle.com/competitions/gemma-4-developer-agent/data)
- [Rules](https://www.kaggle.com/competitions/gemma-4-developer-agent/rules)
- [Official queue and infrastructure announcement](https://www.kaggle.com/competitions/gemma-4-developer-agent/discussion/747519)

This is an experimental candidate. A top leaderboard position requires
observed evaluation results and further iteration; packaging and prompt
changes alone do not establish that level of performance.
