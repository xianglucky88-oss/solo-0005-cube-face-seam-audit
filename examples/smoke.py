import json
from pathlib import Path
import subprocess
import sys
import tempfile


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
doc = json.loads((HERE / 'demo.json').read_text(encoding='utf-8'))


def invoke(payload, expected_error=None):
    with tempfile.TemporaryDirectory() as temp:
        path = Path(temp) / 'source.json'
        path.write_text(json.dumps(payload), encoding='utf-8')
        cmd = [sys.executable, '-B', '-m', 'cubeseams', str(path)]
        result = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, timeout=15)
    if expected_error:
        assert result.returncode == 2 and not result.stdout and expected_error in result.stderr, result
    else:
        assert result.returncode == 0, result.stderr
        return json.loads(result.stdout)


out = invoke(doc)
assert len(out['seams']) == out['matched'] == 12
assert any(e['members'][0]['reversed'] != e['members'][1]['reversed'] for e in out['seams'])
doc['faces'][0]['pixels'][0][0] = 255
changed = invoke(doc)
assert changed['matched'] == 10 and sum(len(e['mismatches']) for e in changed['seams']) == 2
doc['faces'][0]['right'] = doc['faces'][0]['down']
invoke(doc, 'invalid or repeated face orientation')
print('production smoke: PASS (cubeseams)')
