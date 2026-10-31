"""Build an isolated public-reference verification control; never agent input."""
import json
from pathlib import Path

base = Path(__file__).resolve().parent
n = json.loads((base / 'kaggle_validation.ipynb').read_text(encoding='utf-8'))
bootstrap = next(c for c in n['cells'] if c['cell_type'] == 'code')
code = '''import asyncio
import concurrent.futures
import json
import time
from adk_submission import ModelRegistry
from swegemma.config import EvalConfig
from swegemma.evaluate import Evaluator
from swegemma.models import load_tasks
from swegemma.deduplication import resolve_task_snapshot_paths
from swegemma.harness.verification import verify_task
from swegemma.results import append_task_result

DATA_DIR = Path('/kaggle/input/competitions/gemma-4-developer-agent')
OUT = Path('/kaggle/working/gold_control')
OUT.mkdir(parents=True, exist_ok=True)
config = EvalConfig(tasks_path=DATA_DIR/'tasks.jsonl', snapshots_dir=DATA_DIR/'snapshots',
    results_dir=OUT, submission_dir=OUT, models=ModelRegistry(), sandbox='subprocess',
    wheels_dir=DATA_DIR/'wheels', verification_timeout_seconds=300)
evaluator = Evaluator(config)
ids = {'fastapi_11355', 'fastapi_14512', 'fastapi_14953', 'fastapi_15661',
       'rich_3894', 'rich_3535', 'rich_3772', 'rich_3278',
       'requests_7505', 'requests_7427', 'requests_6757', 'httpx_3672'}
tasks = [t for t in load_tasks(config.tasks_path) if t.instance_id in ids]
assert len(tasks) == 12
results = []
for i, raw in enumerate(tasks, 1):
    task = evaluator._hydrate_task_from_secret(raw)
    assert task.patch.strip(), f'No public reference patch for {task.instance_id}'
    snapshot, base_snapshot, patch_path = resolve_task_snapshot_paths(config.snapshots_dir, task.instance_id, task.repo)
    print(f'[{i}/12] Public reference control: {task.instance_id}', flush=True)
    async def check():
        return await verify_task(evaluator.docker, config, task, snapshot,
            base_snapshot_path=base_snapshot, patch_path=patch_path,
            agent_patch=task.patch, start_time=time.perf_counter())
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
        result = pool.submit(lambda: asyncio.run(check())).result()
    results.append(result)
    append_task_result(result, OUT, results)
    print(f'  -> reference_resolved={result.resolved}, exit_code={result.test_exit_code}, error={result.error}', flush=True)
print('This control verifies published reference patches only. It does not measure agent quality.')
shutil.make_archive('/kaggle/working/gold_control_results', 'zip', OUT)
'''
n['cells'] = [
    {'cell_type':'markdown','metadata':{},'source':'# Public reference patch control\n\nOffline verification only. No model, no generated patches, no agent access to reference answers. Derived from the official starter bootstrap and verification API.'},
    bootstrap,
    {'cell_type':'code','metadata':{},'source':code,'outputs':[],'execution_count':None},
]
for cell in n['cells']:
    if cell['cell_type'] == 'code':
        src = cell['source']
        compile(''.join(src) if isinstance(src, list) else src, '<control>', 'exec')
(base/'kaggle_gold_control.ipynb').write_text(json.dumps(n, indent=1), encoding='utf-8')
print('Created isolated public-reference control notebook')
