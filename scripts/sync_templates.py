"""Sync the legacy template URL and native Clash versions of our local lists."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
(ROOT / 'Clash-Full.ini').write_bytes((ROOT / 'config/openclash.ini').read_bytes())
output = ROOT / 'rules/clash'
output.mkdir(parents=True, exist_ok=True)
for name in ['Apple', 'ChatGPT', 'CaoyuDirect', 'CaoyuProxy', 'AI2']:
    rules = [line.strip() for line in (ROOT / 'list' / (name + '.list')).read_text().splitlines()
             if line.strip() and not line.lstrip().startswith('#')]
    if any(len(line.split(',')) != 2 for line in rules):
        raise ValueError(f'{name}: local domain lists must not contain policy fields')
    (output / (name + '.yaml')).write_text(
        '# Generated from list/' + name + '.list; do not edit independently.\npayload:\n' +
        ''.join('  - ' + repr(line) + '\n' for line in rules))
print('Synced Clash-Full.ini and 5 local rule providers')
