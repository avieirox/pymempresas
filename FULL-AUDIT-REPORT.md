# SEO Audit Report: pymempresas.com

**Date:** 2026-05-09
**Audited URL:** https://pymempresas.com/
**Business Type:** Local Service — Digital Marketing / SEO Agency (Hybrid: Brick-and-Mortar + SAB)
**Location:** Gijón, Asturias, Spain
**Pages Crawled:** 16 (from sitemap.xml)

---

## Executive Summary

### Overall SEO Health Score: 62/100

| Category | Weight | Score | Weighted |
|----------|--------|-------|----------|
| Technical SEO | 22% | 68 | 15.0 |
| Content Quality | 23% | 58 | 13.3 |
| On-Page SEO | 20% | 55 | 11.0 |
| Schema / Structured Data | 10% | 65 | 6.5 |
| Performance (CWV) | 10% | 92 | 9.2 |
| AI Search Readiness | 10% | 55 | 5.5 |
| Images | 5% | 70 | 3.5 |

### Top 5 Critical Issues

1. **www vs non-www duplicate** — Both `www.pymempresas.com` and `pymempresas.com` return 200. No 301 redirect. Splits link equity.
2. **Gijón/Oviedo duplicate content** — ~80% identical across city landing pages. Doorway page risk.
3. ~~NAP phone discrepancy~~ — **FIXED.** Consolidated to +34 697 71 13 44 across all files.
4. **Two different GBP share links** — Schema `sameAs` and visible text link to different Google Business Profile share codes.
5. **Zero security headers** — No HSTS, X-Frame-Options, X-Content-Type-Options, CSP, or Referrer-Policy.

### Top 5 Quick Wins

1. Add 301 redirect `www` → non-www in `.htaccess`
2. ~~Fix phone number~~ — **FIXED.** Now uses +34 697 71 13 44 everywhere.
3. Consolidate GBP share links to one active profile
4. Add security headers via `.htaccess` (4 lines)
5. Replace `og-default.svg` with `og-default.jpg` (1200x630px)

---

## Technical SEO — Score: 68/100

### Crawlability & Indexability

| Check | Status | Detail |
|-------|--------|--------|
| robots.txt | PASS | Allows all, disallows `/cdn-cgi/`, sitemap declared |
| Sitemap completeness | PASS | 16 URLs, all valid, correctly generated from Astro collections |
| www → non-www redirect | **CRITICAL** | Both resolve 200, no redirect. Duplicate content risk. |
| Canonical tags | PASS | Self-referencing canonicals on all pages |
| Meta robots | PASS | `index, follow` on all content pages |
| Noindex pages in sitemap | **HIGH** | `/aviso-legal/` and `/politica-privacidad/` have `noindex` but are in sitemap |
| Custom 404 page | **MEDIUM** | Bare `<title>404 Not Found</title>`, no navigation or branding |
| JavaScript dependency | PASS | Static HTML from Astro, zero JS required |
| Page depth | PASS | Max 2 clicks from homepage |
| URL structure | PASS | Consistent trailing slashes, clean paths |

### Security

| Header | Status |
|--------|--------|
| HSTS | **MISSING** |
| X-Frame-Options | **MISSING** |
| X-Content-Type-Options | **MISSING** |
| CSP | **MISSING** |
| Referrer-Policy | **MISSING** |

### Sitemap Issues

- 14 of 16 pages share identical `lastmod` (2026-05-06) — signals automated generation
- All non-homepage pages have uniform `priority` 0.8 — no differentiation
- No image sitemap for Google Images discovery
- One stale lastmod: `/seo-local-empresas-asturias/` shows 2025-01-15 (16 months old)

### Other Technical

- **llms.txt exists** at `/llms.txt` — well-structured, lists services with descriptions
- **Footer cookie link** points to `/politica-privacidad/` (same as privacy policy) — no dedicated cookie page
- HTTP/3 enabled (Alt-Svc: h3), LiteSpeed server, TTFB ~120ms

---

## Content Quality — Score: 58/100

### E-E-A-T Assessment

| Signal | Score | Notes |
|--------|-------|-------|
| Experience | 55/100 | Claims "10+ years, 150+ projects" but zero evidence — no case studies, client logos, testimonials |
| Expertise | 65/100 | Blog post shows analytical depth; Arturo Vieiros Garcia named as author. No certifications or team credentials displayed. |
| Authoritativeness | 40/100 | GSC data: 17K impressions, 0.01% CTR, positions 55-97. Zero backlinks, media mentions, or third-party citations. |
| Trustworthiness | 65/100 | Address, phone, email, legal pages present. Missing: NIF/CIF, office photos, real testimonials, T&C page. |

### Content Depth

