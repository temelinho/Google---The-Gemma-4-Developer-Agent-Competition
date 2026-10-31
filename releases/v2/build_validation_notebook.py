"""Build a reproducible development notebook from the official starter source.

The original Kaggle API response is cached in vendor/official_notebook_response.json.
It comes from /api/v1/kernels/pull/ryanholbrook/getting-started-gemma-4-developer-agent.
"""
import base64
import hashlib
import json
from pathlib import Path
import sys

BASE = Path(__file__).resolve().parent
CANDIDATE = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else BASE
VARIANT = CANDIDATE.name
response = json.loads((BASE / 'vendor/official_notebook_response.json').read_text(encoding='utf-8'))
notebook = json.loads(response['blob']['sourceNullable'])
code_cells = [c for c in notebook['cells'] if c['cell_type'] == 'code']
assert len(code_cells) == 6
for c in notebook['cells']:
    c['metadata'] = {}
    if c['cell_type'] == 'code':
        c['outputs'] = []
        c['execution_count'] = None

archive_bytes = (CANDIDATE / 'submission.zip').read_bytes()
encoded = base64.b64encode(archive_bytes).decode('ascii')
digest = hashlib.sha256(archive_bytes).hexdigest()
model_name = next(line.split(':', 1)[1].strip() for line in (CANDIDATE / 'submission/agent.yaml').read_text(encoding='utf-8').splitlines() if line.startswith('model:'))
code_cells[1]['source'] = f'''import re
import base64
import hashlib
import io
import zipfile
from swegemma.models import load_tasks
DATA_DIR = Path('/kaggle/input/competitions/gemma-4-developer-agent')
WORKING_DIR = Path('/kaggle/working')
WORKING_DIR.mkdir(parents=True, exist_ok=True)
MODEL_NAME = {model_name!r}
AGENT_DIR = WORKING_DIR / 'evidence_coder_{VARIANT}'
AGENT_DIR.mkdir(parents=True, exist_ok=True)
archive_bytes = base64.b64decode('{encoded}')
assert hashlib.sha256(archive_bytes).hexdigest() == '{digest}'
with zipfile.ZipFile(io.BytesIO(archive_bytes)) as z:
    z.extractall(AGENT_DIR)
TASKS_PATH = DATA_DIR / 'tasks.jsonl'
tasks = load_tasks(TASKS_PATH)
print('Candidate ready', MODEL_NAME, len(tasks), hashlib.sha256(archive_bytes).hexdigest())
'''

SAMPLE_IDS = ['fastapi_11355', 'fastapi_14512', 'fastapi_14953', 'fastapi_15661',
              'rich_3894', 'rich_3535', 'rich_3772', 'rich_3278',
              'requests_7505', 'requests_7427', 'requests_6757', 'httpx_3672']

def source(cell):
    raw = cell['source']
    return ''.join(raw) if isinstance(raw, list) else raw

eval_source = source(code_cells[4])
assert eval_source.count('SAMPLE_TASKS = tasks[:2]') == 1
eval_source = eval_source.replace('SAMPLE_TASKS = tasks[:2]', f'''SAMPLE_IDS = set({SAMPLE_IDS!r})
SAMPLE_TASKS = [t for t in tasks if t.instance_id in SAMPLE_IDS]
assert len(SAMPLE_TASKS) == 12
import json
from swegemma.results import append_task_result
metrics = []
all_results = []''')
eval_source = eval_source.replace("    patch = (result.agent_patch or '').strip()", '''    all_results.append(result)
    append_task_result(result, WORKING_DIR / 'results', all_results)
    metrics.append({'id': task.instance_id, 'resolved': result.resolved, 'test_exit_code': result.test_exit_code, 'tool_calls': result.tool_calls, 'duration_seconds': result.duration_seconds})
    (WORKING_DIR / 'validation_metrics.json').write_text(json.dumps(metrics, indent=2))
    patch = (result.agent_patch or '').strip()''')
code_cells[4]['source'] = eval_source

notebook['cells'].append({
    'cell_type': 'code', 'execution_count': None, 'metadata': {}, 'outputs': [],
    'source': '''import math
metrics_df = pd.DataFrame(metrics)
metrics_df['repo'] = metrics_df['id'].str.rsplit('_', n=1).str[0]
print('Development slice; not a leaderboard estimate')
display(metrics_df.groupby('repo').agg(tasks=('id', 'count'), resolved=('resolved', 'sum'), mean_seconds=('duration_seconds', 'mean')))
display(metrics_df)
(WORKING_DIR / 'validation_summary.json').write_text(json.dumps({
    'candidate_sha256': hashlib.sha256(archive_bytes).hexdigest(),
    'completed_tasks': len(metrics),
    'resolved_tasks': sum(bool(m['resolved']) for m in metrics),
    'nonempty_patches': sum(p['prediction'] != 'NO_PATCH' for p in predictions),
    'scope': '12-task development slice, not hidden or leaderboard evaluation',
}, indent=2))
''',
})
notebook['cells'][0]['source'] = f'''# Gemma Evidence Coder {VARIANT.upper()} — development validation

Derived from Ryan Holbrook's official Apache-2.0 Getting Started notebook.
The exact local candidate ZIP is embedded and hashed before extraction.
Use the attached competition, official wheelhouse and Gemma 4 model inputs.
The session must use L4 x4 and internet must remain disabled.

This is a 12-task development diagnostic. Structural validation is not a model
quality measurement, and development results do not establish hidden-test rank.
'''
for c in notebook['cells']:
    if c['cell_type'] == 'code':
        compile(source(c), '<validation-notebook-cell>', 'exec')

(CANDIDATE / 'kaggle_validation.ipynb').write_text(json.dumps(notebook, ensure_ascii=False, indent=2), encoding='utf-8')
(CANDIDATE / 'development_slice.json').write_text(json.dumps({
    'selection': 'Per-repository SHA-256(instance_id) order; counts 4/4/3/1',
    'ids': SAMPLE_IDS, 'candidate_sha256': digest,
}, indent=2), encoding='utf-8')
print('Created kaggle_validation.ipynb; every Python cell parses successfully.')
