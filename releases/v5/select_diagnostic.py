import json
from pathlib import Path

base = Path(__file__).resolve().parent
path = base/'kaggle_validation.ipynb'
n = json.loads(path.read_text(encoding='utf-8'))
ids = ['fastapi_15661', 'rich_3894', 'rich_3772', 'rich_3535', 'rich_3278']
for cell in n['cells']:
    src = cell['source']
    src = ''.join(src) if isinstance(src, list) else src
    if 'SAMPLE_IDS = set(' in src:
        lines = src.splitlines()
        lines = [f'SAMPLE_IDS = set({ids!r})' if line.startswith('SAMPLE_IDS = set(') else line for line in lines]
        src = '\n'.join(lines)+'\n'
        src = src.replace('assert len(SAMPLE_TASKS) == 12', 'assert len(SAMPLE_TASKS) == 5')
    src = src.replace('12-task development diagnostic', '5-task diagnostic subset with passing published reference controls')
    src = src.replace('12-task development slice, not hidden or leaderboard evaluation', '5-task diagnostic subset with passing public reference controls; not a hidden-rank estimate')
    if cell['cell_type'] == 'code':
        compile(src, '<candidate>', 'exec')
    cell['source'] = src
path.write_text(json.dumps(n, indent=1), encoding='utf-8')
(base/'development_slice.json').write_text(json.dumps({'ids': ids, 'selection': 'Five passing public-reference verification controls from the previously fixed twelve-task slice. Selected diagnostic, not representative hidden evaluation.'}, indent=2), encoding='utf-8')
print('Selected 5 reference-passing diagnostic tasks')
