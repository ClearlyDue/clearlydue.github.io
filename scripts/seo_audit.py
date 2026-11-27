"""Weekly search check of https://clearlydue.com. Reads a Lighthouse JSON report and checks the live site.
Prints a Markdown report (used by .github/workflows/seo.yml to open a GitHub issue)."""
import json, re, sys, urllib.request, datetime
SITE = 'https://clearlydue.com/'
def get(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'ClearlyDue-SEO-check/1.0'})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, r.geturl(), r.read().decode('utf-8', 'replace')
    except urllib.error.HTTPError as e:
        return e.code, url, ''
    except Exception as e:
        return 0, url, str(e)
rows, problems = [], []
def check(name, ok, detail=''):
    rows.append(f"| {'✅' if ok else '❌'} | {name} | {detail} |")
    if not ok: problems.append(name)
st, _, html = get(SITE)
check('Home page answers', st == 200, f'HTTP {st}')
head = html[:20000]
t = re.search(r'<title>(.*?)</title>', head, re.S); t = t.group(1).strip() if t else ''
check('Title present (Google shows about 60 characters)', bool(t), f'{len(t)} characters')
d = re.search(r'<meta name="description" content="(.*?)"', head); d = d.group(1) if d else ''
check('Meta description present', 50 <= len(d), f'{len(d)} characters')
check('Indexing allowed', 'noindex' not in head.split('<style>')[0], '')
hl = len(re.findall(r'hreflang="', head)); check('Language alternates (hreflang)', hl >= 2, f'{hl} links')
ld = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
try:
    json.loads(ld[0]); ldok = True
except Exception:
    ldok = False
check('Structured data (JSON-LD) parses', ldok, '')
for path in ['robots.txt', 'sitemap.xml', 'og-image.png', 'icon-512.png', '404.html']:
    s2, _, body = get(SITE + path)
    extra = ''
    if path == 'sitemap.xml': extra = f"{body.count('<loc>')} addresses"
    check(f'/{path} reachable', s2 == 200, extra)
s3, final, body = get('https://clearlydue.es/')
check('clearlydue.es sends visitors to clearlydue.com', s3 == 200 and 'https://clearlydue.com' in body, final)
lh = {}
try:
    lh = json.load(open(sys.argv[1])) if len(sys.argv) > 1 else {}
except Exception as e:
    rows.append(f'| ⚠️ | Lighthouse report missing | {e} |')
scores = {k: round((v.get('score') or 0) * 100) for k, v in lh.get('categories', {}).items()}
fails = [a.get('title', k) for k, a in lh.get('audits', {}).items() if a.get('scoreDisplayMode') == 'binary' and a.get('score') == 0 and k in {r.get('id') for g in lh.get('categories', {}).values() for r in g.get('auditRefs', [])}]
today = datetime.date.today().isoformat()
print(f'# Weekly SEO report, {today}\n')
print('**Lighthouse (mobile):** ' + (' · '.join(f'{k} {v}' for k, v in scores.items()) if scores else 'not available') + '\n')
print('| | Check | Detail |\n|---|---|---|'); print('\n'.join(rows))
if fails:
    print('\n**Lighthouse items to fix:**\n' + '\n'.join(f'- {f}' for f in fails[:25]))
print('\n**Summary:** ' + ('all checks passed.' if not problems else f"{len(problems)} problem(s): " + ', '.join(problems)))
print('\nRankings, clicks and impressions are in Google Search Console and Bing Webmaster Tools once the site is verified there (see README).')
