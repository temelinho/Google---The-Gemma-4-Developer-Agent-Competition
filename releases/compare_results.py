"""Compare completed public development runs without treating them as a leaderboard."""
import argparse
import json
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('runs', nargs='+', type=Path)
args = parser.parse_args()
all_runs = {}
for path in args.runs:
    metrics_path = path/'validation_metrics.json'
    if metrics_path.exists():
        rows = json.loads(metrics_path.read_text(encoding='utf-8'))
    else:
        rows = [json.loads(line) for line in (path/'task_results.jsonl').read_text(encoding='utf-8').splitlines() if line.strip()]
    by_id = {r.get('id', r.get('instance_id', r.get('task_id'))): r for r in rows}
    assert None not in by_id and len(by_id) == len(rows), 'Missing or duplicate task id'
    all_runs[str(path)] = by_id
    print(json.dumps({'run': str(path), 'completed': len(rows),
        'resolved': sum(bool(r['resolved']) for r in rows),
        'duration_seconds': round(sum(r.get('duration_seconds', 0) for r in rows), 1)}, ensure_ascii=False))

paired = set.intersection(*(set(rows) for rows in all_runs.values()))
print('Common completed tasks:', len(paired))
for task_id in sorted(paired):
    print(task_id, {name: rows[task_id]['resolved'] for name, rows in all_runs.items()})
print('Public development diagnostics only. Different prompts/models are confounded; no hidden-rank estimate.')
