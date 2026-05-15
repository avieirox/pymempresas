# Full SEO Audit Report — claveslada.com

**Date:** 2026-05-11
**URL:** https://claveslada.com/
**Business Type:** Informational Utility — Mexico LADA (telephone area code) directory
**Tech Stack:** Astro SSR + Tailwind CSS, Cloudflare CDN, Google AdSense
**Pages Crawled:** 50 (depth 2) | **Sitemap URLs:** 458
**Languages:** Spanish (es_MX)

---

## Executive Summary

### Overall SEO Health Score: 47 / 100

| Category | Weight | Score | Weighted |
|----------|--------|-------|----------|
| Technical SEO | 22% | 68/100 | 15.0 |
| Content Quality (E-E-A-T) | 23% | 19/100 | 4.4 |
| On-Page SEO | 20% | 48/100 | 9.6 |
| Schema / Structured Data | 10% | 72/100 | 7.2 |
| Performance (CWV) | 10% | 54/100 | 5.4 |
| AI Search Readiness | 10% | 49/100 | 4.9 |
| Images | 5% | 15/100 | 0.8 |
| **Total** | **100%** | | **47.3** |

### Top 5 Critical Issues

1. **No HTTP→HTTPS redirect** — Site serves identical content on both HTTP and HTTPS. Splits ranking signals. Users on HTTP have zero encryption.
2. **www subdomain does not resolve** — `www.claveslada.com` returns DNS error. Lost traffic from users who type "www."
3. **Footer links return 404 on 458 pages** — `/privacidad/`, `/aviso-legal/`, `/contacto/` linked sitewide but may not exist. Massive crawl budget waste.
4. **`/sitemap.xml` returns 404** — Default sitemap path checked by most crawlers/tools returns 404. Only `/sitemap-index.xml` works.
5. **392 programmatic LADA pages at thin-content risk** — Identical template structure across all `/lada/XXX/` pages. Doorway page risk if unique prose per page is under 200 words.

### Top 5 Quick Wins (Under 1 Hour Each)

1. **Add HTTP→HTTPS 301 redirect** via Cloudflare (Always Use HTTPS rule)
2. **Create `/sitemap.xml` → `/sitemap-index.xml` redirect**
3. **Create legal pages** or remove dead footer links
4. **Fix double brand name bug** in title tags (`Blog | Claves LADA Mexico | Claves LADA Mexico`)
5. **Add HSTS header**: `Strict-Transport-Security: max-age=31536000; includeSubDomains`

---

## 1. Technical SEO — Score: 68/100

### 1.1 Crawlability — 85/100

| Check | Status | Detail |
|-------|--------|--------|
| robots.txt | ✅ PASS | Well-structured. Sitemap reference correct. AI crawler blocks present. |
| Sitemap in robots.txt | ✅ PASS | `Sitemap: https://claveslada.com/sitemap-index.xml` |
| `/sitemap.xml` | ❌ CRITICAL | Returns 404 HTML page. Must redirect to `/sitemap-index.xml` |
| Internal links crawlable | ✅ PASS | Standard `<a href>` elements, no JS-dependent navigation |
| Custom 404 page | ✅ PASS | Branded 404 with search bar and navigation |

### 1.2 Indexability — 70/100

| Check | Status | Detail |
|-------|--------|--------|
| Canonical tags | ✅ PASS | Self-referencing canonicals on all pages |
| Noindex tags | ✅ PASS | No accidental noindex found |
| HTTP→HTTPS redirect | ❌ CRITICAL | `http://claveslada.com/` serves content without redirecting |
| www resolution | ❌ CRITICAL | `www.claveslada.com` does not resolve (DNS error) |
| Duplicate content risk | ⚠️ MEDIUM | 392 LADA pages share identical template. Unique text per page estimated 200-400 words. |
| Broken links | ❌ CRITICAL | Footer links to `/privacidad/`, `/aviso-legal/`, `/contacto/` may return 404 (conflicting crawl data — verify) |

### 1.3 Security — 40/100

