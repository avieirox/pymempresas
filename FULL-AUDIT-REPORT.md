# Full SEO Audit Report — pymempresas.com

**Date:** 2026-05-15
**Site:** https://pymempresas.com/
**Stack:** Astro 5.14 + Tailwind CSS 4.1 + LiteSpeed
**Business:** Agencia de Marketing Digital — SEO Local, Diseño Web, IA para PYMES (Gijón, Asturias)
**Audit scope:** 22 pages, 8 specialist subagents, live GSC data (Feb–May 2026)

---

## Executive Summary

### Overall SEO Health Score: 57 / 100

| Category | Weight | Score | Weighted |
|----------|--------|-------|----------|
| Technical SEO | 22% | 78 | 17.2 |
| Content Quality | 23% | 52 | 12.0 |
| On-Page SEO | 20% | 55 | 11.0 |
| Schema / Structured Data | 10% | 42 | 4.2 |
| Performance (CWV) | 10% | 50 | 5.0 |
| AI Search Readiness | 10% | 64 | 6.4 |
| Images | 5% | 35 | 1.8 |
| **TOTAL** | **100%** | — | **57.5** |

### GSC Reality Check

| Metric | Value |
|--------|-------|
| Total clicks (4 months) | **7** |
| Total impressions | 12,509 |
| Overall CTR | 0.06% |
| Avg position | ~65 |
| Indexed pages | 11 (of ~17 indexable) |
| Rich results | 0 |
| Enhanced features | 0 |
| Mobile share | 29% of impressions |
| Only market | Spain (98% of traffic) |

**The site is virtually invisible in Google.** With 12.5K impressions and only 7 clicks, it ranks on page 5–10 for most queries. Rich results are completely absent. The site has strong technical foundations (SSG, fast server, good compression) but critical failures in content depth, schema markup, and performance are suppressing rankings.

### Top 5 Critical Issues

