# clearlydue.com

Public site of ClearlyDue: the design-partner (pilot programme) page, published with GitHub Pages.
`clearlydue.es` and `www.clearlydue.es` send visitors here (repository `ClearlyDue/clearlydue-es`).

## Files
- `index.html`: the pilot page, built from the browser edition (`node build.js`, folder `dist-partners`). Self-contained, in 50 languages. Version 1.4.0, Notion-style design (27 Nov 2026).
- `robots.txt`, `sitemap.xml`: tell search engines what to index. The sitemap lists one address per language (`/?lang=fr` and so on) with `hreflang` alternates.
- `og-image.png`, `icon-512.png`, `apple-touch-icon.png`, `favicon-32.png`: images for link previews and icons.
- `404.html`: page for unknown addresses.
- `<32 hex characters>.txt`: IndexNow key file (proves to search engines that this site sends the notifications).
- `scripts/indexnow.py`, `scripts/seo_audit.py`, `.github/workflows/seo.yml`: search automation (below).

## Search automation (runs on GitHub, free)
- **Every publish** (push to `main`): after two minutes, all page addresses are sent to IndexNow (Bing, Yandex, Seznam, Naver, Yep).
- **Every Monday 07:17 (Barcelona):** Lighthouse runs on the live site and the site is checked (title, description, language alternates, structured data, robots, sitemap, images, 404, the .es redirect). The result is opened as a GitHub issue labelled `seo-report`. Run it any time from Actions → SEO automation → Run workflow.

## One-time steps that need the owner's own accounts
- Google Search Console: add `clearlydue.com` (Domain property, DNS TXT record at DonDominio), then submit `https://clearlydue.com/sitemap.xml`. Google does not use IndexNow.
- Bing Webmaster Tools: import the site from Search Console (one click), so Bing reports clicks and positions too.
