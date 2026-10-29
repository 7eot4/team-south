"""Static release security gates. No network or third-party dependencies."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit
import base64, hashlib, re, subprocess, xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / 'dist'
class Document(HTMLParser):
    def __init__(self): super().__init__(); self.tags=[]
    def handle_starttag(self, tag, attrs): self.tags.append((tag,dict(attrs)))
doc=Document();doc.feed((DIST/'index.html').read_text(encoding='utf-8'))
policy=next(a['content'] for t,a in doc.tags if t=='meta' and a.get('http-equiv','').lower()=='content-security-policy')
assert all(rule in policy for rule in ["default-src 'none'", "connect-src 'none'", "form-action 'none'", "object-src 'none'", "base-uri 'none'"])
assert 'unsafe-inline' not in policy and 'unsafe-eval' not in policy
assert 'frame-ancestors' not in policy, 'frame-ancestors is not enforceable through meta'
assert next(a['content'] for t,a in doc.tags if t=='meta' and a.get('name')=='referrer')=='no-referrer'
script_integrities=[]
for tag,a in doc.tags:
    assert not any(name.lower().startswith('on') for name in a), ('Inline event handler',tag)
    assert 'style' not in a, ('Unexpected inline style',tag)
    assert tag not in ['object','embed','base'],tag
    for attribute in ['href','src','action']:
        value=a.get(attribute,'')
        assert not value.lower().startswith(('javascript:','http:','data:')),value
    if a.get('target')=='_blank': assert {'noopener','noreferrer'}<=set(a.get('rel','').split()),a
    if tag=='script' or (tag=='link' and a.get('rel')=='stylesheet' and 'integrity' in a):
        reference=a.get('src') or a.get('href')
        content=(DIST/urlsplit(reference).path).read_bytes()
        expected='sha384-'+base64.b64encode(hashlib.sha384(content).digest()).decode()
        assert a.get('integrity')==expected,reference
        if tag=='script': script_integrities.append(expected)
assert len(script_integrities)==1
assert f"script-src '{script_integrities[0]}'" in policy
assert doc.tags.index(next((t,a) for t,a in doc.tags if t=='meta' and a.get('http-equiv','').lower()=='content-security-policy')) < next(i for i,(t,a) in enumerate(doc.tags) if t in ['script','link'])
for path in DIST.rglob('*.svg'):
    root=ET.parse(path).getroot()
    for element in root.iter():
        assert element.tag.split('}')[-1] not in ['script','foreignObject'],path
        assert not any(name.lower().startswith('on') for name in element.attrib),path
        for name,value in element.attrib.items():
            if name.split('}')[-1] in ['href','src']: assert not value or value.startswith('#'),path
code=(ROOT/'site.js').read_text(encoding='utf-8')
for sink in ['innerHTML','outerHTML','insertAdjacentHTML','document.write','eval(', 'new Function(', 'localStorage','sessionStorage','sendBeacon','XMLHttpRequest']:
    assert sink not in code,sink
workflow=(ROOT/'.github/workflows/pages.yml').read_text(encoding='utf-8')
actions=re.findall(r'uses:\s*([^\s]+)',workflow)
assert actions and all(re.fullmatch(r'[^@]+@[a-f0-9]{40}',action) for action in actions)
tracked=subprocess.check_output(['git','ls-files'],cwd=ROOT,text=True).splitlines()
patterns=[re.compile(r'\bgh[pousr]_[A-Za-z0-9]{30,}\b'),re.compile(r'\bAKIA[0-9A-Z]{16}\b'),re.compile(r'-----BEGIN (?:[A-Z]+ )?PRIVATE KEY-----')]
for relative in tracked:
    path=Path(relative)
    assert '#Done' not in path.parts, 'Protected tree is out of scope'
    assert not relative.startswith(('.local/','.env','.git/')),relative
    if path.suffix.lower() in ['.py','.js','.css','.html','.md','.json','.yml','.txt']:
        text=(ROOT/path).read_text(encoding='utf-8-sig')
        assert not any(pattern.search(text) for pattern in patterns), 'Potential secret: '+relative
print('PASS security static: strict script hash, SRI, CSP, safe links/SVG, no dangerous DOM sinks, pinned Actions and tracked-file secret patterns.')
