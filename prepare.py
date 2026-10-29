from pathlib import Path
import urllib.request,json
from html.parser import HTMLParser
root=Path(__file__).parent
(root/'dist/assets').mkdir(parents=True,exist_ok=True)
class Assets(HTMLParser):
 def handle_starttag(self,t,a):
  d=dict(a)
  if 'data-ww_rwd' not in d:return
  u=json.loads(d['data-ww_rwd']).get('data-lazy-load-src',{}).get('rwdMode_1','')
  names={'element_697_image':'logo.png','element_442_image':'earthworks.jpg','element_703_image':'paving.jpg','element_326_image':'hero.jpg'}
  if d.get('id') in names:
   name=names[d['id']]; urllib.request.urlretrieve('https://teamsouth.pl/'+u,root/'dist/assets'/name)
   print(name,u)
Assets().feed(urllib.request.urlopen('https://teamsouth.pl').read().decode())
