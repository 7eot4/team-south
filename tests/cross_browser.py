"""Three-engine functional and responsive smoke tests, without private browser profiles."""
from pathlib import Path
import json,sys,re
from urllib.parse import urlsplit
from playwright.sync_api import sync_playwright,expect

BASE=sys.argv[1] if len(sys.argv)>1 else 'https://127.0.0.1:8182/'
OUT=Path(__file__).resolve().parents[1]/'.local/security';OUT.mkdir(parents=True,exist_ok=True)
sizes=[(320,568),(360,640),(375,667),(390,844),(412,915),(540,720),(568,320),(667,375),(768,1024),(800,600),(801,600),(820,1180),(844,390),(950,700),(1024,768),(1280,720),(1440,900),(1920,1080),(2560,1440)]
results=[]
with sync_playwright() as p:
    for name,launcher,options in [('Edge',p.chromium,{'channel':'msedge'}),('Firefox',p.firefox,{}),('WebKit',p.webkit,{})]:
        browser=launcher.launch(headless=True,**options)
        context=browser.new_context(viewport={'width':1440,'height':900},locale='pl-PL',ignore_https_errors=urlsplit(BASE).hostname in ['127.0.0.1','localhost'])
        page=context.new_page();errors=[];violations=[]
        page.on('pageerror',lambda error:errors.append(str(error)))
        page.add_init_script("window.auditCsp=[];document.addEventListener('securitypolicyviolation',e=>auditCsp.push({directive:e.effectiveDirective,source:e.sourceFile,blocked:e.blockedURI}))")
        page.goto(BASE,wait_until='networkidle')
        assert 'no-js' not in (page.locator('html').get_attribute('class') or ''),name
        for width,height in sizes:
            page.set_viewport_size({'width':width,'height':height})
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'),(name,width,height)
            header=page.locator('.site-header').bounding_box()
            assert header['height']<=105,(name,width,header)
            if width<=800:
                menu=page.locator('.menu').bounding_box()
                for icon in page.locator('.header-socials .social-button').all():
                    box=icon.bounding_box();assert box['x']>=0 and box['x']+box['width']<=menu['x']+1,(name,width,box,menu)
                page.locator('.menu').click();expect(page.locator('.menu')).to_have_attribute('aria-expanded','true')
                page.keyboard.press('Escape');expect(page.locator('.menu')).to_have_attribute('aria-expanded','false')
        page.set_viewport_size({'width':390,'height':844})
        page.locator('[data-service="bruk"]').click();expect(page.locator('#service-title')).to_have_text('Podjazdy, chodniki i nawierzchnie')
        page.locator('.choose-service').click();expect(page.locator('#inquiry-service')).to_have_value('bruk')
        page.locator('#form-next').click();page.locator('#location').fill('Niedźwiedź');page.locator('#description').fill('<svg onload="window.__xss=1">Opis testowy</svg>');page.locator('#form-next').click()
        expect(page.locator('[data-step="2"]')).to_be_visible();assert page.evaluate('window.__xss||0')==0
        assert page.locator('#inquiry-summary svg').count()==0
        assert page.locator('legend:visible').bounding_box()['y']>=page.locator('.site-header').bounding_box()['height']-1
        page.locator('#form-reset').click()
        page.locator('[data-filter="rekreacja"]').click();expect(page.locator('.gallery-card:visible')).to_have_count(4)
        for width,height in [(390,844),(667,375),(1440,900)]:
            page.set_viewport_size({'width':width,'height':height});page.locator('.gallery-card:visible .gallery-link').first.click()
            expect(page.locator('#lightbox')).to_be_visible();expect(page.locator('#lightbox-feedback')).to_be_hidden()
            box=page.locator('#lightbox').bounding_box();assert box['x']>=0 and box['y']>=0 and box['height']<=height,(name,box,width,height)
            page.keyboard.press('ArrowRight');page.keyboard.press('Escape');expect(page.locator('#lightbox')).to_be_hidden()
            expect(page.locator('body')).not_to_have_class(re.compile(r'\bmodal-open\b'))
        page.locator('.header-socials [data-social="Instagram"]').click();expect(page.locator('#social-dialog')).to_be_visible();page.keyboard.press('Escape')
        page.locator('.faq-list summary').first.click();expect(page.locator('.faq-list details').first).to_have_attribute('open','')
        assert not errors,(name,errors)
        csp_events=page.evaluate('auditCsp')
        known_engine_warnings=0
        if name=='WebKit' and csp_events:
            # Reproduced on a minimal select-only document; do not weaken application CSP.
            # https://github.com/microsoft/playwright/issues/43497 (WebKit 27.2 regression).
            assert len(csp_events)==page.locator('select').count(),csp_events
            assert all(e=={'directive':'style-src-attr','source':'','blocked':'inline'} for e in csp_events),csp_events
            assert page.locator('[style]').count()==0
            known_engine_warnings=len(csp_events)
        else:
            assert csp_events==[],(name,csp_events)
        page.set_viewport_size({'width':390,'height':844});page.evaluate("scrollTo({top:0,behavior:'instant'})");page.screenshot(path=str(OUT/f'{name.lower()}-mobile.png'))
        results.append({'engine':name,'version':browser.version,'layouts':len(sizes),'result':'PASS','page_errors':0,'unexpected_csp_violations':0,'known_webkit_select_warnings':known_engine_warnings})
        context.close();browser.close()
        print(f'PASS {name}: {len(sizes)} layouts, short landscape, header, service/form, safe text, gallery/modal, social and FAQ.')
(OUT/'cross-browser.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
