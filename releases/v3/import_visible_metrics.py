"""Reconstruct metrics from the rendered, complete Kaggle result table."""
import json
from pathlib import Path

base = Path(__file__).resolve().parent
rows = json.loads((base/'metric_table_rows.json').read_text(encoding='utf-8'))
assert len(rows) == 13 and 'duration_seconds' in rows[0]
metrics = []
for i, row in enumerate(rows[1:]):
    fields = row.split()
    assert len(fields) == 7 and int(fields[0]) == i
    metrics.append(dict(id=fields[1], resolved=fields[2] == 'True',
        test_exit_code=int(fields[3]), tool_calls=int(fields[4]),
        duration_seconds=float(fields[5])))
(base/'validation_metrics.json').write_text(json.dumps(metrics, indent=2), encoding='utf-8')
summary = dict(completed_tasks=len(metrics), resolved_tasks=sum(r['resolved'] for r in metrics),
    resolution_rate=sum(r['resolved'] for r in metrics)/len(metrics),
    source='Kaggle rendered final result table; time values rounded to six decimals',
    notebook_url='https://www.kaggle.com/code/muhammettemel/gemma-evidence-coder-v3-validation?scriptVersionId=363373646',
    candidate_sha256='0c65307d36740d1ea96b935416d99129b3b9ea109b3c2a5a15e641214ac81d95',
    scope='Public development diagnostic, not a hidden score or rank estimate')
(base/'development_summary.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
metadata = json.loads((base/'run_metadata.json').read_text(encoding='utf-8'))
metadata['status_at_recording'] = 'completed_12_tasks_2_resolved'
metadata['completed_tasks'] = 12
metadata['resolved_tasks'] = 2
(base/'run_metadata.json').write_text(json.dumps(metadata, indent=2), encoding='utf-8')
print(json.dumps(summary, indent=2))
