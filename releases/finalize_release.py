"""Freeze the selected, already tested ZIP without rebuilding its bytes."""
import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

root = Path(__file__).resolve().parent
selection = json.loads((root/'candidate_selection.json').read_text(encoding='utf-8'))
chosen = selection['ranking'][0]
assert chosen['candidate'] == selection['selected']
candidate = root/chosen['candidate']
destination = root/'final'
destination.mkdir(exist_ok=False)
shutil.copyfile(candidate/'submission.zip', destination/'submission.zip')
shutil.copytree(candidate/'submission', destination/'source')
shutil.copyfile(candidate/'validation_report.json', destination/'validation_report.json')
shutil.copyfile(root/'candidate_selection.json', destination/'candidate_selection.json')
digest = hashlib.sha256((destination/'submission.zip').read_bytes()).hexdigest()
assert digest == chosen['archive_sha256']
(destination/'SHA256SUMS.txt').write_text(f'{digest}  submission.zip\n', encoding='utf-8')
receipt = dict(prepared_at_utc=datetime.now(timezone.utc).isoformat(),
    selected_candidate=selection['selected'], archive_sha256=digest,
    competition_url='https://www.kaggle.com/competitions/gemma-4-developer-agent',
    final_submit_verified=False, leaderboard_score=None)
(destination/'submission_receipt.json').write_text(json.dumps(receipt, indent=2), encoding='utf-8')
rows = '\n'.join(f"| {r['candidate']} | {r['matched_resolved']}/5 | {r['matched_seconds']:.1f} | {r['full_run_resolved']}/{r['full_run_completed_tasks']} |" for r in selection['ranking'])
readme = f'''# Final candidate: {selection['selected'].upper()}

The exact ZIP tested in Kaggle is copied here without rebuilding it.
The source directory and compiler validation report are included for review.
Only submission.zip is uploaded. The submission receipt records whether the
final Kaggle action was verified; a prepared file alone is not a submission.

## Measured selection

| Candidate | Same five tasks resolved | Same five elapsed seconds | Complete run raw resolved |
| --- | ---: | ---: | ---: |
{rows}

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

- ZIP SHA-256: {digest}
- Official compiler: adk-submission 0.2.13; google-adk 1.36.1.
- Directory, extracted archive, skills and tool declarations compiled successfully.
- Kaggle runtime checked the exact embedded ZIP hash before extracting.
- No LoRA, reference answers, notebook, tests, environment or compiler is in the ZIP.
- Earlier candidates, evidence, builders and pre-existing user changes are preserved.

See ../EXPERIMENT_PROTOCOL.md, ../gold_control_results/INTERPRETATION.md and the
candidate directories for the source notebooks and complete diagnostics.
'''
(destination/'README.md').write_text(readme, encoding='utf-8')
print(json.dumps(receipt, indent=2))
