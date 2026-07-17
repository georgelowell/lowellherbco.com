# Lowell Herb Co. — Website Migration Feasibility Study

**Date:** July 16, 2026  
**Current Site:** https://www.lowellherbco.com  
**Author:** Nixon (Hermes)

---

## Executive Summary

Lowell Herb Co.'s website is a **WordPress 7.0.1 brochure site** with ~5 pages (Home, Catalogue, Store Locator, Follow Us, Blog) and a custom theme (`daniel_theme`). It's an ideal candidate for migration to a static site hosted on GitHub Pages — faster, cheaper ($0/mo vs. current hosting), and directly editable via GitHub. The only non-trivial piece is the store locator, which is handled by an embeddable third-party widget (Stockist.co).

**Estimated build time:** 3-5 days for a developer, or I can scaffold it for you.

---

## 1. Current Stack

| Component | Technology | Notes |
|---|---|---|
| **CMS** | WordPress 7.0.1 | Heavily customized |
| **Theme** | `daniel_theme` (custom Underscores child) | ~17KB CSS, Bootstrap 5 |
| **Plugins** | WooCommerce 10.9.4 (unused), Contact Form 7, Mailchimp for WooCommerce, Dispensary Age Verification, WP Store Locator, Google Site Kit, Mailchimp for WP | WooCommerce installed but no active cart/checkout |
| **Ecommerce** | None on-site — "Shop Online" links to `lowellsupply.com/shop` | No need to replicate |
| **Store Locator** | Stockist.co embed (third-party widget) | **Preserves easily** — just keep the embed snippet |
| **Forms** | Contact Form 7 + Mailchimp | Replace with Netlify Forms, Formspree, or direct Mailchimp API |
| **Age Gate** | Dispensary Age Verification plugin | Simple JS cookie overlay — 30 lines of code |
| **Analytics** | Google Site Kit (GA4 + GSC) | Just replace with direct GA4 snippet |

---

## 2. Page Inventory

### 2.1 Homepage
- **Hero:** Full-screen background video (`video-1.mp4`) + dark overlay + centered "Great American Cannabis" headline + social icons
- **Parallax Image 1:** Cannabis leaf close-up (`leaf-paralax-crop.png`)
- **"What Sets Us Apart":** 4-column feature section with leaf icons — Quality First, Always Blended, A Better Smoke, Ready and Able
- **Story Sections** (image-left / text-right alternating):
  - About — grow facility photo
  - Our Inspiration — product packaging photo
  - History — staff photo
  - Natura Arte Aucta — hiking couple in redwoods
  - America's Favorite Pre-Roll — prerolls in wooden bowl
- **Parallax Image 2:** Outdoor grow (`outdoor-grow-parralax_.png`)
- **Footer:** Logo + disclaimer + 3-column (Useful Links, Legal, Follow Us)

### 2.2 Catalogue
- 10 product listings with left-image/right-text layout:
  - Originals, Quicks, 35s, One Gram Pre-Roll, Farmer's Eights, Littles, Bigs, Classic Bubble Hash, Rosin AIO Vape, Rosin Sauce 510 Cart
  - Each has: product image, name, tagline, description
- Currently rendered via AJAX from a WordPress custom post type, but the HTML is fully baked into the page source — can be static

### 2.3 Store Locator
- Stockist.co embed: `<stockist-store-locator data-stockist-widget-tag="u24108"></stockist-store-locator>`
- 100+ retail locations nationwide
- **Migration-friendly:** Just copy the embed snippet to the new site

### 2.4 Follow Us
- Mailchimp + CF7 signup form
- **Migration-friendly:** Replace with direct Mailchimp embedded form

### 2.5 Blog
- **Critical issue:** Infected with spam casino content in Italian (gambling SEO spam)
- 10+ posts, all junk
- **Recommendation:** Wipe completely — start fresh or skip entirely

---

## 3. Design Specifications