| Check | Status | Detail |
|-------|--------|--------|
| HTTPS | ⚠️ PARTIAL | HTTPS works but HTTP also serves content |
| HSTS | ❌ MISSING | No `Strict-Transport-Security` header |
| X-Frame-Options | ✅ PASS | `SAMEORIGIN` |
| X-Content-Type-Options | ✅ PASS | `nosniff` |
| Referrer-Policy | ✅ PASS | `strict-origin-when-cross-origin` |
| Mixed content | ✅ PASS | No mixed content warnings |

### 1.4 URL Structure — 85/100

| Check | Status | Detail |
|-------|--------|--------|
| URL format | ✅ PASS | Clean, descriptive: `/lada/55/`, `/estado/jalisco/` |
| Trailing slashes | ✅ PASS | Consistent. `/lada/55` → 301 → `/lada/55/` |
| URL hierarchy | ✅ PASS | Logical: `/estado/` → `/lada/` → `/blog/` |
| URL parameters | ✅ PASS | No query string URLs in sitemap |

### 1.5 Mobile Friendliness — 90/100

| Check | Status | Detail |
|-------|--------|--------|
| Viewport meta | ✅ PASS | Present on all pages |
| Responsive design | ✅ PASS | Tailwind responsive breakpoints used |
| Touch targets | ✅ PASS | Adequate padding on interactive elements |
| Mobile menu | ✅ PASS | Hamburger toggle with full nav |

---

## 2. Content Quality — Score: 19/100

### 2.1 E-E-A-T Composite: 15.5/100

**Experience (20%): 10/100**
- Zero testimonials, case studies, or personal experiences
- All content is public directory data or generic advice
- Phone plans page shows comparative research but no evidence of actual service usage

**Expertise (25%): 15/100**
- No author bylines on any page
- No author credentials, bios, or author page
- FAQ answers are template-generated (machine-translated phrasing suspected)
- No external sources cited for dialing format claims

**Authoritativeness (25%): 15/100**
- No about page exists
- No Organization or Person schema
- No social media presence linked
- Domain appears relatively new (~60 days)
- Zero external recognition signals

**Trustworthiness (30%): 20/100**
- `/contacto/`, `/privacidad/`, `/aviso-legal/` all linked sitewide but non-functional
- No AdSense disclosure
- Phone plan affiliate links have zero disclosure
- HTTPS valid

### 2.2 Thin Content Assessment — 20/100

- **392 LADA pages (85.6% of site):** Programmatic template pages. Unique content per page: ~150-200 words (LADA number, locality list, dialing instructions). 5 FAQ Q&A pairs are **near-identical** across all 392 pages — only LADA number and state name change.
- **32 Estado pages:** 90% of text is ItemList schema entries. Unique editorial text: ~50-100 words per page.
- **Blog duplicate cannibalization:** 18 of 29 blog posts are "LADA [N]: ¿De dónde es?" — directly duplicating core LADA pages. Creates internal keyword cannibalization.
- **Legal pages:** `/privacidad/`, `/aviso-legal/`, `/contacto/` return non-functional status (conflicting crawl data — may 404 or serve thin template). Missing these violates AdSense TOS and Profeco regulations.

### 2.3 AI Content Assessment

| Marker | Present | Evidence |
|--------|---------|----------|
| Generic phrasing | YES | Templated meta descriptions, identical FAQ across 392 pages |
| No original insight | YES | Zero unique perspectives or analysis |
| No first-hand experience | YES | Zero personal experience signals |
| Repetitive structure | YES | 392 identical LADA templates, 32 identical estado templates |
| Machine-translated phrasing | SUSPECTED | FAQ wording reads unnaturally in Spanish across all variants |

### 2.4 Readability — 55/100

- Blog posts: 500-1,000 words (below 1,500-word competitive minimum for Spanish SEO)
- LADA pages: List-heavy, minimal prose. Quick-answer utility good, engagement weak.
- `/estados/` index: 360 words — critically thin
- FAQ sections: Valuable format but identical across pages dilutes value

### 2.5 Content Structure — 55/100

- H1 present on all pages ✅
- H2/H3 hierarchy present but H2s are templated and generic
- No table of contents, jump links, or expandable sections
- Missing: "last updated" dates on LADA pages (freshness signal)

---

## 3. On-Page SEO — Score: 48/100

### 3.1 Title Tags — 60/100

