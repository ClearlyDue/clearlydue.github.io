# clearlydue.com

Public site of ClearlyDue: the design-partner (pilot programme) page, published with GitHub Pages.
`clearlydue.es` and `www.clearlydue.es` send visitors here (repository `ClearlyDue/clearlydue-es`).

## Files
- `index.html` and `i18n/`: the pilot page, built from the browser edition (`node build.js`, folder `dist-web`). English and Spanish are inside the page; each other language (48) is a file in `i18n/` loaded only when chosen, so the page is about 470 KB instead of 2.6 MB. Version 1.4.0, Notion-style design (27 Nov 2026).
- `robots.txt`, `sitemap.xml`: tell search engines what to index. The sitemap lists one address per language (`/?lang=fr` and so on) with `hreflang` alternates.
- `og-image.png`, `icon-512.png`, `apple-touch-icon.png`, `favicon-32.png`: images for link previews and icons.
- `404.html`: page for unknown addresses.
- `<32 hex characters>.txt`: IndexNow key file (proves to search engines that this site sends the notifications).
- `scripts/indexnow.py`, `scripts/seo_audit.py`, `.github/workflows/seo.yml`: search automation (below).

## Search automation (runs on GitHub, free)
- **Every publish** (push to `main`): after two minutes, all page addresses are sent to IndexNow (Bing, Yandex, Seznam, Naver, Yep).
- **Every Monday 07:17 (Barcelona):** Lighthouse runs on the live site and the site is checked (title, description, language alternates, structured data, robots, sitemap, images, 404, the .es redirect). The result is opened as a GitHub issue labelled `seo-report`. Run it any time from Actions → SEO automation → Run workflow.

## Search engine accounts
- Google Search Console (account clearlydue.team@gmail.com): property `https://clearlydue.com/` verified on 27 Nov 2026 with the file `googled157c10a789465ea.html` (do not delete it); `sitemap.xml` submitted the same day (50 addresses found). Google does not use IndexNow.
- Bing Webmaster Tools (optional): import the site from Search Console, so Bing reports clicks and positions too.