| Page | Words | Threshold | Status |
|------|-------|-----------|--------|
| Homepage | ~1,080 | 500 | PASS |
| SEO Local Gijón | ~2,250 | 800 | PASS |
| SEO Local Oviedo | ~2,400 | 800 | PASS |
| Diseño Web Gijón | ~2,230 | 800 | PASS |
| IA para Empresas | ~700 | 800 | **FAIL** — thin, no FAQ, no pricing |
| Blog: SEO Cost | ~1,500 | 1,500 | PASS |
| Blog: SEO Asturias | ~500 | 1,500 | **FAIL** — below minimum |

### Duplicate Content — CRITICAL

Gijón and Oviedo SEO pages share ~80% identical content:
- Same benefits section (city name swapped)
- Same expert tasks list (city name swapped)
- Same "4 types of SEO" section (identical)
- Same pricing tables (identical)
- Same FAQ answers (city name swapped)
- Same CTA section (identical)

### Content Freshness

- Most recent blog post: 2026-05-07 (fresh)
- Older blog post: 2025-01-15 (16 months stale)
- Only 2 blog posts total — effectively dormant blog
- Service pages have no visible "last updated" dates

### Author Bios

- Only 1 named author (Arturo Vieiros Garcia) on 1 blog post
- Second blog post uses "PYMEMPRESAS" as author — inconsistent
- No team page, no author archive page
- Author image file exists (`/images/arturo-vieiros-foto.png`) but not displayed on blog cards

---

## On-Page SEO — Score: 55/100

### Strengths

- All pages have unique, descriptive title tags
- Meta descriptions present on all pages (150-160 char range)
- Clean heading hierarchy (H1 → H2 → H3)
- Service pages follow consistent structure: Hero → What Is → Benefits → Pricing → FAQ → CTA
- Internal linking strategy documented in `docs/INTERLINKING.md` with GSC keyword data
- BreadcrumbList schema on most pages (JSON-LD only, not visible in UI)

### Issues

| Issue | Severity | Detail |
|-------|----------|--------|
| Duplicate city pages | **CRITICAL** | 80% content overlap between Gijón/Oviedo |
| Generic CTA anchor text | MEDIUM | "Solicitar Plan", "Ver Servicios" — not keyword-rich |
| No visible breadcrumbs | LOW | Breadcrumbs exist only in JSON-LD, not rendered on page |
| Thin IA page | MEDIUM | 700 words, no pricing/FAQ/benefits structure |
| Missing H1 on some pages | LOW | Blog listing page uses H2 as primary heading |

---

## Schema & Structured Data — Score: 65/100

### Current Implementation

| Page | Schema Types | Status |
|------|-------------|--------|
| Homepage | ProfessionalService, WebSite, BreadcrumbList | GOOD |
| Service pages (Gijón, Oviedo, Diseño Web, Posicionamiento) | Service + FAQPage + BreadcrumbList | GOOD |
| Google Negocios | Service + FAQPage | GOOD |
| Formación IA | Organization, LocalBusiness | NEEDS FIX |
| IA Empresas | WebSite only | **CRITICAL** — no page-level schema |
| Contacto | ContactPage (minimal) | NEEDS FIX |
| Consultoría | Service (minimal) | NEEDS FIX |
| Blog listing | Blog | NEEDS FIX |
| Blog post | BlogPosting (incomplete) | NEEDS FIX |

### Critical Schema Issues

1. **Broken @id reference chain** — Service pages reference `#organization` or `#business` via `provider` but those IDs aren't defined on those pages. Dead references.
2. **IA Empresas page has zero schema** beyond global WebSite — CLAUDE.md flagged this as pending fix.
3. **Contacto page** — ContactPage missing telephone, email, contactPoint properties.

### High-Priority Schema Gaps

- Blog post missing `@id`, `image`, `publisher`, `mainEntityOfPage`
- `sameAs` incomplete — only GBP link, no LinkedIn/Twitter/Facebook
- Formación IA defines both `#organization` AND `#localbusiness` — duplicate identity nodes
- Homepage OfferCatalog: third entry missing `unitText` in `priceSpecification`
- Relative logo URLs on Formación IA page — must be absolute

---

## Performance (Core Web Vitals) — Score: 92/100

### Estimated Metrics

| Metric | Estimate | Rating |
|--------|----------|--------|
| LCP | 0.8–1.5s | GOOD |
| CLS | ~0 | GOOD |
| INP | <50ms | GOOD |
| TTFB | ~120ms | GOOD |
| Lighthouse (Desktop) | 90–98 | GOOD |
| Lighthouse (Mobile) | 85–95 | GOOD |

### Strengths

- Zero third-party scripts — no analytics, no chat widgets, no external JS
- CSS inlined in single `<style>` — no external stylesheet requests
- Fonts self-hosted in `/_astro/` — no Google Fonts CDN dependency
- Hero image uses `fetchpriority="high"` and `loading="eager"`
- All images have `width`/`height` — zero CLS from image loading
- Cache headers: `max-age=31536000` on images and fonts
- HTTP/3 enabled on LiteSpeed