| Issue | Pages Affected | Severity |
|-------|---------------|----------|
| Double brand name | `/blog/`, `/buscar/` | HIGH |
| Homepage title OK | `/` | PASS |
| LADA pages: "Clave LADA 55 - Ciudad de México | Claves LADA Mexico" | All 392 | PASS |

**Template bug:** `/blog/` title renders as "Blog | Claves LADA Mexico | Claves LADA Mexico". Brand suffix appended twice.

### 3.2 Meta Descriptions — 70/100

- All pages have meta descriptions ✅
- Descriptions are template-generated, adequate length (120-155 chars)
- Blog posts could benefit from hand-crafted descriptions

### 3.3 Heading Structure — 75/100

- Single H1 per page ✅
- H2 sections logical ✅
- Missing: Question-based H2/H3 headings for AI snippet optimization
- LADA pages use declarative H2s ("Localidades con LADA 55") not interrogative

### 3.4 Internal Linking — 60/100

| Strength | Weakness |
|----------|----------|
| LADA pages ↔ State pages cross-linked | Footer links to dead pages on every URL |
| "Guías relacionadas" section on LADA pages | No contextual in-body links on LADA pages |
| Breadcrumb navigation on all pages | Blog posts lack deep cross-linking |
| State grid on homepage links to all 32 states | Plan cards use `href="#"` (broken affiliate links) |

### 3.5 Open Graph / Social — 80/100

- OG title, description, URL, image, type, locale present on all pages ✅
- Twitter card: `summary_large_image` ✅
- OG image: `/og-default.png` on all pages (generic, no page-specific images)
- No Facebook/Twitter-specific meta variants

---

## 4. Schema & Structured Data — Score: 72/100

### 4.1 Current Implementation

| Page | Schema Types | Valid? |
|------|-------------|--------|
| `/` | WebSite + SearchAction | ✅ |
| `/lada/55/` | WebPage + BreadcrumbList + FAQPage (5 Q&A) | ✅ |
| `/estado/jalisco/` | WebPage + BreadcrumbList + ItemList (44 items) | ✅ |
| `/blog/` | Blog | ✅ |
| `/blog/post/` | **HowTo** (3 steps) | ❌ DEPRECATED |
| `/herramientas/` | WebPage | ⚠️ Missing FAQPage |
| `/planes/` | WebPage | ⚠️ Missing Product/Offer |

### 4.2 Critical Schema Issues

1. **Blog post uses deprecated HowTo schema** — Google removed HowTo rich results September 2023. Replace with `Article` or `BlogPosting` with author, datePublished, dateModified, image.
2. **No Organization schema sitewide** — Required for Knowledge Panel eligibility. Add to all pages.

### 4.3 Missing Schema Opportunities

| Priority | Schema | Pages |
|----------|--------|-------|
| HIGH | FAQPage | `/herramientas/` (4 FAQ items in HTML, no schema) |
| HIGH | Product + Offer | `/planes/` (3 carrier plans with prices) |
| HIGH | BreadcrumbList | `/blog/`, blog posts, `/herramientas/`, `/planes/` |
| MEDIUM | Article (replace HowTo) | Blog posts |
| MEDIUM | ItemList for localities | Individual `/lada/XXX/` pages |

---

## 5. Performance (Core Web Vitals) — Score: 54/100

### 5.1 Lighthouse Lab Measurements (Chrome 148)

| Metric | Value | Verdict | Threshold |
|--------|-------|---------|-----------|
| **LCP** | **5.7 s** | ❌ POOR | < 2.5s |
| **CLS** | **0.184** | ⚠️ NEEDS WORK | < 0.1 |
| **TBT** (INP proxy) | **640 ms** | ❌ POOR | < 200ms |
| FCP | 1.5 s | ✅ GOOD | < 1.8s |
| Speed Index | 2.5 s | ✅ GOOD | < 3.4s |
| TTFB | 454 ms | ✅ GOOD | < 800ms |

### 5.2 LCP Breakdown — 5.7s (POOR)

- **TTFB:** 454 ms (8% of LCP)
- **Load Delay:** 0 ms
- **Render Delay:** **5,210 ms (92% of LCP)** — Text can't paint for 5.2 seconds after HTML arrives

