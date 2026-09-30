"""Check real subconverter output, without printing node credentials.
Usage: python3 scripts/validate_generated.py CONFIG.yaml [PROVIDER_FIXTURE_DIR]
Requires PyYAML. The optional directory contains downloaded test provider payloads.
"""
import sys
from pathlib import Path
from urllib.parse import urlparse
import yaml

config = yaml.safe_load(Path(sys.argv[1]).read_text())
groups = {g['name']: g for g in config['proxy-groups']}
ai = '🍏 Apple Intelligence'
for name in ['台湾-固定', '香港-固定', '日本-固定', '新加坡-固定', '美国-固定', '全部-手动']:
    members = groups[name]['proxies']
    assert groups[name]['type'] == 'select', name
    assert members and 'DIRECT' not in members, f'{name}: empty group became DIRECT'
    assert members[-1] == 'REJECT', f'{name}: missing explicit empty-group guard'
assert groups[ai]['proxies'][0] == '🔐 稳定账号'
assert groups['🔐 稳定账号']['proxies'][0] == '台湾-固定'
assert groups['🧭 日常代理']['proxies'][0] == '台湾-固定'
assert groups['🎥 Netflix']['proxies'][0] == '新加坡-固定'

rules = []
for rule in config['rules']:
    fields = rule.split(',')
    if fields[0] != 'RULE-SET':
        rules.append(rule)
        continue
    provider = config['rule-providers'][fields[1]]
    assert provider['interval'] == 86400
    assert '/getruleset' not in provider['url'], 'Provider depends on converter at runtime'
    fixture = Path(sys.argv[2]) / Path(urlparse(provider['url']).path).name
    payload = yaml.safe_load(fixture.read_text())['payload']
    for entry in payload:
        if provider['behavior'] == 'domain':
            if entry.startswith('+.'):
                rules.append('DOMAIN-SUFFIX,' + entry[2:] + ',' + fields[2])
            else:
                rules.append('DOMAIN,' + entry + ',' + fields[2])
        else:
            parts = entry.split(',')
            rules.append(','.join(parts[:2] + [fields[2]] + parts[2:]))

def first_domain_match(domain):
    for rule in rules:
        parts = rule.split(',')
        kind, value = parts[:2]
        if kind == 'MATCH':
            return value
        if (kind == 'DOMAIN' and domain == value or
            kind == 'DOMAIN-SUFFIX' and (domain == value or domain.endswith('.' + value)) or
            kind == 'DOMAIN-KEYWORD' and value in domain):
            return parts[2]

cases = {}
for domain in ['guzzoni.apple.com', 'api.smoot.apple.com', 'apple-relay.apple.com',
               'apple-relay.cloudflare.com', 'apple-relay.fastly-edge.com',
               'cp4.cloudflare.com', 'apple-relay.mask.apple-dns.net',
               'chatgpt.com', 'auth.openai.com', 'cdn.oaistatic.com', 'files.oaiusercontent.com']:
    cases[domain] = ai
for domain in ['www.apple.com', 'gateway.icloud.com', 'apps.mzstatic.com',
               'gspe1-ssl.ls.apple.com', 'push.apple.com', 'time.apple.com']:
    cases[domain] = '🍎 Apple'
cases.update({'claude.ai':'🤖 AI','claude.com':'🤖 AI','gemini.google.com':'🤖 AI',
              'github.com':'💼 工作账号','accounts.google.com':'💼 工作账号',
              'login.microsoftonline.com':'💼 工作账号','onedrive.live.com':'💼 工作账号',
              'paypal.com':'💳 海外账户','amazon.com':'💳 海外账户',
              'netflix.com':'🎥 Netflix','youtube.com':'🎬 国际媒体',
              'baidu.com':'➡️ 国内','router.lan':'DIRECT',
              'unclassified-example.invalid':'🌐 漏网'})
for domain, expected in cases.items():
    actual = first_domain_match(domain)
    assert actual == expected, f'{domain}: {actual} != {expected}'
known = set(groups) | {p['name'] for p in config['proxies']} | {'DIRECT', 'REJECT'}
for group in groups.values():
    assert group['proxies'], group['name']
    assert set(group['proxies']) <= known, group['name']
for rule in rules:
    assert 'ProxyGroupName' not in rule, 'Unconverted policy placeholder'
print(f'PASS: {len(rules)} expanded rules, {len(groups)} groups; {len(cases)} routing cases and empty-group guards')
