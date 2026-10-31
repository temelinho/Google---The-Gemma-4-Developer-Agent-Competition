"""Apply the recorded five-task diagnostic selection rule to completed runs."""
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parent
ids = {'fastapi_15661', 'rich_3894', 'rich_3772', 'rich_3535', 'rich_3278'}
ranking = []
for version in ('v3', 'v4', 'v5'):
    metrics = json.loads((root/version/'validation_metrics.json').read_text(encoding='utf-8'))
    chosen = [r for r in metrics if r['id'] in ids]
    assert {r['id'] for r in chosen} == ids and len(chosen) == len(ids), f'{version}: incomplete comparison'
    archive = root/version/'submission.zip'
    ranking.append(dict(candidate=version, matched_tasks=len(chosen),
        matched_resolved=sum(bool(r['resolved']) for r in chosen),
        matched_seconds=sum(r['duration_seconds'] for r in chosen),
        full_run_completed_tasks=len(metrics),
        full_run_resolved=sum(bool(r['resolved']) for r in metrics),
        archive_sha256=hashlib.sha256(archive.read_bytes()).hexdigest(),
        archive_path=str(archive.resolve())))
ranking.sort(key=lambda r: (-r['matched_resolved'], r['matched_seconds']))
report = dict(rule='Most resolved on the same five reference-passing tasks, then least elapsed time on those five.',
    selected=ranking[0]['candidate'], ranking=ranking,
    limitation='Selected public development diagnostic; not a hidden score, representative sample, statistical proof or rank guarantee.')
(root/'candidate_selection.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
print(json.dumps(report, indent=2))