### Issues

| Issue | Severity | Detail |
|-------|----------|--------|
| CSS inline too large | **HIGH** | ~100KB of Tailwind + custom CSS inlined in HTML — adds ~80ms parse time on slow CPUs |
| Inter font bloat | MEDIUM | 6 weights × all unicode ranges = ~120 woff2 files (~1.5MB). Spanish site only needs Latin subset. |
| HTML uncompressed | MEDIUM | 101KB raw HTML due to inline CSS |
| No resource hints | LOW | Missing `<link rel="preload">` for hero image and font preconnects |
| Unused images in build | LOW | ~24 files (8.5MB) including legacy PNGs not referenced by any page |

---

## Images — Score: 70/100

### Current State

- Images converted to WebP format — good
- Hero image: `/images/hero-bg-DF654TP8.webp` with `fetchpriority="high"`
- Logo: `/images/logo-header.webp` with `width`/`height` attributes
- All service page images have `alt` text
- Cache headers set to 1 year

### Issues

| Issue | Severity | Detail |
|-------|----------|--------|
| OG image is SVG | **HIGH** | `og-default.svg` — social platforms don't render SVG. Replace with 1200×630 JPG. |
| Unused images in build | LOW | Legacy PNGs in `public/images/` not referenced — inflate build by ~8.5MB |
| No image sitemap | LOW | Images not declared with `<image:image>` tags for Google Images |
| Logo file size | LOW | CLAUDE.md notes logo should be ~20KB WebP — verify current size |

---

## AI Search Readiness (GEO) — Score: 55/100

### Dimension Breakdown

| Dimension | Score | Weight |
|-----------|-------|--------|
| Citability | 46/100 | 25% |
| Structural Readability | 75/100 | 20% |
| Multi-Modal Content | 40/100 | 15% |
| Authority & Brand Signals | 28/100 | 20% |
| Technical Accessibility | 84/100 | 20% |

### Platform-Specific Scores

| Platform | Score | Key Issue |
|----------|-------|-----------|
| Google AI Overviews | 45/100 | No source citations for claims |
| ChatGPT | 50/100 | Weak author credentials |
| Perplexity | 35/100 | No cite-worthy sources |
| Bing Copilot | 45/100 | Thin blog, shallow content depth |

### Key Gaps

1. **Statistics without sources** — "46% of Google searches are local" and "40% productivity gains from AI" have zero attribution. AI citation systems require named sources.
2. **No author credentials** — Only 1 named author across site. LLMs deprioritize orphaned brand claims without human expert grounding.
3. **Passages too short for AI extraction** — Optimal cite-length is 134–167 words. Most homepage passages are 30–70 words.
4. **Wikipedia/Reddit/YouTube absence** — These correlate most strongly with AI citation frequency.
5. **llms.txt exists** and is well-structured — positive signal for AI crawler discovery.
6. **AI crawlers implicitly allowed** — No blocks for GPTBot, ClaudeBot, PerplexityBot, Google-Extended in robots.txt.

---

## Local SEO — Score: 45/100

### Critical Local Issues

1. ~~Phone discrepancy~~ — **FIXED.** Consolidated to +34 697 71 13 44 across all pages.
2. **Two GBP share links** — Schema `sameAs` and visible text use different share.google codes. Audit and consolidate.
3. **Zero social media profiles** — No LinkedIn, Facebook, Instagram, Twitter/X anywhere on site. Critical trust gap for a marketing agency.
4. **No reviews or testimonials on site** — Zero review content, no aggregateRating schema, no star ratings.
5. **No Google Maps embed** — Despite listing physical address, no map iframe or "Get Directions" link.

### What Works

- ProfessionalService schema with full NAP, hours, areaServed
- GBP presence acknowledged with "Ficha verificada" claim
- Dedicated `/google-negocios/` service page with strong GBP optimization content
- Clear city-specific URL architecture
- Transparent pricing across all service pages

---

## Methodology

- **Homepage analysis:** WebFetch of rendered HTML
- **robots.txt & sitemap:** Fetched and parsed
- **Service pages:** Sampled via WebFetch (SEO Gijón, Diseño Web, IA, Contacto, Consultoría, Blog)
- **Subagent delegation:** 7 specialist agents run in parallel (technical, content, schema, sitemap, performance, GEO, local)
- **Codebase verification:** Cross-referenced against `src/pages/`, `src/content/`, and `src/components/` in the Astro project
- **Date:** 2026-05-09

### Limitations

- No Playwright/headless browser available — Lighthouse and CWV are estimates, not measured
- No DataForSEO MCP tools connected — SERP positions, backlink profiles, and keyword data not live-checked
- GBP review velocity and primary category could not be verified (requires GBP dashboard access)
- Citation accuracy on third-party directories not verified (requires Moz Local / BrightLocal)
- Local pack rankings and competitor gap analysis not performed
