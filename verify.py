"""Dependency-free release check: paths, anchors, duplicate IDs and privacy boundary."""
from pathlib import Path
from html.parser import HTMLParser
import re

ROOT = Path(__file__).parent / 'dist'
class Page(HTMLParser):
    def __init__(self): super().__init__(); self.ids = []; self.refs = []; self.anchors = []; self.links = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a: self.ids.append(a['id'])
        if tag in ['script', 'img'] and a.get('src'): self.refs.append(a['src'])
        if tag == 'link' and a.get('href'): self.refs.append(a['href'])
        if 'srcset' in a: self.refs.extend(part.strip().split()[0] for part in a['srcset'].split(','))
        if tag == 'a':
            href = a.get('href', '')
            if href.startswith('#'): self.anchors.append(href[1:])
            elif href and not re.match(r'\w+:', href): self.refs.append(href)
            self.links.append(href)
page = Page(); page.feed((ROOT / 'index.html').read_text(encoding='utf-8'))
assert len(page.ids) == len(set(page.ids)), 'Duplicate HTML IDs'
assert set(page.anchors) <= set(page.ids), 'Broken anchors'
for ref in page.refs:
    assert not re.match(r'\w+://', ref), 'Unexpected third-party initial asset: ' + ref
    assert (ROOT / ref).is_file(), 'Missing local asset: ' + ref
for css in ROOT.rglob('*.css'):
    for ref in re.findall(r'url\([\'"]?([^\)\'\"]+)', css.read_text(encoding='utf-8')):
        assert (css.parent / ref).is_file(), ref
code = (ROOT / 'app.js').read_text(encoding='utf-8')
for api in ['localStorage', 'sessionStorage', 'fetch(', 'XMLHttpRequest', 'sendBeacon']:
    assert api not in code, 'Unexpected persistence or submission: ' + api
assert '{{' not in (ROOT / 'index.html').read_text(encoding='utf-8'), 'Unrendered template'
assert b'BEGIN:VCARD\r\nVERSION:3.0' in (ROOT / 'team-south.vcf').read_bytes()
print(f'PASS static release: {len(page.ids)} unique IDs, {len(page.refs)} local asset references, anchors and privacy boundary.')