1. **Cookie banner full-screen overlay blocks all first-visit interaction** — every organic visitor hits a consent wall before they can click any CTA, navigate, or scroll effectively.
2. **Schema @id references fragmented beyond resolution** — 4 different ID patterns across pages (`#website`, `#business`, `#organization`, `#localbusiness`), with `#organization` never defined anywhere. Google cannot resolve the business entity.
3. **~60% duplicate content between /seo-local-gijon/ and /seo-local-oviedo/** — benefits, expert tasks, FAQ, and pricing are near-identical. Google's helpful content system will devalue both pages.
4. **No team credentials, about page, or verifiable expertise** — zero author attribution on service pages, no certifications, no case studies with real data. E-E-A-T score: 40.75/100.
5. **2.1MB author PNG loaded twice per blog page** — `arturo-vieiros-foto.png` is a raw PNG used at 28px and 64px display sizes. Single largest performance drain.

### Top 5 Quick Wins (fix this week)

1. Convert `arturo-vieiros-foto.png` to WebP 128×128px (~10KB) — fixes LCP on all blog pages
2. Add security headers (HSTS, X-Content-Type-Options, X-Frame-Options) via `.htaccess`
3. Add `/seo-gijon/` to sitemap generation
4. Create `og-default.jpg` 1200×630px and update `SEO.astro`
5. Restrict Inter font to Latin-only woff2 (42 declarations → 3) — saves ~6KB inline CSS + 1.3MB font files

---

## Technical SEO — Score: 78/100

### Crawlability

| Check | Status |
|-------|--------|
| robots.txt | Clean — `Allow: /`, sitemap referenced, only `/cdn-cgi/` blocked |
| Sitemap XML | Valid, 18 URLs, proper namespace |
| Sitemap in robots.txt | Present |
| Custom 404 | **FAIL** — LiteSpeed default served, `dist/404.html` not configured |
| `/seo-gijon/` in sitemap | **FAIL** — not included (standalone `.astro`, not in any collection) |
| Case-insensitive URLs | **FAIL** — `/BLOG/` returns LiteSpeed 404 |

### Indexability

| Check | Status |
|-------|--------|
| Canonical tags | Self-referencing on all pages (BaseLayout) |
| Meta robots | `index, follow` on all indexable pages |
| Legal pages noindex | Correct — `aviso-legal`, `politica-privacidad` set to `noindex` |
| H1 tags | Exactly 1 per page |
| Orphan pages | None — all pages linked from nav or footer |
| Indexed vs sitemap gap | 11 indexed vs 18 in sitemap (7 missing — new pages, crawling delay) |

### URL Structure

| Check | Status |
|-------|--------|
| Clean URLs | Hyphen-separated, no query strings, no extensions |
| Trailing slash | 301 redirect for missing trailing slash |
| www → non-www | 301 redirect |
| HTTP → HTTPS | 301 redirect |
| Redirect chains | None detected (all single-hop) |

### Security — Score: 35/100

**All 6 security headers are missing:**

| Header | Status |
|--------|--------|
| `Strict-Transport-Security` | Missing |
| `X-Content-Type-Options` | Missing |
| `X-Frame-Options` | Missing |
| `Content-Security-Policy` | Missing |
| `Referrer-Policy` | Missing |
| `Permissions-Policy` | Missing |

**Fix:** Add via Cloudflare Dashboard → Security → Headers, or via `.htaccess`:
```
Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains; preload"
Header always set X-Content-Type-Options "nosniff"
Header always set X-Frame-Options "SAMEORIGIN"
Header always set Referrer-Policy "strict-origin-when-cross-origin"
```

### Server Configuration

| Setting | Value | Verdict |
|---------|-------|---------|
| TTFB | ~97ms | Excellent |
| Compression | Brotli (81%: 104KB → 19KB) | Excellent |
| HTTP/3 | Supported (h3 alt-svc) | Excellent |
| Cache (HTML) | `max-age=3600, must-revalidate` | Good (could be longer for static) |
| Cache (assets) | `max-age=31536000` | Excellent |
| Content-Type charset | Missing `charset=utf-8` | Minor — declared in HTML `<meta>` |

---

## Content Quality — Score: 52/100

### E-E-A-T Assessment: 40.75/100

| Factor | Score | Key Gaps |
|--------|-------|----------|
| Experience | 35/100 | Zero verifiable case studies, generic stats, "150+ proyectos" unsubstantiated |
| Expertise | 45/100 | No certifications, no named team members, no industry affiliations |
| Authoritativeness | 30/100 | No backlinks, no LinkedIn company page, no citations |
| Trustworthiness | 50/100 | Address is coworking space, no legal entity details, no reviews |

### Page-by-Page Content Scores

| Page | Score | Words | Key Issues |
|------|-------|-------|------------|
| Homepage `/` | 45/100 | ~300 substantive | Thin, no social proof, `#portfolio` link broken |
| `/seo-local-gijon/` | 65/100 | ~1,500 | Best page, but ~60% duplicated on Oviedo |
| `/seo-local-oviedo/` | 55/100 | ~1,500 | Heavy duplication, schema bug (wrong city) |
| `/posicionamiento-web-asturias/` | 60/100 | ~2,000 | Deepest content, worst CTR (0.02%) — title/meta not compelling |
| `/diseno-web-gijon/` | 58/100 | ~1,200 | Only page with case studies (unverified) |
| `/inteligencia-artificial-empresas/` | 50/100 | ~1,000 | Generic content, wrong brand color (#ff6b35) |
| `/formacion-ia-empresas/` | 48/100 | ~1,200 | Thin for topic |
| `/automatizaciones-con-ia/` | 45/100 | ~900 | Missing FAQ, no images |
| `/google-negocios/` | 50/100 | ~1,200 | Avilés marked "Próximamente" |
| `/seo-gijon/` | 58/100 | ~5,500 | Longest page but potential overlap with seo-local-gijon |
| Blog posts (6) | 70/100 avg | 1,500–2,500 | Best content — good author E-E-A-T, well-structured |

### Critical Content Issues

**C1. Duplicate Content — Gijón vs Oviedo (~60% overlap)**
- Expert Tasks: 9 of 10 cards are word-for-word identical
- Benefits: same 4 cards with same statistics
- Pricing: identical plans, prices, features
- FAQ: 5 of 7 questions have near-identical answers
- **Risk:** Google's helpful content system (merged into core, Sept 2025) may devalue or deindex both pages.

**C2. No Team/About Page**
- Claims "10+ years experience" and "150+ projects" — zero verifiable evidence
- No team photos, no LinkedIn for individuals on service pages
- No certifications, no Google Partner badge, no industry memberships
- Business address is Spaces Coworking (OK, but no office photos or proof of operations)

**C3. No Verifiable Testimonials or Case Studies**
- 3 testimonials on `/consultoria/` — "María González", "Carlos Fernández", "Laura Martínez" — no last names verifiable, no business names, no links
- "95% Clientes satisfechos" stat has no source, no date, no methodology
- Invented case study names on `/diseno-web-gijon/` ("Restaurante El Asturiano", "Clínica Dental Gijón", "Inmobiliaria Costa Verde")
- **Action:** Collect real testimonials with permission to publish names and companies. Link to actual Google reviews.

### High-Severity Content Issues

**H1. Homepage Thin Content (~300 words substantive)**
- Hero: ~70 words, services: ~180 words, about: ~120 words, advantages: ~90 words, CTA: ~40 words
- Reads as a gateway/index page, not a landing page that can rank
- **Action:** Expand About section with company history and methodology. Target 800+ words.

**H2. Title Tags Missing Locations**
- Homepage: "Agencia de Posicionamiento WEB SEO Local | PYMEMPRESAS" — no location
- IA page: "Inteligencia Artificial para Empresas | PYMEMPRESAS" — no location
- Blog: "Blog — PYMEMPRESAS" — too generic
- **Action:** Add "en Gijón / Asturias" to homepage and IA titles.

**H3. Broken `#portfolio` Links**
- Appears on homepage CTA and service page CTAs
- No `#portfolio` anchor exists on any page
- Dead link on every service page → bad UX

### Medium-Severity Content Issues

| Issue | Details |
|-------|---------|
| Only 6 blog posts for an SEO agency | Insufficient topical authority |
| Inconsistent pricing names | "Básico" vs "Esencial" across pages |
| No content on /aviso-legal/ and /politica-privacidad/ | Thin legal pages hurt trust |
| Inconsistent title separator | Some use `\|`, some use `—` |

---

## On-Page SEO — Score: 55/100

### Title Tags

| Page | Current Title | Issue |
|------|--------------|-------|
| Homepage | Agencia de Posicionamiento WEB SEO Local \| PYMEMPRESAS | Missing location |
| /inteligencia-artificial-empresas/ | Inteligencia Artificial para Empresas \| PYMEMPRESAS | Missing location |
| /blog/ | Blog — PYMEMPRESAS | Generic |
| /seo-local-gijon/ | SEO Local Gijon — Posiciona tu Negocio \| PYMEMPRESAS | Good |
| /seo-local-oviedo/ | SEO Local Oviedo — Posiciona tu Negocio \| PYMEMPRESAS | Good |
| /posicionamiento-web-asturias/ | Posicionamiento Web en Asturias \| SEO + IA \| PYMEMPRESAS | Good |

### Meta Descriptions

Most meta descriptions are present and serviceable. The homepage description is good:
> "Agencia SEO Local en Asturias con más de 10 años de experiencia. Posicionamos tu negocio en Google. Consultoría gratuita sin compromiso."

Recommend reviewing `/formacion-ia-empresas/` and `/automatizaciones-con-ia/` descriptions for CTA strength.

### Heading Structure

All pages have exactly 1 H1. H2/H3 hierarchy is logical on service pages. Blog posts use proper heading nesting.

### Internal Linking

**Issue: Most internal links between service pages appear only in small-print footer paragraphs.** Example from `/seo-local-gijon/`:
```html
<p style="color:#666;font-size:14px;margin:24px auto 0;max-width:800px;text-align:center;">
  ¿Buscas un <a href="/seo-gijon/">consultor SEO en Gijón</a>? ...
</p>
```

This gray, 14px footer text carries minimal link equity. Blog posts do better with natural interlinking.

**Action:** Weave anchor-text links into main body content. INTERLINKING.md already has the right strategy — implement it consistently.

### Open Graph

| Element | Status |
|---------|--------|
| `og:title` | Present on all pages |
| `og:description` | Present on all pages |
| `og:image` | `/og-default.svg` — **SVG format unsupported by most platforms** |
| `og:type` | `website` (home) / `article` (blog) |
| `twitter:card` | `summary_large_image` |

---

## Schema / Structured Data — Score: 42/100

### Global Issues

**F1. @id Reference Fragmentation (CRITICAL)**

Four different ID patterns exist across pages, and the most-referenced one is never defined:

| @id Pattern | Used Where | Entity Defined? |
|-------------|-----------|-----------------|
| `#website` | All pages (BaseLayout) | YES — WebSite |
| `#business` | Homepage, blog posts, diseno-web | YES — only on homepage |
| `#organization` | All service pages (`provider` ref), formacion-ia | **NO — never defined anywhere** |
| `#localbusiness` | seo-local-*, seo-gijon, posicionamiento-web, formacion-ia | YES — but incomplete on each page |

**Every service page has a Service → provider → `@id: "#organization"` that resolves to nothing.** Google cannot connect any Service to its provider entity.

**F2. Incomplete LocalBusiness on 7 of 11 Pages**

Pages defining LocalBusiness are missing: `streetAddress`, `telephone`, `email`, `image`/`logo`, `geo` coordinates. Only the homepage has a complete address.

**F3. Wrong Address on Oviedo Page**

`/seo-local-oviedo/` schema sets `addressLocality: "Oviedo"`. The physical business is in Gijón. Use `areaServed` for Oviedo, not `addressLocality`.

### Page-Specific Issues

| Page | Missing Schema Types | Other Issues |
|------|---------------------|--------------|
| `/automatizaciones-con-ia/` | WebPage, FAQPage, serviceType, image | Most incomplete schema on site |
| `/consultoria/` | WebPage, BreadcrumbList | Minimal Service only |
| `/contacto/` | mainEntity pointing to LocalBusiness | ContactPage is orphaned |
| `/diseno-web-gijon/` | WebPage, BreadcrumbList | Has FAQ but no page-level schema |
| `/inteligencia-artificial-empresas/` | — | Relative image URLs (`/images/…` should be absolute) |
| `/formacion-ia-empresas/` | — | Has BOTH Organization and LocalBusiness (duplicate). lat/lng are strings not numbers |
| `/google-negocios/` | LocalBusiness | Service has no provider reference |
| Blog listing `/blog/` | — | BlogPosting items lack @id refs matching individual posts |
| Blog posts `/[slug]/` | — | 4 of 6 blog images return 404 |

### Recommended Centralized Schema

Add a complete `LocalBusiness` to `BaseLayout.astro` so all pages can reference it:

```json
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "@id": "https://pymempresas.com/#business",
  "name": "PYMEMPRESAS",
  "url": "https://pymempresas.com",
  "logo": "https://pymempresas.com/images/logo-header.webp",
  "telephone": "+34 697 71 13 44",
  "email": "info@pymempresas.com",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "C. Rodríguez San Pedro, 1, Centro",
    "addressLocality": "Gijón",
    "addressRegion": "Asturias",
    "postalCode": "33206",
    "addressCountry": "ES"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": 43.54124,
    "longitude": -5.66205
  },
  "openingHoursSpecification": {
    "@type": "OpeningHoursSpecification",
    "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
    "opens": "09:00",
    "closes": "18:00"
  },
  "areaServed": [
    { "@type": "City", "name": "Gijón" },
    { "@type": "City", "name": "Oviedo" },
    { "@type": "City", "name": "Avilés" },
    { "@type": "State", "name": "Asturias" }
  ],
  "priceRange": "€€€"
}
```

Then all service pages reference `"provider": { "@id": "https://pymempresas.com/#business" }`.

---

## Performance — Score: 50/100

### Core Web Vitals (Estimated)

| Metric | Desktop | Mobile | Target | Verdict |
|--------|---------|--------|--------|---------|
| LCP | ~1.5–2.0s | **~3.0–5.0s** | ≤2.5s | Mobile failing |
| CLS | ~0.05 | ~0.05–0.10 | ≤0.1 | Good |
| INP | ~50ms | ~50–150ms | ≤200ms | Good |
| TBT | ~0ms | ~0–100ms | ≤200ms | Good |
| TTFB | ~97ms | ~100ms | ≤800ms | Excellent |

**Mobile LCP is the barrier.** On slow 3G, LCP likely 3.0–5.0s. This aligns with poor mobile CTR (0.08%) despite 29% mobile impressions.

### Page Weight

| Page | Uncompressed | Compressed | Main Problem |
|------|-------------|------------|--------------|
| Homepage | 104KB | 19KB | 97KB inline CSS |
| Blog post | 160KB + 4.8MB images | ~21KB HTML | 2.1MB author PNG (×2) |
| Service pages | 107–118KB | ~19–21KB | Acceptable |

### Critical Performance Issues

**P0. Author Photo — 2.1MB PNG on Every Blog Page**

`arturo-vieiros-foto.png` is 2,165KB, used at 28px and 64px display sizes. Blog pages load this twice (ArticleHero + AuthorCard). That's 4.2MB of image for a 64px thumbnail.

**Fix:** Convert to WebP 256×256px. Target size: ~10KB. Add `width`/`height` attributes. Add `loading="lazy"`.

**P1. Font Bloat — 42 @font-face Declarations**

@fontsource/inter imports all 6 weights × 7 subsets × 2 formats = 84 font files. Only 3 files are actually needed (Inter Latin 400, 600, 700 woff2).

**Fix:** Replace the 5 `@import` lines in `global.css` with 3 explicit `@font-face` rules for Latin-only woff2. This reduces inline CSS by ~6KB, eliminates 81 unused font files from dist (~1.3MB), and speeds up font discovery.

**P2. No Resource Preloading**

No `<link rel="preload">` for hero image or critical fonts. The browser must parse 97KB of inline CSS before discovering `@font-face` URLs, delaying the first paint.

**Fix:** Add in `BaseLayout.astro`:
```html
<link rel="preload" href="/images/hero-bg-DF654TP8.webp" as="image" fetchpriority="high">
<link rel="preconnect" href="https://www.googletagmanager.com" crossorigin>
```

### CSS Analysis

| Metric | Value |
|--------|-------|
| Inline CSS size | ~97KB (main) + ~8KB (page-specific) |
| External CSS files | 0 (all inlined) |
| Render-blocking CSS | 0 (no external CSS files) |
| Tailwind tree-shaking | Unknown — 97KB suggests incomplete purging |
| @font-face overhead | ~8KB of 97KB (~8% wasted on unused fonts) |

---

## Images — Score: 35/100

### Critical Issues

| Issue | Severity | Details |
|-------|----------|---------|
| Author photo PNG | **P0** | 2.1MB PNG used at 28/64px — convert to 256px WebP (~10KB) |
| 4 blog images 404 | **HIGH** | `precio-SEO-asturias.webp`, `google-my-business-guia-pymempresas-asturias.webp`, `posicionamiento web gijon.webp` (spaces in filename), `seo-local-asturias.webp` |
| OG image SVG only | **HIGH** | `og-default.svg` unsupported by Facebook/Twitter/LinkedIn/WhatsApp |
| Blog images no width/height | **MEDIUM** | ArticleHero, ArticleCard, FeaturedCard, AuthorCard all lack dimensions → CLS on blog |
| WebP adoption | **GOOD** | Most images are WebP with explicit dimensions |
| Hero image | **GOOD** | `fetchpriority="high"` + `loading="eager"` + explicit dimensions |

---

## AI Search Readiness (GEO) — Score: 64/100

### Strengths

- All AI crawlers allowed (GPTBot, ClaudeBot, PerplexityBot, Google-Extended)
- llms.txt present and well-formed (lists services, contact info)
- FAQ sections with self-contained Q&A on most service pages
- Blog posts with author attribution (name, photo, bio, LinkedIn, Twitter)
- Statistics present on service pages (46% local intent, 78% mobile-to-visit, etc.)

### Critical Gaps

**G1. No Author Attribution on Service Pages**
Blog posts model good author E-E-A-T (Arturo Vieiros García, photo, bio, LinkedIn, Twitter). Service pages have ZERO author attribution. AI models prioritize content with identifiable expertise signals.

**G2. No Original Research or Proprietary Data**
All statistics are industry-average data (46%, 78%, 75%) without source attribution. No original surveys, case studies with hard numbers, or unique methodology. AI models cite unique data — repackaged common knowledge is not citable.

**G3. FAQPage Schema Missing Despite FAQ Content**
Pages have FAQ sections visible to users but no `FAQPage` JSON-LD. FAQ content without schema is invisible to structured data parsers and AI models. Already flagged in schema audit.

**G4. No YouTube Channel**
YouTube mentions have the strongest correlation (~0.737) with AI citations in GEO research. Zero YouTube content.
**Action:** Create channel with 5–10 "SEO tips for Asturias businesses" videos.

### Platform-Specific Scores

| Platform | Score | Key Issue |
|----------|-------|-----------|
| Google AI Overviews | 42/100 | No rich results, no FAQPage schema, no author on services |
| ChatGPT Search | 55/100 | llms.txt helps, but no unique data to cite |
| Perplexity | 48/100 | Unsourced statistics, no external references |
| Bing Copilot | 52/100 | llms.txt helps, no Microsoft-specific verification |

---

## Local SEO — Score: 48/100

### Google Business Profile

GBP listing exists and is verified. However:
- No Google Maps embed on ANY page
- No reviews embedded on site
- No `aggregateRating` schema
- No directions link ("Cómo llegar")
- GBP share link `sameAs` is deprecated Google Posts URL

### NAP Consistency

| Source | Name | Address | Phone |
|--------|------|---------|-------|
| Footer | PYMEMPRESAS | Spaces Coworking, C. Rodríguez San Pedro… | +34 697 71 13 44 |
| Contact page | PYMEMPRESAS | Same | +34 697 71 13 44 |
| Homepage schema | PYMEMPRESAS | C. Rodríguez San Pedro, 1… | +34-697-71-13-44 (dashes) |
| Oviedo page schema | PYMEMPRESAS | **addressLocality: "Oviedo"** (WRONG) | +34 697 71 13 44 |

### Missing Location Pages

| City | Population | Status |
|------|-----------|--------|
| Avilés | 78K | Marked "Próximamente" — no page exists |
| Langreo | 40K | Only mentioned in areaServed |
| Mieres | 22K | Not mentioned anywhere |

### Review Signals

**Zero review schema on any page.** The site sells review management as a service but practices none of it. No embedded Google reviews, no aggregate rating, no individual Review markup. The 3 testimonials on `/consultoria/` are unverifiable.

---

## Visual / UX — Critical Issues

### C1. Cookie Banner Full-Screen Overlay Blocks All Interaction

The `#cookie-overlay` (`z-index: 99999`) covers the entire viewport on first visit. All navigation links, CTAs, and the hamburger menu are unclickable until the user dismisses it. **Every organic visitor hits a consent wall.**

The cookie banner itself is well-styled (glassmorphism). The problem is that it's a full-screen modal, not a bottom bar that allows interaction with the page behind it.

**Fix:** Convert to a bottom-bar style that doesn't block page interaction, or add a prominent "Cerrar" button that's immediately tappable.

### C2. Horizontal Overflow on /posicionamiento-web-asturias/ Mobile

At 375px viewport, `scrollWidth` is 729px — 354px overflow. The process/timeline section uses horizontal layout that doesn't stack on mobile. Content is clipped/inaccessible.

### H1. Navigation Blocked on First Visit

Hamburger menu works correctly AFTER cookie dismissal. Before dismissal, it's under the overlay. Tablet users (768px) see only the logo — no navigation at all until cookie is accepted.

### H2. CTA Font Size Below Minimum

Primary CTAs use 15px font. WCAG and mobile UX best practices recommend minimum 16px for body text and 18px for CTAs.

### What Works Well

- Color contrast: orange (#F5A623) on black (#0A0A0A) = 9.77:1 (exceeds WCAG AAA)
- Zero layout shift on all tested pages
- Skip-to-content link present
- Inter font loads correctly on all viewports
- Contact form renders correctly on mobile
- No horizontal scroll on most pages (only posicionamiento-web-asturias affected)
- Cookie banner is well-designed visually — the issue is its blocking behavior, not its appearance

---

## Sitemap Issues

### Missing from Sitemap

| URL | Severity | Notes |
|-----|----------|-------|
| `/seo-gijon/` | **HIGH** | Standalone `.astro` page, not in any collection, not in hardcoded array |
| `/aviso-legal/` | MEDIUM | Legal page, intentionally noindex — acceptable |
| `/politica-privacidad/` | MEDIUM | Legal page, intentionally noindex — acceptable |

### Bug: All Service Pages Share Identical lastmod

`sitemap.xml.ts` references `s.data.updatedAt` which does not exist in the `servicios` content schema. All 8 service pages get the hardcoded fallback `2026-05-06`.

**Fix:** Either add `updatedAt: z.date().optional()` to the servicio schema, or use a date field that exists.

### Bug: Hardcoded Static Pages Array

Sitemap generation hardcodes only `['', 'consultoria/', 'contacto/', 'blog/']`. The 3 missing pages must be added manually or the code must be refactored to auto-discover all built pages.

---

## Audit Methodology

- **GSC data:** Real data from Google Search Console (Feb–May 2026), 7 CSV files
- **Live testing:** HTTP headers, redirects, content fetching via curl + WebFetch
- **Source code review:** Full analysis of Astro pages, components, constants, content schemas
- **Visual testing:** 53 screenshots across 5 pages × 4 viewports via Playwright
- **Schema validation:** Manual review against Schema.org specifications
- **Performance:** Estimated CWV based on resource analysis (PageSpeed Insights API exhausted)
- **Competitive:** GSC query analysis for position and impression data

---

## Screenshots

53 screenshots saved to `screenshots/`:
- 5 pages: homepage, seo-local-gijon, diseno-web-gijon, consultoria, contacto
- 4 viewports each: mobile (375px), tablet (768px), laptop (1366px), desktop (1920px)
- Plus: blog article captures, debug captures

---

*Report generated 2026-05-15 by SEO Audit (8 specialist subagents). GSC data period: Feb–May 2026.*