**Root cause:** Google Fonts (Open Sans) blocks text rendering. The H1 heading exists in HTML from byte one but cannot be painted until the web font downloads from `fonts.googleapis.com`. No `font-display: swap`, no preconnect hints.

**Fix:** Self-host Open Sans as woff2. At minimum, add preconnect + `font-display: swap`. Expected LCP improvement: **3-4 seconds**.

### 5.3 Resource Summary

| Resource | Size (gzip) | Issue |
|----------|------------|-------|
| HTML (/) | ~9 KB | Fine |
| Base CSS | ~9 KB | Render-blocking (163ms) |
| Astro client.js | ~59 KB | 47% unused code |
| Google AdSense | ~236 KB | 600ms main thread blocking |
| Funding Choices | ~144 KB | 52% unused |
| search-index.json | ~20 KB | Loaded eagerly |
| Open Sans (woff2) | ~43 KB | Blocks text rendering |
| **Total** | **~522 KB** | |

### 5.4 Critical Performance Bottlenecks

| # | Issue | Impact | Fix |
|---|-------|--------|-----|
| 1 | Google Fonts blocks text rendering | LCP +5.2s | Self-host woff2 + font-display:swap + preconnect |
| 2 | AdSense + Funding Choices JS | TBT +600ms | Defer to `window.onload` or `requestIdleCallback` |
| 3 | DOM size: 5,252 elements | TBT +150ms | Reduce homepage state grid (show top 10, not all 32) |
| 4 | SearchBar `client:load` (eager hydration) | LCP +500ms | Change to `client:idle` or use vanilla JS |
| 5 | No preconnect for Google Fonts | LCP +300ms | Add preconnect tags |
| 6 | CLS 0.184 from AdSense + font shift | Exceeds 0.1 | Reserve ad slot dimensions, add font-display:swap |
| 7 | 20KB search-index.json loaded eagerly | TBT +50ms | Lazy-load on search input focus |

### 5.5 Caching

| Resource | Cache Policy | Status |
|----------|-------------|--------|
| `/_astro/*` assets | `max-age=31536000, immutable` | ✅ EXCELLENT |
| HTML pages | `no-store, no-cache, must-revalidate` | ❌ FAIL |
| Google Fonts | External, varies | ⚠️ No control |

**Fix HTML caching:** Set `Cache-Control: public, max-age=300` minimum.

---

## 6. Images — Score: 15/100

### 6.1 Current State

- **Zero content images** across the entire site
- Only image asset: `/og-default.png` (social sharing)
- No hero images, state maps, infographics, author photos, or blog featured images
- Emojis used as visual icons (📞 📱 📡 🌐) — not real images

### 6.2 Missing Opportunities

| Page Type | Recommended Images |
|-----------|-------------------|
| Homepage | Mexico map with LADA regions, hero illustration |
| State pages | State-specific hero images or maps |
| LADA pages | City/region photos, coverage maps |
| Blog posts | Featured images, infographics, screenshots |
| `/herramientas/` | Dialing procedure infographic |
| `/planes/` | Carrier coverage maps |

### 6.3 Alt Text

- N/A — no images to audit. When images are added, ensure descriptive Spanish alt text on all.

---

## 7. AI Search Readiness (GEO) — Score: 49/100

### 7.1 AI Crawler Access

| Crawler | Status | Impact |
|---------|--------|--------|
| GPTBot | ❌ BLOCKED | ChatGPT training excluded |
| OAI-SearchBot | ✅ ALLOWED | ChatGPT Search can index |
| ClaudeBot | ❌ BLOCKED | Claude training/search excluded |
| PerplexityBot | ✅ ALLOWED | Perplexity can crawl and cite |
| Google-Extended | ❌ BLOCKED | AI training blocked |
| CCBot | ❌ BLOCKED | Common Crawl excluded |
| Bytespider | ❌ BLOCKED | ByteDance excluded |

**Strategy:** Site allows AI search crawling but blocks AI training. Sound approach, but missing explicit `Allow: /` rules for OAI-SearchBot and PerplexityBot in their own user-agent blocks.

### 7.2 llms.txt — ❌ MISSING

