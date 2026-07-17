# Lowell Herb Co. — Static Website

Built with Astro. 5 pages, zero database, deploys to GitHub Pages.

## Pages

| Route | Content |
|---|---|
| `/` | Homepage — video hero, parallax, features grid, brand story |
| `/catalogue` | Product catalogue — 10 products with images |
| `/store-locator` | Store locator — **placeholder for your bespoke build** |
| `/follow` | Newsletter signup + social links |
| `/404` | Custom 404 page |

## Quick Start

```bash
npm install
npm run dev     # local dev at localhost:4321
npm run build   # production build to dist/
```

## Deploy

The included `.github/workflows/deploy.yml` auto-deploys to GitHub Pages on every push to `main`.

## Remaining Setup

- **Mailchimp:** Fill in your audience IDs in `src/pages/follow.astro` (search for `YOUR_MAILCHIMP`)
- **Store locator:** Drop your bespoke implementation into `src/pages/store-locator.astro`
- **Analytics:** Add your GA4 tracking snippet to `src/layouts/BaseLayout.astro`
- **Custom domain:** Add CNAME record at your DNS provider pointing `www.lowellherbco.com` → `georgelowell.github.io`
