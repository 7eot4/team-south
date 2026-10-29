"""Render the static site from a single HTML template and an explicit gallery catalogue."""
from pathlib import Path
from html import escape
import shutil

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
for number, category, label, caption in gallery:
    small, large = (f'assets/work-{number:02}-{size}.webp' for size in [600, 1400])
    for asset in [small, large]:
        if not (ROOT / 'dist' / asset).is_file(): raise FileNotFoundError(asset)
    cards.append(f'<figure class="gallery-card" data-category="{category}"><a class="gallery-link" href="{large}" aria-label="Powiększ: {escape(caption)}"><img src="{small}" alt="{escape(caption)} — galeria TEAM SOUTH" width="600" height="450" loading="lazy" decoding="async"><span class="gallery-zoom" aria-hidden="true">+</span></a><figcaption><span>{escape(label)}</span><strong>{escape(caption)}</strong></figcaption></figure>')
template = (ROOT / 'site.html').read_text(encoding='utf-8')
assert template.count('{{GALLERY}}') == 1
(ROOT / 'dist/index.html').write_text(template.replace('{{GALLERY}}', '\n'.join(cards)), encoding='utf-8')
shutil.copyfile(ROOT / 'site.css', ROOT / 'dist/style.css')
shutil.copyfile(ROOT / 'site.js', ROOT / 'dist/app.js')
(ROOT / 'dist/team-south.vcf').write_bytes(('BEGIN:VCARD\r\nVERSION:3.0\r\nFN:TEAM SOUTH\r\nORG:TEAM SOUTH\r\nTEL;TYPE=WORK,VOICE:+48797559814\r\nEMAIL;TYPE=WORK:biuro@teamsouth.pl\r\nADR;TYPE=WORK:;;Niedźwiedź 145;Niedźwiedź;;34-735;Polska\r\nURL:https://teamsouth.pl/\r\nEND:VCARD\r\n').encode('utf-8'))
print(f'Built static site with {len(gallery)} gallery photographs.')
