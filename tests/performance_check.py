"""Repeatable Chromium lab measurements; these are not real-user Core Web Vitals."""
from pathlib import Path
import json,sys,statistics
from playwright.sync_api import sync_playwright

BASE=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8181/'
OUT=Path(__file__).resolve().parents[1]/'.local/security';OUT.mkdir(parents=True,exist_ok=True)
init='''window.auditPerf={cls:0,lcp:0,longTasks:[]};new PerformanceObserver(l=>{for(const e of l.getEntries())if(!e.hadRecentInput)window.auditPerf.cls+=e.value}).observe({type:'layout-shift',buffered:true});new PerformanceObserver(l=>{for(const e of l.getEntries())window.auditPerf.lcp=e.startTime}).observe({type:'largest-contentful-paint',buffered:true});new PerformanceObserver(l=>{for(const e of l.getEntries())window.auditPerf.longTasks.push(e.duration)}).observe({type:'longtask',buffered:true});'''
results=[]
with sync_playwright() as p:
    browser=p.chromium.launch(channel='msedge',headless=True)
    for profile,slow in [('mobile-normal',False),('mobile-slow4g-cpu4x',True)]:
        for repeat in range(3):
            context=browser.new_context(viewport={'width':390,'height':844},device_scale_factor=1)
            page=context.new_page();page.add_init_script(init)
            cdp=context.new_cdp_session(page);cdp.send('Network.enable');cdp.send('Network.setCacheDisabled',{'cacheDisabled':True})
            if slow:
                cdp.send('Network.emulateNetworkConditions',{'offline':False,'latency':150,'downloadThroughput':200000,'uploadThroughput':93750})
                cdp.send('Emulation.setCPUThrottlingRate',{'rate':4})
            page.goto(BASE,wait_until='networkidle',timeout=60000)
            result=page.evaluate('''({cls:auditPerf.cls,lcp_ms:auditPerf.lcp,longTasks:auditPerf.longTasks,resources:performance.getEntriesByType('resource').map(r=>({url:r.name,bytes:r.transferSize,duration:r.duration})),dom_ms:performance.getEntriesByType('navigation')[0].domContentLoadedEventEnd})''')
            result.update({'profile':profile,'repeat':repeat+1,'transfer_bytes':sum(r['bytes'] for r in result['resources']),'requests':len(result['resources'])})
            assert result['cls']<=.1,(profile,'layout shifts',result['cls'])
            assert result['transfer_bytes']<650000,(profile,'excess initial payload',result['transfer_bytes'])
            assert max(result['longTasks'],default=0)<300,(profile,'long blocking task',result['longTasks'])
            assert result['lcp_ms']<5000,(profile,'slow LCP',result['lcp_ms'])
            results.append(result);context.close()
        group=[r for r in results if r['profile']==profile]
        assert statistics.median(r['lcp_ms'] for r in group)<2500,(profile,'median LCP outside good lab target')
        print(profile, json.dumps({'median_lcp_ms':statistics.median(r['lcp_ms'] for r in group),'max_cls':max(r['cls'] for r in group),'median_transfer_bytes':statistics.median(r['transfer_bytes'] for r in group),'max_long_task_ms':max((t for r in group for t in r['longTasks']),default=0)}))
    browser.close()
(OUT/'performance-after.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
print('PASS performance lab budgets: CLS <= 0.1, initial resources < 650 kB, no >300 ms tasks and LCP < 5 s under stated profiles.')
