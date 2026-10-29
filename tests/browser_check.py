"""Browser acceptance checks. Run: python tests/browser_check.py [base-url]."""
from pathlib import Path
import sys
from urllib.parse import urlsplit, parse_qs
from playwright.sync_api import sync_playwright, expect

BASE = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8177/'
ARTIFACTS = Path(__file__).resolve().parents[1] / '.local/qa-v2'
ARTIFACTS.mkdir(parents=True, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(channel='msedge', headless=True)
    context = browser.new_context(viewport={'width': 1440, 'height': 1000}, locale='pl-PL', permissions=['clipboard-read', 'clipboard-write'], accept_downloads=True)
    page = context.new_page()
    errors, failed, requests = [], [], []
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.on('response', lambda response: failed.append((response.status, response.url)) if response.status >= 400 else None)
    page.on('request', lambda request: requests.append(request.url))
    page.goto(BASE, wait_until='networkidle')
    expect(page.locator('h1')).to_contain_text('Roboty ziemne')
    assert page.locator('.brand img').evaluate('(i)=>i.complete && i.naturalWidth > 0')
    assert not any(urlsplit(url).netloc != urlsplit(BASE).netloc for url in requests), requests
    assert page.locator('iframe').count() == 0
    for key, title in [('bruk', 'Podjazdy, chodniki i nawierzchnie'), ('drogi', 'Drogi i ciągi komunikacyjne'), ('rekreacja', 'Place zabaw i tereny rekreacyjne'), ('zielen', 'Parki, ogrody i otoczenie budynków'), ('ziemne', 'Wykopy i niwelacja terenu')]:
        page.locator(f'[data-service="{key}"]').click()
        expect(page.locator('#service-title')).to_have_text(title)
        expect(page.locator('.choose-service')).to_have_attribute('data-select-service', key)
    print('PASS services: all five categories and enquiry selection')

    expect(page.locator('.gallery-card:visible')).to_have_count(6)
    page.locator('#gallery-more').click()
    expect(page.locator('.gallery-card:visible')).to_have_count(12)
    page.locator('#gallery-more').click()
    expect(page.locator('.gallery-card:visible')).to_have_count(16)
    expect(page.locator('#gallery-more')).to_be_hidden()
    for category, count in [('nawierzchnie', 5), ('ziemne', 3), ('rekreacja', 4), ('zielen', 4)]:
        page.locator(f'[data-filter="{category}"]').click()
        expect(page.locator('.gallery-card:visible')).to_have_count(count)
        assert page.locator('.gallery-card:visible').evaluate_all('(items)=>items.every(i=>i.dataset.category === "'+category+'")')
    trigger = page.locator('.gallery-card:visible .gallery-link').first
    trigger.click()
    expect(page.locator('#lightbox')).to_be_visible()
    caption = page.locator('#lightbox-caption').inner_text()
    page.keyboard.press('ArrowRight')
    assert page.locator('#lightbox-caption').inner_text() != caption
    page.keyboard.press('ArrowLeft')
    expect(page.locator('#lightbox-caption')).to_have_text(caption)
    page.keyboard.press('Tab')
    assert page.evaluate('!!document.activeElement.closest("#lightbox")')
    page.keyboard.press('Escape')
    expect(page.locator('#lightbox')).to_be_hidden()
    expect(trigger).to_be_focused()
    page.locator('[data-filter="all"]').click()
    print('PASS gallery: all filters, pagination, lightbox keyboard, modal focus and Escape')

    page.locator('#form-next').click()
    expect(page.locator('[data-step="0"]')).to_be_visible()
    page.locator('[data-service="bruk"]').click()
    page.locator('.choose-service').click()
    expect(page.locator('#inquiry-service')).to_have_value('bruk')
    page.locator('#form-next').click()
    expect(page.locator('[data-step="1"]')).to_be_visible()
    page.locator('#form-next').click()
    expect(page.locator('[data-step="1"]')).to_be_visible()
    page.locator('#location').fill('  ')
    page.locator('#form-next').click()
    expect(page.locator('[data-step="1"]')).to_be_visible()
    page.locator('#location').fill('Niedźwiedź')
    page.locator('#scope').fill('Podjazd 50 m²')
    page.locator('#description').fill('<img src=x onerror=alert(1)> — opis testowy')
    page.locator('#documentation').check()
    page.locator('#form-next').click()
    expect(page.locator('[data-step="2"]')).to_be_visible()
    summary = page.locator('#inquiry-summary').inner_text()
    assert all(text in summary for text in ['Brukarstwo', 'Niedźwiedź', 'Podjazd 50 m²', '<img src=x onerror=alert(1)>', 'mam do przekazania'])
    assert page.locator('#inquiry-summary img').count() == 0
    mail = urlsplit(page.locator('#mail-inquiry').get_attribute('href'))
    assert mail.scheme == 'mailto' and mail.path == 'biuro@teamsouth.pl'
    assert parse_qs(mail.query)['body'][0] == summary
    wa = urlsplit(page.locator('#whatsapp-inquiry').get_attribute('href'))
    assert wa.scheme == 'https' and wa.netloc == 'wa.me' and wa.path == '/48797559814'
    assert parse_qs(wa.query)['text'][0] == summary
    page.locator('#copy-inquiry').click()
    expect(page.locator('#form-status')).to_have_text('Skopiowano.')
    assert page.evaluate('navigator.clipboard.readText()').replace('\r\n', '\n') == summary
    page.evaluate("window.savedClipboard = navigator.clipboard; Object.defineProperty(navigator, 'clipboard', {value: {writeText: () => Promise.reject(new Error('denied'))}, configurable: true})")
    page.locator('#copy-inquiry').click()
    expect(page.locator('#form-status')).to_contain_text('Kopiowanie niedostępne')
    assert page.evaluate('getSelection().toString()') == summary
    page.evaluate("Object.defineProperty(navigator, 'clipboard', {value: window.savedClipboard, configurable: true})")
    with page.expect_download() as download_info: page.locator('#download-inquiry').click()
    assert Path(download_info.value.path()).read_text(encoding='utf-8-sig') == summary
    page.locator('.inquiry-form').screenshot(path=str(ARTIFACTS / 'form-summary.png'))
    page.set_viewport_size({'width': 320, 'height': 844})
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), 'summary overflow at 320'
    page.locator('.inquiry-form').screenshot(path=str(ARTIFACTS / 'mobile-summary.png'))
    page.set_viewport_size({'width': 1440, 'height': 1000})
    page.locator('#form-back').click()
    page.locator('#description').fill('ą' * 800)
    page.locator('#form-next').click()
    expect(page.locator('#mail-inquiry')).to_be_hidden()
    expect(page.locator('#whatsapp-inquiry')).to_be_hidden()
    expect(page.locator('#long-message-note')).to_be_visible()
    page.locator('#form-reset').click()
    expect(page.locator('#inquiry-service')).to_have_value('')
    expect(page.locator('#long-message-note')).to_be_hidden()
    page.locator('.measure-tool summary').click()
    page.locator('#measure-length').fill('10')
    page.locator('#measure-width').fill('5')
    page.locator('#measure-depth').fill('0.3')
    expect(page.locator('#measure-result')).to_contain_text('50 m²')
    expect(page.locator('#measure-result')).to_contain_text('15 m³')
    page.locator('#use-measure').click()
    expect(page.locator('[data-step="0"]')).to_be_visible()
    expect(page.locator('#scope')).to_have_value('Powierzchnia: 50 m²; objętość geometryczna: 15 m³')
    page.locator('#measure-width').fill('-5')
    expect(page.locator('#use-measure')).to_be_disabled()
    page.locator('#measure-length').fill('0.01')
    page.locator('#measure-width').fill('0.01')
    page.locator('#measure-depth').fill('0.01')
    expect(page.locator('#measure-result')).to_contain_text('0,000001 m³')
    page.locator('#form-reset').click()
    page.locator('.measure-tool summary').click()
    print('PASS enquiry: required fields, whitespace, safe text, exact mailto body, clipboard, TXT, long-message fallback, reset and measurement')

    page.locator('.faq-list summary').first.click()
    expect(page.locator('.faq-list details').first).to_have_attribute('open', '')
    page.locator('.faq-list summary').first.click()
    page.locator('.copy').click()
    expect(page.locator('.copy-status')).to_have_text('Skopiowano.')
    assert page.evaluate('navigator.clipboard.readText()') == 'biuro@teamsouth.pl'
    page.evaluate("Object.defineProperty(navigator, 'share', {value: undefined, configurable: true})")
    page.locator('#share-site').click()
    expect(page.locator('.copy-status')).to_have_text('Skopiowano link do strony.')
    assert page.evaluate('navigator.clipboard.readText()') == 'https://7eot4.github.io/team-south/'
    page.locator('#open-privacy').click()
    expect(page.locator('#privacy-dialog')).to_be_visible()
    page.keyboard.press('Escape')
    expect(page.locator('#privacy-dialog')).to_be_hidden()
    for network in ['Facebook', 'Instagram', 'LinkedIn']:
        for group in ['.header-socials', '.footer-socials']:
            icon = page.locator(f'{group} [data-social="{network}"]')
            assert icon.evaluate('(button)=>button.tagName') == 'BUTTON'
            icon.click()
            expect(page.locator('#social-dialog')).to_be_visible()
            expect(page.locator('#social-dialog-title')).to_have_text(network)
            expect(page.locator('#social-dialog')).to_contain_text('Profil nie jest jeszcze podłączony.')
            assert page.locator('#social-dialog a[href^="https://"]').count() == 0
            page.locator('#social-dialog').screenshot(path=str(ARTIFACTS / f'social-{network.lower()}.png'))
            page.keyboard.press('Escape')
            expect(page.locator('#social-dialog')).to_be_hidden()
            expect(icon).to_be_focused()
    for link in page.locator('.whatsapp-link').all():
        destination = urlsplit(link.get_attribute('href'))
        assert destination.netloc == 'wa.me' and destination.path == '/48797559814'
        assert 'Dzień dobry' in parse_qs(destination.query)['text'][0]
        assert 'Zakres prac:' in parse_qs(destination.query)['text'][0]
    context.route('https://wa.me/**', lambda route: route.fulfill(status=200, content_type='text/html', body='<html><body>Test przekazania do WhatsApp</body></html>'))
    with page.expect_popup() as popup_info: page.locator('.header-socials .whatsapp-link').click()
    popup = popup_info.value
    popup.wait_for_load_state('domcontentloaded')
    assert urlsplit(popup.url).netloc == 'wa.me'
    assert 'TEAM SOUTH' in parse_qs(urlsplit(popup.url).query)['text'][0]
    popup.close()
    with page.expect_download() as vcard_info: page.get_by_role('link', name='Zapisz kontakt').click()
    vcard = Path(vcard_info.value.path()).read_text(encoding='utf-8')
    assert all(item in vcard for item in ['FN:TEAM SOUTH', '+48797559814', 'biuro@teamsouth.pl'])
    assert not any(urlsplit(url).netloc != urlsplit(BASE).netloc for url in requests)
    print('PASS FAQ, three social placeholders, email, sharing fallback, privacy dialog, vCard; zero third-party requests before map consent')

    for width in [1440, 1024, 768, 540, 390, 320]:
        page.set_viewport_size({'width': width, 'height': 900})
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), f'overflow at {width}'
        if width < 801:
            for icon in page.locator('.header-socials .social-button').all():
                expect(icon).to_be_visible()
                box = icon.bounding_box()
                assert 0 <= box['x'] and box['x'] + box['width'] <= width
            mobile_icon = page.locator('.header-socials [data-social="Facebook"]')
            mobile_icon.click()
            expect(page.locator('#social-dialog')).to_be_visible()
            page.keyboard.press('Escape')
            expect(mobile_icon).to_be_focused()
            page.locator('.menu').click()
            expect(page.locator('.menu')).to_have_attribute('aria-expanded', 'true')
            page.locator('#navigation').get_by_role('link', name='Oferta', exact=True).click()
            expect(page.locator('.menu')).to_have_attribute('aria-expanded', 'false')
    page.set_viewport_size({'width': 1440, 'height': 1000})
    for image in page.locator('img[src]:visible').all():
        image.scroll_into_view_if_needed(); expect(image).to_have_js_property('complete', True)
        assert image.evaluate('(i)=>i.naturalWidth > 0')
    page.locator('#poczatek').scroll_into_view_if_needed()
    page.locator('.hero').screenshot(path=str(ARTIFACTS / 'desktop-hero.png'))
    page.locator('#oferta').screenshot(path=str(ARTIFACTS / 'desktop-services.png'))
    page.locator('.site-header').screenshot(path=str(ARTIFACTS / 'social-icons.png'))
    page.evaluate("scrollTo({top:0,behavior:'instant'})")
    page.screenshot(path=str(ARTIFACTS / 'desktop.png'), full_page=True)
    page.set_viewport_size({'width': 390, 'height': 844})
    page.locator('#poczatek').scroll_into_view_if_needed()
    page.evaluate("scrollTo({top:0,behavior:'instant'})")
    page.screenshot(path=str(ARTIFACTS / 'mobile.png'), full_page=True)
    page.locator('.hero').screenshot(path=str(ARTIFACTS / 'mobile-hero.png'))
    page.emulate_media(reduced_motion='reduce')
    assert page.evaluate('getComputedStyle(document.documentElement).scrollBehavior') == 'auto'
    print('PASS six viewport widths, mobile navigation, image loads and reduced motion')

    page.route('https://www.google.com/maps**', lambda route: route.fulfill(status=200, content_type='text/html', body='<html><body>Mapa — odpowiedź testowa</body></html>'))
    page.locator('#load-map').click()
    expect(page.locator('#map-container iframe')).to_have_attribute('title', 'Mapa lokalizacji TEAM SOUTH — Niedźwiedź 145')
    expect(page.locator('#load-map')).to_have_count(0)
    page.reload(wait_until='networkidle')
    expect(page.locator('#scope')).to_have_value('')
    expect(page.locator('#inquiry-service')).to_have_value('')
    assert page.evaluate('localStorage.length') == 0
    assert page.evaluate('sessionStorage.length') == 0
    assert not errors, errors
    assert not failed, failed
    print('PASS opt-in map insertion, no restored form data, no storage, no JS errors or HTTP failures')

    nojs = browser.new_context(java_script_enabled=False, viewport={'width':390,'height':844})
    fallback = nojs.new_page(); fallback.goto(BASE, wait_until='networkidle')
    expect(fallback.locator('.inquiry-form')).to_be_hidden()
    expect(fallback.locator('.gallery-card')).to_have_count(16)
    expect(fallback.locator('.gallery-card:visible')).to_have_count(16)
    expect(fallback.locator('.phone')).to_be_visible()
    assert fallback.evaluate('document.documentElement.scrollWidth <= innerWidth')
    nojs.close(); context.close(); browser.close()
    print('PASS no-JavaScript contact and gallery fallback. Browser acceptance complete.')
