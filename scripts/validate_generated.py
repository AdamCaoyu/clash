"""Check real subconverter output, without printing node credentials.
Usage: python3 scripts/validate_generated.py CONFIG.yaml [PROVIDER_FIXTURE_DIR]
Requires PyYAML. The optional directory contains downloaded test provider payloads.
"""
import sys
import re
from pathlib import Path
from urllib.parse import urlparse
import yaml

config = yaml.safe_load(Path(sys.argv[1]).read_text())
groups = {g['name']: g for g in config['proxy-groups']}
ai = '🍏 Apple Intelligence'
for name in ['所有','港台日新韩','台日新韩','香港','台湾','日本','新加坡','韩国','美国','其他']:
    g = groups[name+'-自动']
    assert g['type'] == 'url-test'
    assert g['interval'] == 180 and g['tolerance'] == 100
    assert g['proxies'] and 'DIRECT' not in g['proxies']
    assert g['proxies'][-1] == 'REJECT'
assert groups[ai]['proxies'][0] == '💬 ChatGPT'
assert groups['☁️ OneDrive']['proxies'][0] == 'Ⓜ️ Microsoft'
assert groups['Ⓜ️ Microsoft']['proxies'][0] == 'DIRECT'
assert config['rules'][-1] == 'MATCH,DIRECT'
for name in ['💬 ChatGPT','🧠 Claude','📘 GitHub','🔎 Google','Ⓜ️ Microsoft','💳 PayPal','🌳 Amazon']:
    assert groups[name]['type'] == 'select'
    eligible = {p['name'] for p in config['proxies']
                if not re.search('下载|公益|备用|剩余|到期|官网|异常', p['name'])}
    assert eligible <= set(groups[name]['proxies']), f'{name}: missing independently selectable nodes'

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
               'cp4.cloudflare.com', 'apple-relay.mask.apple-dns.net']:
    cases[domain] = ai
for domain in ['www.apple.com', 'gateway.icloud.com', 'apps.mzstatic.com',
               'gspe1-ssl.ls.apple.com', 'push.apple.com', 'time.apple.com']:
    cases[domain] = '🍎 Apple'
cases.update({'chatgpt.com':'💬 ChatGPT','auth.openai.com':'💬 ChatGPT',
              'cdn.oaistatic.com':'💬 ChatGPT','files.oaiusercontent.com':'💬 ChatGPT',
              'chatgpt.livekit.cloud':'💬 ChatGPT','openaiassets.blob.core.windows.net':'💬 ChatGPT',
              'claude.ai':'🧠 Claude','claude.com':'🧠 Claude','gemini.google.com':'🔎 Google',
              'grok.com':'🤖 Grok','grok.x.com':'🤖 Grok','x.com':'🕊️ Twitter(X)',
              'meta.ai':'✨ AI2','perplexity.ai':'✨ AI2','poe.com':'✨ AI1',
              'github.com':'📘 GitHub','githubcopilot.com':'📘 GitHub',
              'accounts.google.com':'🔎 Google','login.microsoftonline.com':'Ⓜ️ Microsoft',
              'login.live.com':'Ⓜ️ Microsoft','copilot.microsoft.com':'Ⓜ️ Microsoft',
              'copilot.com':'Ⓜ️ Microsoft','onedrive.live.com':'☁️ OneDrive',
              'paypal.com':'💳 PayPal','amazon.com':'🌳 Amazon',
              'netflix.com':'🎥 Netflix','youtube.com':'🎞️ YouTube',
              'baidu.com':'DIRECT','router.lan':'DIRECT',
              'unclassified-example.invalid':'DIRECT'})

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
