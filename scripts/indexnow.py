"""Tell IndexNow search engines (Bing, Yandex, Seznam, Naver, Yep) that the pages in sitemap.xml changed.
Runs in GitHub Actions after each publish. Google does not use IndexNow; it reads sitemap.xml (see README)."""
import glob, json, os, re, sys, urllib.request
here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
keys = [os.path.basename(p)[:-4] for p in glob.glob(os.path.join(here, '*.txt')) if re.fullmatch(r'[0-9a-f]{32}', os.path.basename(p)[:-4])]
if not keys:
    sys.exit('no IndexNow key file found')
urls = re.findall(r'<loc>(.*?)</loc>', open(os.path.join(here, 'sitemap.xml'), encoding='utf-8').read())
urls = [u.replace('&amp;', '&') for u in urls]
body = json.dumps({'host': 'clearlydue.com', 'key': keys[0], 'keyLocation': f'https://clearlydue.com/{keys[0]}.txt', 'urlList': urls}).encode()
req = urllib.request.Request('https://api.indexnow.org/indexnow', data=body, headers={'Content-Type': 'application/json; charset=utf-8'})
try:
    with urllib.request.urlopen(req, timeout=30) as r:
        print('IndexNow answered', r.status, 'for', len(urls), 'addresses')
except urllib.error.HTTPError as e:
    print('IndexNow answered', e.code, e.read()[:300])
    sys.exit(0 if e.code in (200, 202) else 1)
