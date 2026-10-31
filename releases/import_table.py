"""Import complete metrics rendered in a Kaggle notebook result table."""
import argparse
import hashlib
import json
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument('candidate', type=Path)
p.add_argument('expected_count', type=int)
args = p.parse_args()
base = args.candidate
rows = json.loads((base/'metric_table_rows.json').read_text(encoding='utf-8'))
assert len(rows) == args.expected_count+1 and 'duration_seconds' in rows[0]
metrics = []
for i, row in enumerate(rows[1:]):
    fields = row.split()
    assert len(fields) == 7 and int(fields[0]) == i
    assert fields[2] in {'True', 'False'}
    metrics.append(dict(id=fields[1], resolved=fields[2]=='True',
        test_exit_code=int(fields[3]), tool_calls=int(fields[4]),
        duration_seconds=float(fields[5])))
assert len({r['id'] for r in metrics}) == args.expected_count
(base/'validation_metrics.json').write_text(json.dumps(metrics, indent=2), encoding='utf-8')
summary = dict(completed_tasks=len(metrics), resolved_tasks=sum(r['resolved'] for r in metrics),
    resolution_rate=sum(r['resolved'] for r in metrics)/len(metrics),
    source='Complete rendered Kaggle table; duration values rounded to six decimals',
    candidate_sha256=hashlib.sha256((base/'submission.zip').read_bytes()).hexdigest(),
    scope='Public development diagnostic; not a hidden score or rank estimate')
(base/'development_summary.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
metadata = json.loads((base/'run_metadata.json').read_text(encoding='utf-8'))
metadata.update(status_at_recording='completed', completed_tasks=len(metrics),
    resolved_tasks=sum(r['resolved'] for r in metrics), source_hash_verified_in_runtime=True)
(base/'run_metadata.json').write_text(json.dumps(metadata, indent=2), encoding='utf-8')
print(json.dumps(summary, indent=2))
