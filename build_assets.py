"""Optimize original company assets. Requires Pillow; not required for deployment."""
from pathlib import Path
import json, re, urllib.request
from PIL import Image, ImageOps

ROOT = Path(__file__).parent
ASSETS = ROOT / 'dist/assets'
catalogue = ROOT / 'dist/assets/sources.json'
records = json.loads(catalogue.read_text(encoding='utf-8'))['gallery'] if catalogue.exists() else json.loads((ROOT / '.local/research/gallery-sources.json').read_text(encoding='utf-8'))
selected = [1, 2, 5, 7, 8, 9, 10, 13, 15, 16, 18, 19, 23, 24, 26, 30]
manifest = []
for number in selected:
    record = next(r for r in records if r['id'] == number)
    original = ROOT / f'.local/research/gallery-{number:02}.jpg'
    if not original.exists():
        original.parent.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(record['source'], original)
    im = ImageOps.exif_transpose(Image.open(original)).convert('RGB')
    for size in [600, 1400]:
        resized = im.copy()
        resized.thumbnail((size, size))
        resized.save(ASSETS / f'work-{number:02}-{size}.webp', quality=82, method=6)
    if number == 26:
        ImageOps.fit(im, (1200, 630)).save(ASSETS / 'share.jpg', quality=85, optimize=True)
    manifest.append({'id': number, 'source': record['source'], 'width': im.width, 'height': im.height})

logo = Image.open(ASSETS / 'logo.png')
logo.thumbnail((420, 300))
logo.save(ASSETS / 'logo.webp', lossless=True, method=6)
# Original symbol extracted from the same logo; no redrawing or generated replacement.
mark = Image.open(ASSETS / 'logo.png').crop((368, 0, 1195, 825))
mark.thumbnail((64, 64))
mark.save(ROOT / 'dist/favicon.png')

font_dir = ASSETS / 'fonts'
font_dir.mkdir(exist_ok=True)
css_parts = []
for family, slug, weights in [('Manrope', 'manrope', '400..800'), ('Barlow+Condensed', 'barlow-condensed', '600')]:
    request = urllib.request.Request(f'https://fonts.googleapis.com/css2?family={family}:wght@{weights}&display=swap', headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'})
    css = urllib.request.urlopen(request).read().decode()
    count = 0
    for comment, rule in re.findall(r'/\* (.*?) \*/\s*(@font-face\s*\{.*?\})', css, re.S):
        if comment not in ['latin-ext', 'latin']: continue
        source = re.search(r'url\((.*?)\)', rule).group(1)
        extension = 'woff2' if 'woff2' in rule else 'ttf'
        filename = f'{slug}-{comment}.{extension}'
        urllib.request.urlretrieve(source, font_dir / filename)
        css_parts.append(rule.replace(source, filename))
        count += 1
    if not count: raise RuntimeError('No Latin font subsets: ' + family)
(font_dir / 'fonts.css').write_text('\n'.join(css_parts), encoding='utf-8')
for slug, directory in [('manrope', 'manrope'), ('barlow-condensed', 'barlowcondensed')]:
    license_file = font_dir / f'{slug}-OFL.txt'
    urllib.request.urlretrieve(f'https://raw.githubusercontent.com/google/fonts/main/ofl/{directory}/OFL.txt', license_file)
    license_file.write_text('\n'.join(line.rstrip() for line in license_file.read_text(encoding='utf-8').splitlines()) + '\n', encoding='utf-8')
(ASSETS / 'sources.json').write_text(json.dumps({'company': 'https://teamsouth.pl/', 'gallery': manifest, 'logo': 'https://teamsouth.pl/_/images/pl/webpage_1/lysc2ncz/element_697/logo_main_page.png', 'note': 'Company gallery; no verified association between individual photographs and named projects.'}, ensure_ascii=False, indent=2), encoding='utf-8')
print('Prepared', len(selected), 'photographs, original logo, favicon, local fonts and source manifest.')