### 3.1 Color Palette
```css
--primary-brown: #7B604B;       /* Footer background */
--button-burgundy: #563835;      /* Primary button */
--sage-light: #dde5dc;          /* Mobile nav background */
--sage-dark: #4A5346;           /* Age gate background */
--text-dark: #0C0C0C;
--text-gray: #666666;
--text-muted: #7C7C7C;
--text-charcoal: #4C4C4C;
--white: #ffffff;
--gold-cream: #D1D0C3;          /* Age gate text */
```

### 3.2 Typography (⚠️ Licensed Fonts)
| Font | Usage | Weights |
|---|---|---|
| **El Hidrant Swash** | Script headings | Regular |
| **El Hidrant** | Main headings (85px), section headings (42px) | Regular |
| **Baton Turbo** | Body, buttons, nav | Book, Medium, Bold, Heavy (+ Italics) |

**⚠️ Licensing concern:** These are custom commercial fonts served from the theme's `/font/` directory. If you don't have a license to redistribute them outside the WordPress theme, you'll need alternatives:

| Current Font | Recommended Free Alternative |
|---|---|
| El Hidrant Swash | Playfair Display italic, Cormorant Garamond italic |
| El Hidrant | Playfair Display, Cormorant Garamond |
| Baton Turbo | Inter, DM Sans, Plus Jakarta Sans |

I've downloaded all 36 font files to `assets/fonts/` for your reference.

### 3.3 Key CSS Properties
```
.main-heading { font: 85px/1.2 'El Hidrant'; text-transform: capitalize; }
.common-h2 { font: 42px/1.2 'El Hidrant'; text-transform: capitalize; }
body text: 16px/1.6 'Baton Turbo', weight 400-500
Buttons: 16px/1.6 'Baton Turbo', padding 15px 40px
Herb icon separator: 98px wide, 26px tall, margin-bottom 30px
```

---

## 4. Asset Inventory

All assets have been downloaded to `assets/`:

| Folder | Contents | Count |
|---|---|---|
| `assets/images/` | Logo, hero text, section photos, product images, icons, parallax backgrounds | 23 files |
| `assets/video/` | Hero background video (`video-1.mp4`) | 1 file |
| `assets/fonts/` | El Hidrant Swash, El Hidrant, Baton Turbo (all weights + formats) | 36 files |
| `data/` | (Reserved for store locator export) | — |

---

## 5. Recommended Architecture

### Option A: Astro + GitHub Pages ✅ (Recommended)

**Why:** Static site generator — 5 pages, no database, zero maintenance. Markdown/HTML content means you edit via GitHub directly.

**Structure:**
```
lowellherbco.com/
├── public/
│   ├── assets/images/        (downloaded images)
│   ├── assets/fonts/         (font files)
│   └── assets/video/         (hero.mp4)
├── src/
│   ├── pages/
│   │   ├── index.astro       (Homepage)
│   │   ├── catalogue.astro   (Product catalogue)
│   │   ├── store-locator.astro (Map embed)
│   │   ├── follow.astro      (Signup form)
│   │   └── blog/             (optional MDX blog)
│   ├── components/
│   │   ├── Header.astro      (Nav + hamburger menu)
│   │   ├── Footer.astro      (3-column footer)
│   │   ├── AgeGate.astro     (21+ overlay)
│   │   ├── HeroSection.astro
│   │   ├── FeaturesSection.astro
│   │   ├── StorySection.astro (reusable image+text)
│   │   └── ProductCard.astro
│   └── layouts/
│       └── BaseLayout.astro  (shared head/footer/age-gate)
├── astro.config.mjs
├── package.json
└── README.md
```

**Deployment:** Push to GitHub → GitHub Actions auto-deploys to GitHub Pages. Custom domain via CNAME.

**Cost: $0.** Hosting, SSL, CDN all included.

### Option B: Next.js + Vercel

