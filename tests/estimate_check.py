"""Reference-budget arithmetic and enquiry consistency in three browser engines."""
from decimal import Decimal
from urllib.parse import urlsplit, parse_qs
import re, sys
from playwright.sync_api import sync_playwright, expect

base = sys.argv[1] if len(sys.argv) > 1 else 'https://127.0.0.1:8182/'
local = urlsplit(base).hostname in ['127.0.0.1', 'localhost']
def amounts(locator):
    return [Decimal(re.sub(r'\s', '', n).replace(',', '.')) for n in re.findall(r'([\d\s]+(?:,\d{1,2})?)\s*zł', locator.inner_text())]

with sync_playwright() as p:
    for name, launcher, options in [('Edge', p.chromium, {'channel': 'msedge'}), ('Firefox', p.firefox, {}), ('WebKit', p.webkit, {})]:
        browser = launcher.launch(headless=True, **options)
        context = browser.new_context(viewport={'width': 1440, 'height': 1000}, reduced_motion='reduce', ignore_https_errors=local)
        page = context.new_page(); errors = []; requests = []
        page.on('pageerror', lambda e: errors.append(str(e)))
        page.on('request', lambda r: requests.append(r.url))
        page.goto(base, wait_until='networkidle')
        total = page.locator('#estimate-total')
        expect(page.locator('#estimate-use')).to_be_disabled()
        page.locator('#estimate-quantity').fill('60')
        assert amounts(total) == [Decimal(3000), Decimal(4800)], total.inner_text()
        page.locator('#estimate-foundation').check()
        page.locator('#estimate-extra').fill('500,00')
        page.locator('#estimate-reserve').select_option('10')
        assert amounts(total) == [Decimal(5830), Decimal(9130)]
        assert amounts(page.locator('#estimate-foundation-cost')) == [Decimal(1800), Decimal(3000)]
        assert amounts(page.locator('#estimate-reserve-cost')) == [Decimal(530), Decimal(830)]

        page.locator('#estimate-reset').click()
        page.locator('#estimate-service').select_option('bruk-material')
        page.locator('#estimate-quantity').fill('10')
        assert amounts(total) == [Decimal(1300), Decimal(1600)]
        page.locator('#estimate-mode').select_option('dimensions')
        page.locator('#estimate-length').fill('2,5'); page.locator('#estimate-width').fill('4')
        assert amounts(total) == [Decimal(1300), Decimal(1600)]

        page.locator('#estimate-service').select_option('ziemne')
        page.locator('#estimate-length').fill('10'); page.locator('#estimate-width').fill('2'); page.locator('#estimate-depth').fill('0.5')
        assert amounts(total) == [Decimal(400), Decimal(1000)]
        expect(page.locator('#estimate-foundation-field')).to_be_hidden()
        page.locator('#estimate-service').select_option('minikoparka')
        page.locator('#estimate-quantity').fill('8')
        assert amounts(total) == [Decimal(960)]
        expect(page.locator('#estimate-mode-field')).to_be_hidden()

        page.locator('#estimate-reset').click()
        for invalid in ['', '0', '-1', 'Infinity', 'NaN', '1e3', '1000001', '1,2,3', '0.00001', '<img onerror=x>', '1.2345']:
            page.locator('#estimate-quantity').fill(invalid)
            expect(page.locator('#estimate-use')).to_be_disabled()
            expect(total).to_have_text('—')
        page.locator('#estimate-quantity').fill('0,101')
        assert amounts(total) == [Decimal('5.05'), Decimal('8.08')]
        page.locator('#estimate-extra').fill('0,001')
        expect(page.locator('#estimate-use')).to_be_disabled()
        page.locator('#estimate-extra').fill('0.01'); page.locator('#estimate-reserve').select_option('15')
        assert amounts(total) == [Decimal('5.82'), Decimal('9.30')]

        page.locator('#estimate-reset').click(); page.locator('#estimate-quantity').fill('60')
        page.locator('#estimate-use').click()
        expect(page.locator('[data-step="1"]')).to_be_visible()
        expect(page.locator('#estimate-attached')).to_be_visible()
        expect(page.locator('#inquiry-service')).to_have_value('bruk')
        assert '60 m²' in page.locator('#scope').input_value()
        page.locator('#location').fill('Niedźwiedź')
        page.locator('#form-next').click()
        summary = page.locator('#inquiry-summary').inner_text()
        assert 'SZACUNEK RYNKOWY' in summary and 'nie oferta TEAM SOUTH' in summary
        assert '\n' in summary
        wa = page.locator('#whatsapp-inquiry'); expect(wa).to_be_visible()
        link = urlsplit(wa.get_attribute('href'))
        assert link.netloc == 'wa.me' and link.path == '/48797559814'
        assert parse_qs(link.query)['text'] == [summary]
        mail = urlsplit(page.locator('#mail-inquiry').get_attribute('href'))
        assert mail.path == 'biuro@teamsouth.pl' and parse_qs(mail.query)['body'] == [summary]

        page.locator('#estimate-quantity').fill('70')
        expect(page.locator('#estimate-attached')).to_be_hidden()
        assert 'SZACUNEK RYNKOWY' not in page.locator('#inquiry-summary').inner_text()
        assert 'SZACUNEK RYNKOWY' not in parse_qs(urlsplit(wa.get_attribute('href')).query)['text'][0]
        page.locator('#estimate-use').click(); page.locator('#scope').fill('Inny, ręcznie opisany zakres')
        expect(page.locator('#estimate-attached')).to_be_hidden()
        assert page.locator('#scope').input_value() == 'Inny, ręcznie opisany zakres'
        page.locator('#estimate-use').click(); page.locator('#form-back').click(); page.locator('#inquiry-service').select_option('zielen')
        expect(page.locator('#estimate-attached')).to_be_hidden()
        page.locator('#estimate-use').click(); page.locator('#form-reset').click()
        expect(page.locator('#estimate-attached')).to_be_hidden()
        expect(page.locator('#scope')).to_have_value('')
        page.locator('#estimate-reset').click()
        expect(total).to_have_text('—')

        for width in [320, 390, 768, 1024, 1440]:
            page.set_viewport_size({'width': width, 'height': 900})
            page.locator('#estimate-quantity').fill('1000000')
            page.locator('#kalkulator').scroll_into_view_if_needed()
            assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'), (name, width)
            if width <= 800: expect(page.locator('.mobile-contact')).to_be_hidden()
        assert all(urlsplit(u).netloc == urlsplit(base).netloc for u in requests), requests
        assert not errors, errors
        context.close()
        nojs = browser.new_context(java_script_enabled=False, viewport={'width': 390, 'height': 844}, ignore_https_errors=local)
        page = nojs.new_page(); page.goto(base, wait_until='networkidle')
        expect(page.locator('.estimate-layout')).to_be_hidden()
        expect(page.locator('.phone')).to_be_visible()
        nojs.close(); browser.close()
        print(f'PASS {name}: four price models, dimensions, decimals, exact rounding, extras/reserve, invalid inputs, email/WhatsApp, stale attachment removal, reset, responsive/no-JS fallback.')
