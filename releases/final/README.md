# Final candidate: V3

Competition upload was verified on 2026-10-29. Kaggle showed **Notebook Running**;
no leaderboard score was available at the recorded check. See submission_receipt.json
and submission-proof.jpg for the accepted upload evidence.

The exact ZIP tested in Kaggle is copied here without rebuilding it.
The source directory and compiler validation report are included for review.
Only submission.zip is uploaded. The submission receipt records whether the
final Kaggle action was verified; a prepared file alone is not a submission.

## Measured selection

| Candidate | Same five tasks resolved | Same five elapsed seconds | Complete run raw resolved |
| --- | ---: | ---: | ---: |
| v3 | 2/5 | 1336.1 | 2/12 |
| v5 | 1/5 | 1098.5 | 1/5 |
| v4 | 0/5 | 1572.2 | 0/12 |

Selection rule: most resolved on the same five tasks, then least elapsed time.
The five tasks are the reference-passing subset of a fixed twelve-task public
development slice. V3/V4 have twelve-task runs; V5 only has five. Seven published
reference patches failed verification, with a mix of missing dependencies,
fixture failures, import incompatibility and ordinary assertion failures.
Their failures do not establish that candidate patches are correct.

These are selected development diagnostics. They do not prove hidden-test
accuracy, a statistically reliable improvement, perfection or a top rank.
The actual leaderboard result is separate and may remain queued after upload.

## Reproducibility

- ZIP SHA-256: 0c65307d36740d1ea96b935416d99129b3b9ea109b3c2a5a15e641214ac81d95
- Official compiler: adk-submission 0.2.13; google-adk 1.36.1.
- Directory, extracted archive, skills and tool declarations compiled successfully.
- Kaggle runtime checked the exact embedded ZIP hash before extracting.
- No LoRA, reference answers, notebook, tests, environment or compiler is in the ZIP.
- Earlier candidates, evidence, builders and pre-existing user changes are preserved.

See ../EXPERIMENT_PROTOCOL.md, ../gold_control_results/INTERPRETATION.md and the
candidate directories for the source notebooks and complete diagnostics.