Better if you plan to add features later (headless CMS, ecommerce, dynamic content). Slightly more complex but Vercel handles deploy + DNS.

**Cost: $0** for your traffic level.

---

## 6. Migration Path

### Phase 1 — Prep (✅ Done)
- [x] Audit current site stack and pages
- [x] Extract all text content (homepage, catalogue, footer)
- [x] Download all images (23 files)
- [x] Download hero video
- [x] Download all font files (36 files)
- [x] Identify store locator embed (Stockist.co)
- [x] Identify form providers (Mailchimp, CF7)
- [ ] Clean blog spam (before migration)
- [ ] Confirm font licensing with theme provider
- [ ] Export Mailchimp list configuration

### Phase 2 — Build (~2-3 days)
- [ ] Scaffold static project (Astro or plain HTML/CSS/JS)
- [ ] Build `BaseLayout` with shared header, footer, age gate
- [ ] Build homepage — hero, features, story sections, parallax
- [ ] Build catalogue page — 10 product listings
- [ ] Build store locator page — Stockist.co embed
- [ ] Build follow/signup page — Mailchimp form
- [ ] Add age verification overlay
- [ ] Responsive design pass
- [ ] Performance optimization (image optimization, lazy loading)

### Phase 3 — Deploy (~2 hours)
- [ ] Create GitHub repository
- [ ] Push build artifacts
- [ ] Configure GitHub Pages (or Vercel)
- [ ] Set up custom domain DNS
- [ ] Add GA4 analytics snippet
- [ ] Test all pages, forms, and links
- [ ] Add 301 redirects from old WordPress URLs

### Phase 4 — Post-Migration
- [ ] Remove WordPress site (or keep as subdomain)
- [ ] Submit new sitemap to Google Search Console
- [ ] Monitor for 404s

---

## 7. Cost Comparison

| Item | Current (WordPress) | Static (GitHub Pages) |
|---|---|---|
| **Hosting** | ~$10-30/mo | **$0** |
| **SSL Certificate** | Included | **Free** (Cloudflare) |
| **CDN** | Plugin-dependent | **Built-in** (Cloudflare/GitHub) |
| **Theme/Font Licenses** | Annual renewal | One-time (or free alternatives) |
| **Security** | Plugin updates + patching | **Zero** (no server-side execution) |
| **Backups** | Plugin + storage | **Git history** |
| **Maintenance** | Monthly plugin updates | **None** |
| **Store Locator** | Stockist.co embed (included) | Same embed (unaffected) |
| **Forms** | CF7 + Mailchimp | Mailchimp embed only |

**Annual savings:** ~$120-360+/yr in hosting alone.

---

## 8. Risks & Mitigations

| Risk | Severity | Mitigation |
|---|---|---|
| **Font licensing** | ⚠️ Medium | Confirm with theme author; have free alternatives ready |
| **Blog spam infecting SEO** | 🚩 High | Wipe all blog posts before migration; 301 redirect /blog |
| **Stockist.co dependency** | Low | Widget URL is stable — embed is portable |
| **Store locator data** | Low | Data lives on Stockist.co platform, not in WordPress |
| **Broken links** | Low | Audit all links before deploying; set up 301s |
| **Age gate legal requirement** | Low | Pure JS/CSS — no server dependency |

---

## 9. Immediate Actions Needed From You

1. **Fonts:** Do you have a license to use El Hidrant and Baton Turbo outside the WordPress theme? If not, I'll use free alternatives (Playfair Display + Inter).
2. **Blog:** Want me to wipe those casino spam posts before we build? I can do that via the WordPress admin.
3. **Store Locator:** The Stockist.co account — do you have the login? The embed tag `u24108` is already in the code, so it should work on any site.
4. **Start building:** Say the word and I'll scaffold the full site here in the workspace.

---

*Generated by Nixon (Hermes Agent) at your request. Assets are ready in `~/workspace/lowell-migration/`.*