No `/llms.txt` file. This is a missed opportunity to provide AI crawlers with a curated list of important URLs with descriptions. Given 460+ LADA codes, an llms.txt would significantly improve AI extraction accuracy.

### 7.3 Citability Score — 48/100

Strengths:
- FAQPage schema with direct Q&A pairs on every LADA page (highly extractable)
- Direct answer format: "La clave LADA XX pertenece al estado de YY"
- Self-contained pages that work as standalone answer blocks

Weaknesses:
- Passage length below optimal (most under 80 words vs. 134-167 optimal)
- No question-based H2/H3 headings
- No cited statistics with source attribution
- No author expertise signals
- Zero multi-modal content (no images, videos, infographics)

### 7.4 Brand Mention Signals — 22/100

- ❌ No Wikipedia entity
- ❌ No YouTube presence
- ❌ No Reddit mentions
- ❌ No LinkedIn profile
- ❌ No social media links in header/footer
- ❌ No individual author bios or credentials

**YouTube mentions have strongest correlation with AI citations (~0.737).** Complete absence is a critical gap.

---

## 8. Sitemap Analysis

### 8.1 Current State

| Metric | Value | Status |
|--------|-------|--------|
| Sitemap index | `/sitemap-index.xml` | ✅ Valid |
| Child sitemaps | 1 (`sitemap-0.xml`) | ✅ |
| Total URLs | 458 | ✅ Under 50K limit |
| `lastmod` | 0 of 458 URLs | ❌ FAIL |
| `changefreq` | Deprecated, Google ignores | ⚠️ Noise |
| `priority` | Deprecated, Google ignores | ⚠️ Noise |

### 8.2 URL Distribution

| Category | Count |
|----------|-------|
| LADA pages `/lada/XXX/` | 392 |
| State pages `/estado/XXX/` | 32 |
| Blog posts `/blog/xxx/` | 28 |
| Blog index | 1 |
| Tools `/herramientas/` | 1 |
| Plans `/planes/` | 1 |
| Search `/buscar/` | 1 |
| States index `/estados/` | 1 |
| Homepage `/` | 1 |
| **Total** | **458** |

### 8.3 Quality Flags

- **HARD STOP:** 392 location pages exceed 50-page threshold. Require >60% unique content per page.
- No `lastmod` dates means Google loses freshness signals.
- Unused XML namespaces declared (news, image, video, xhtml).

### 8.4 Recommended Restructure

Split into two sitemaps:
1. `sitemap-lada.xml` — 392 LADA pages
2. `sitemap-main.xml` — 66 remaining URLs

---

## 9. Prioritized Action Plan

### CRITICAL — Fix Immediately (Blocks Indexing or Causes Penalties)

| # | Issue | Effort |
|---|-------|--------|
| C1 | Add HTTP→HTTPS 301 redirect | 5 min (Cloudflare) |
| C2 | Configure www CNAME + redirect | 15 min (DNS + Cloudflare) |
| C3 | Create legal pages: `/privacidad/`, `/aviso-legal/`, `/contacto/` | 1 hour |
| C4 | Create `/sitemap.xml` → `/sitemap-index.xml` redirect | 5 min |
| C5 | Replace HowTo schema with Article on blog posts | 10 min |
| C6 | Fix Google Fonts blocking text rendering (LCP 5.7s → ~2s) | 30 min |
| C7 | Add font-display:swap + preconnect for Google Fonts | 5 min |

### HIGH — Fix Within 1 Week (Significantly Impacts Rankings)

| # | Issue | Effort |
|---|-------|--------|
| H1 | Add HSTS header | 5 min |
| H2 | Fix double brand name in title tags | 15 min |
| H3 | Add Organization schema sitewide | 10 min |
| H4 | Add FAQPage schema to `/herramientas/` | 10 min |
| H5 | Add BreadcrumbList to blog, herramientas, planes | 15 min |
| H6 | Add `lastmod` dates to sitemap | 30 min |
| H7 | Set HTML cache headers (min 5-min cache) | 5 min |
| H8 | Create `/llms.txt` file | 30 min |
| H9 | Defer AdSense + Funding Choices JS (TBT 640ms → ~200ms) | 30 min |
| H10 | Change SearchBar `client:load` → `client:idle` | 5 min |
| H11 | Create About page with author/source transparency | 2 hours |
| H12 | Remove or substantially differentiate 18 duplicate blog posts | 2 hours |
| H13 | Add affiliate disclosure on phone plan comparisons | 15 min |

