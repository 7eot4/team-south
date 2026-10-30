"""Motion remains optional, settles, and respects changes to reduced-motion preferences."""
import sys
import time
from urllib.parse import urlsplit
from playwright.sync_api import sync_playwright, expect

base = sys.argv[1] if len(sys.argv) > 1 else 'https://127.0.0.1:8182/'
local = urlsplit(base).hostname in ['127.0.0.1', 'localhost']
def until(page, expression):
    deadline = time.monotonic() + 8
    while time.monotonic() < deadline:
        if page.evaluate('() => (' + expression + ')'):
            return
        page.wait_for_timeout(50)
    raise AssertionError(expression)

with sync_playwright() as p:
    for name, launcher, options in [('Edge', p.chromium, {'channel': 'msedge'}), ('Firefox', p.firefox, {}), ('WebKit', p.webkit, {})]:
        browser = launcher.launch(headless=True, **options)
        context = browser.new_context(viewport={'width': 1440, 'height': 900}, ignore_https_errors=local, reduced_motion='no-preference')
        page = context.new_page()
        errors = []
        page.on('pageerror', lambda error: errors.append(str(error)))
        page.goto(base, wait_until='domcontentloaded')
        until(page, "[...document.querySelectorAll('.hero-content > *, .hero-photos')].some(e=>e.getAnimations().length>0)")
        until(page, "[...document.querySelectorAll('.hero-content > *, .hero-photos')].every(e=>e.getAnimations().length===0)")
        assert page.locator('h1').evaluate('(e)=>getComputedStyle(e).opacity') == '1'
        page.locator('.gallery-link').first.hover()
        until(page, "Number(getComputedStyle(document.querySelector('.gallery-link img')).transform.split('(')[1]?.split(',')[0]) > 1")
        page.locator('[data-filter="rekreacja"]').click()
        expect(page.locator('.gallery-card:visible')).to_have_count(4)
        until(page, 'activeMotions.size > 0')
        page.emulate_media(reduced_motion='reduce')
        until(page, 'activeMotions.size === 0')
        until(page, 'document.getAnimations().length === 0')
        page.locator('.gallery-link:visible').first.click()
        expect(page.locator('#lightbox-feedback')).to_be_hidden()
        assert page.locator('#lightbox').evaluate('(e)=>getComputedStyle(e).animationName') == 'none'
        page.keyboard.press('Escape')
        assert page.locator('.gallery-card:visible').first.evaluate('(e)=>getComputedStyle(e).opacity') == '1'
        context.close()

        reduced = browser.new_context(viewport={'width': 390, 'height': 844}, ignore_https_errors=local, reduced_motion='reduce')
        page = reduced.new_page()
        page.on('pageerror', lambda error: errors.append(str(error)))
        page.goto(base, wait_until='networkidle')
        assert page.evaluate('document.getAnimations().length') == 0
        assert page.evaluate('getComputedStyle(document.documentElement).scrollBehavior') == 'auto'
        page.locator('.menu').click()
        expect(page.locator('#navigation')).to_be_visible()
        assert page.locator('#navigation').evaluate('(e)=>e.getAnimations().length') == 0
        page.keyboard.press('Escape')
        page.locator('#inquiry-service').select_option('bruk')
        page.locator('#form-next').click()
        expect(page.locator('[data-step="1"]')).to_be_visible()
        assert page.locator('[data-step="1"]').evaluate('(e)=>e.getAnimations().length') == 0
        assert not errors, errors
        reduced.close(); browser.close()
        print(f'PASS {name}: entrance and hover motion, filter animation, live cancellation, reduced-motion menu/form/modal, visible final content.')
