"""Offline regression checks for the active subconverter template."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
AI = '🍏 Apple Intelligence'

def entries(path):
    return [s.strip() for s in path.read_text().splitlines()
            if s.strip() and not s.lstrip().startswith(('#', ';'))]

def template():
    return entries(ROOT / 'Clash-Full.ini')

def local_rules():
    result = []
    for line in template():
        if not line.startswith('ruleset='):
            continue
        group, url = line[8:].split(',', 1)
        if '/AdamCaoyu/clash/' in url:
            path = ROOT / 'list' / (url.rsplit('/', 1)[-1].split('.')[0] + '.list')
            result.append((group, path))
    return result

def matches(rule, domain):
    kind, value = rule.split(',')[:2]
    return (kind == 'DOMAIN' and domain == value or
            kind == 'DOMAIN-SUFFIX' and (domain == value or domain.endswith('.' + value)) or
            kind == 'DOMAIN-KEYWORD' and value in domain)

class RulesTests(unittest.TestCase):
    def test_local_sources_exist_and_do_not_embed_policies(self):
        for _, path in local_rules():
            with self.subTest(file=path.name):
                self.assertTrue(path.is_file(), str(path))
                seen = set()
                for rule in entries(path):
                    self.assertEqual(len(rule.split(',')), 2, rule)
                    self.assertNotIn(rule, seen, rule)
                    seen.add(rule)

    def test_apple_ai_sources_precede_general_rules(self):
        sources = [line for line in template() if line.startswith('ruleset=')]
        ai = [i for i, line in enumerate(sources) if line.startswith('ruleset=' + AI + ',')]
        self.assertTrue(ai, 'Apple Intelligence has no ruleset binding')
        general = [i for i, line in enumerate(sources) if line.startswith(('ruleset=🍎 Apple,', 'ruleset=🤖 AI,', 'ruleset=🌍 国外,'))]
        self.assertLess(max(ai), min(general))

    def test_ai_routes_cover_services_without_capturing_ordinary_apple(self):
        rules = [r for group, path in local_rules() if group == AI for r in entries(path)]
        for domain in ['guzzoni.apple.com', 'api.smoot.apple.com', 'apple-relay.apple.com',
                       'apple-relay.cloudflare.com', 'apple-relay.fastly-edge.com',
                       'cp4.cloudflare.com', 'apple-relay.mask.apple-dns.net', 'chatgpt.com', 'auth.openai.com',
                       'cdn.oaistatic.com', 'files.oaiusercontent.com']:
            with self.subTest(domain=domain):
                self.assertTrue(any(matches(r, domain) for r in rules), domain)
        for domain in ['www.apple.com', 'gateway.icloud.com', 'apps.mzstatic.com',
                       'gspe1-ssl.ls.apple.com', 'push.apple.com', 'time.apple.com',
                       'example-apple-relay.invalid', 'unrelated.auth0.com', 'stripe.com']:
            with self.subTest(domain=domain):
                self.assertFalse(any(matches(r, domain) for r in rules), domain)

    def test_groups_exist_and_no_cycles(self):
        groups = {}
        for line in template():
            if line.startswith('custom_proxy_group='):
                name, kind, *members = line.split('=', 1)[1].split('`')
                self.assertNotIn(name, groups)
                groups[name] = [m[2:] for m in members if m.startswith('[]')]
        self.assertIn(AI, groups)
        self.assertEqual(groups[AI][0], '🔐 稳定账号')
        self.assertEqual(groups['🔐 稳定账号'][0], '台湾-固定')
        self.assertEqual(groups['🧭 日常代理'][0], '台湾-固定')
        self.assertEqual(groups['🎥 Netflix'][0], '新加坡-固定')
        self.assertNotIn('DIRECT', groups[AI])
        for line in template():
            if line.startswith('ruleset='):
                self.assertIn(line[8:].split(',', 1)[0], set(groups) | {'DIRECT', 'REJECT'})
        def walk(name, stack):
            if name in {'DIRECT', 'REJECT'}:
                return
            self.assertIn(name, groups)
            self.assertNotIn(name, stack)
            for child in groups[name]:
                walk(child, stack + [name])
        for name in groups:
            walk(name, [])

    def test_us_filter_excludes_download_and_unrelated_nodes(self):
        rows = [s for s in template() if s.startswith('custom_proxy_group=美国-固定`')]
        self.assertEqual(len(rows), 1)
        pattern = rows[0].split('`')[2]
        for name in ['❷gR.US神像|荐|AI x1', '美国 节点', '🇺🇸 US 01']:
            self.assertIsNotNone(re.search(pattern, name), name)
        for name in ['❻gR.US无量 [下载专用]', '⓪TJ.US空灵 [备用] [公益]', 'JP Japan', 'HK 香港']:
            self.assertIsNone(re.search(pattern, name), name)

    def test_fixed_groups_do_not_auto_switch(self):
        for name in ['台湾-固定', '美国-固定', '日本-固定', '新加坡-固定']:
            row = next((s for s in template() if s.startswith('custom_proxy_group='+name+'`')), '')
            self.assertTrue(row, name)
            self.assertEqual(row.split('`')[1], 'select')
            self.assertTrue(row.endswith('`[]REJECT'))

    def test_compatibility_template_matches_canonical(self):
        self.assertTrue((ROOT / 'config/openclash.ini').is_file())
        self.assertEqual((ROOT / 'config/openclash.ini').read_bytes(), (ROOT / 'Clash-Full.ini').read_bytes())

if __name__ == '__main__':
    unittest.main()