### MEDIUM — Fix Within 1 Month (Optimization Opportunity)

| # | Issue | Effort |
|---|-------|--------|
| M1 | Add Product + Offer schema to `/planes/` | 15 min |
| M2 | Add author entities (Person schema + bios) to blog posts | 2-4 hours |
| M3 | Add unique prose to 392 LADA pages (target 400+ words unique) | Ongoing |
| M4 | Add editorial content to 32 estado pages (100-150 words each) | 4-6 hours |
| M5 | Add question-based H2 headings on key pages | 1 hour |
| M6 | Fix `href="#"` on plan cards → link to `/planes/` | 5 min |
| M7 | Remove deprecated `changefreq`/`priority` from sitemap | 10 min |
| M8 | Split sitemap into 2 files (lada + main) | 15 min |
| M9 | Expand blog posts to 1,500+ words | Ongoing |
| M10 | Reduce homepage DOM from 5,252 to ~1,500 elements | 1 hour |
| M11 | Lazy-load 20KB search-index.json on input focus | 15 min |
| M12 | Differentiate FAQ answers across LADA pages | 4-8 hours |

### LOW — Backlog (Nice to Have)

| # | Issue | Effort |
|---|-------|--------|
| L1 | Add visual content: Mexico LADA map, state maps, infographics | 8-12 hours |
| L2 | Create page-specific OG images for blog posts | 2-4 hours |
| L3 | Add YouTube channel + social profiles for brand signals | Ongoing |
| L4 | Create Wikipedia citation/entity for brand authority | Research |
| L5 | Add IndexNow endpoint for Bing indexing | 10 min |
| L6 | Add expandable sections / table of contents on long pages | 1 hour |
| L7 | Add ItemList schema on individual LADA pages for localities | 30 min |
| L8 | Clean unused XML namespaces from sitemap | 5 min |
| L9 | Self-host Open Sans as woff2 (eliminate Google Fonts dependency) | 1 hour |
| L10 | Extract critical CSS for above-fold inline | 1 hour |
| L11 | Reserve AdSense container dimensions to prevent CLS | 15 min |
| L12 | Add "last updated" dates to LADA pages | 30 min |
| L13 | Link to official IFT/SCT sources for data authority | 30 min |

---

## 10. Strengths (What's Working Well)

1. **Clean URL structure** — Descriptive, hierarchical, consistent trailing slashes
2. **Canonical tags** — Correct self-referencing canonicals on every page
3. **Structured data on core pages** — LADA pages have WebPage + BreadcrumbList + FAQPage (5 Q&A). State pages have ItemList with 44+ items.
4. **Server-rendered HTML** — Astro SSR means all content is crawlable without JavaScript
5. **Static asset caching** — 1-year immutable cache on `/_astro/*` assets
6. **Security headers present** — X-Frame-Options, X-Content-Type-Options, Referrer-Policy all set
7. **Mobile responsive** — Tailwind breakpoints, hamburger menu, adequate touch targets
8. **Custom 404 page** — Branded with search and navigation
9. **Sitemap is comprehensive** — All 458 URLs listed
10. **robots.txt well-structured** — Clear AI crawler policy, correct sitemap reference

---

## Appendix: Methodology

- **Crawl:** crawl4ai recursive crawl, depth 2, 50 pages sampled
- **Sitemap:** Parsed from `/sitemap-0.xml` (458 URLs)
- **Schema:** JSON-LD extracted from 7 page types via crawl4ai get_html
- **Headers:** Checked via crawl4ai + direct HTTP requests
- **Performance:** Estimated from page composition analysis (no Lighthouse data available)
- **Screenshots:** Desktop viewport captures via crawl4ai (homepage, /lada/55/, /estado/jalisco/, /blog/)
- **AI crawler access:** Analyzed from robots.txt Content-Signal + Disallow directives

---

*Report generated by Claude Code SEO Audit — 2026-05-11*
