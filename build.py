"""Render the static site from a single HTML template and an explicit gallery catalogue."""
from pathlib import Path
from html import escape
import hashlib
import json
import base64
from urllib.parse import quote

ROOT = Path(__file__).parent
gallery = [
    (26, 'rekreacja', 'Rekreacja', 'Kolorowa przestrzeń rekreacyjna'),
    (8, 'nawierzchnie', 'Nawierzchnie', 'Nawierzchnia z kostki brukowej'),
    (9, 'zielen', 'Tereny zielone', 'Ogród i zagospodarowanie terenu'),
    (7, 'ziemne', 'Roboty ziemne', 'Minikoparka w terenie'),
    (1, 'nawierzchnie', 'Infrastruktura', 'Chodnik wzdłuż drogi'),
    (19, 'nawierzchnie', 'Nawierzchnie', 'Prace przy obiekcie przemysłowym'),
    (5, 'ziemne', 'Sprzęt', 'Koparka kołowa na placu prac'),
    (30, 'rekreacja', 'Rekreacja', 'Nawierzchnie strefy aktywności'),
    (13, 'zielen', 'Tereny zielone', 'Zielone otoczenie budynku'),
    (2, 'nawierzchnie', 'Nawierzchnie', 'Układanie kostki przy budynku'),
    (10, 'rekreacja', 'Rekreacja', 'Przestrzeń sportowa z góry'),
    (23, 'ziemne', 'Sprzęt', 'Zaplecze sprzętowe'),
    (24, 'zielen', 'Tereny zielone', 'Ścieżki i przygotowanie ogrodu'),
    (15, 'rekreacja', 'Rekreacja', 'Otoczenie terenu rekreacyjnego'),
    (16, 'zielen', 'Tereny zielone', 'Alejka w przestrzeni zielonej'),
    (18, 'nawierzchnie', 'Nawierzchnie', 'Szczegół nawierzchni brukowej'),
]
cards = []
image_metadata = {record['id']: record for record in json.loads((ROOT / 'dist/assets/sources.json').read_text(encoding='utf-8'))['gallery']}
for number, category, label, caption in gallery:
    small, large = (f'assets/work-{number:02}-{size}.webp' for size in [600, 1400])
    for asset in [small, large]:
        if not (ROOT / 'dist' / asset).is_file(): raise FileNotFoundError(asset)
    metadata = image_metadata[number]
    scale = min(1, 600 / max(metadata['width'], metadata['height']))
    width, height = round(metadata['width'] * scale), round(metadata['height'] * scale)
    cards.append(f'<figure class="gallery-card" data-category="{category}"><a class="gallery-link" href="{large}" aria-label="Powiększ: {escape(caption)}"><img src="{small}" alt="{escape(caption)} — galeria TEAM SOUTH" width="{width}" height="{height}" loading="lazy" decoding="async"><span class="gallery-zoom" aria-hidden="true">+</span></a><figcaption><span>{escape(label)}</span><strong>{escape(caption)}</strong></figcaption></figure>')
template = (ROOT / 'site.html').read_text(encoding='utf-8')
assert template.count('{{GALLERY}}') == 1
html = template.replace('{{GALLERY}}', '\n'.join(cards))
whatsapp_message = 'Dzień dobry, chciałbym zapytać o ofertę TEAM SOUTH.\n\nZakres prac: \nMiejscowość: \nPlanowany termin: '
whatsapp_url = 'https://wa.me/48797559814?text=' + quote(whatsapp_message, safe='')
html = html.replace('{{WHATSAPP_URL}}', escape(whatsapp_url, quote=True))
integrities = {}
for source, target, attribute in [('site.css', 'style.css', 'href'), ('site.js', 'app.js', 'src')]:
    content = (ROOT / source).read_text(encoding='utf-8').encode('utf-8')
    version = hashlib.sha256(content).hexdigest()[:12]
    integrity = 'sha384-' + base64.b64encode(hashlib.sha384(content).digest()).decode('ascii')
    integrities[target] = integrity
    html = html.replace(f'{attribute}="{target}"', f'{attribute}="{target}?v={version}" integrity="{integrity}" crossorigin="anonymous"')
    (ROOT / 'dist' / target).write_bytes(content)
font_css = ROOT / 'dist/assets/fonts/fonts.css'
font_content = font_css.read_text(encoding='utf-8').encode('utf-8')
font_css.write_bytes(font_content)
font_integrity = 'sha384-' + base64.b64encode(hashlib.sha384(font_content).digest()).decode('ascii')
font_version = hashlib.sha256(font_content).hexdigest()[:12]
html = html.replace('href="assets/fonts/fonts.css"', f'href="assets/fonts/fonts.css?v={font_version}" integrity="{font_integrity}" crossorigin="anonymous"')
csp = f"default-src 'none'; script-src '{integrities['app.js']}'; style-src 'self'; img-src 'self'; font-src 'self'; connect-src 'none'; object-src 'none'; base-uri 'none'; form-action 'none'; frame-src https://www.google.com https://maps.google.com; worker-src 'none'; upgrade-insecure-requests"
html = html.replace('{{CSP}}', csp)
(ROOT / 'dist/index.html').write_text(html, encoding='utf-8')
(ROOT / 'dist/team-south.vcf').write_bytes(('BEGIN:VCARD\r\nVERSION:3.0\r\nFN:TEAM SOUTH\r\nN:TEAM SOUTH;;;;\r\nORG:TEAM SOUTH\r\nTEL;TYPE=WORK,VOICE:+48797559814\r\nEMAIL;TYPE=WORK:biuro@teamsouth.pl\r\nADR;TYPE=WORK:;;Niedźwiedź 145;Niedźwiedź;;34-735;Polska\r\nURL:https://teamsouth.pl/\r\nEND:VCARD\r\n').encode('utf-8'))
print(f'Built static site with {len(gallery)} gallery photographs.')
