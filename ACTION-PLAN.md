# SEO Action Plan — pymempresas.com

**Date:** 2026-05-15
**Overall SEO Health Score:** 57/100
**Goal:** Move from page 5–10 (pos 55–97) to page 1–2 (pos 1–20) for target queries

---

## Priority Quick Reference

| Priority | Count | Timeframe |
|----------|-------|-----------|
| Critical | 8 | Fix immediately (this week) |
| High | 10 | Fix within 2 weeks |
| Medium | 8 | Fix within 1 month |
| Low | 6 | Backlog |

---

## CRITICAL — Fix Immediately (This Week)

### C1. Fix Cookie Banner Overlay — Blocks All First-Visit Interaction

**Impact:** Every organic visitor (100% of traffic) hits a full-screen overlay that blocks all CTAs, navigation, and scroll.

**Fix in `src/components/CookieBanner.astro`:**
- Change from full-screen modal (`position: fixed; inset: 0`) to a bottom bar
- OR remove the overlay div and keep only the banner itself clickable
- Ensure hamburger menu, hero CTAs, and nav links are accessible without cookie dismissal
- **Effort:** 30 minutes

### C2. Fix Schema @id References — Centralize LocalBusiness

**Impact:** All service pages reference an entity (`#organization`) that doesn't exist. Google cannot connect services to the business. Zero rich results are generated.

**Fix in `src/layouts/BaseLayout.astro`:**
- Add complete `LocalBusiness` with `@id: "https://pymempresas.com/#business"` to the `@graph`
- Include: name, url, logo, telephone, email, full address, geo, openingHours, areaServed, priceRange

**Fix in all service pages:**
- Change `"provider": { "@id": "https://pymempresas.com/#organization" }` → `"@id": "https://pymempresas.com/#business"`
- Pages: `index.astro`, `seo-local-gijon.astro`, `seo-local-oviedo.astro`, `seo-gijon.astro`, `posicionamiento-web-asturias.astro`, `inteligencia-artificial-empresas.astro`, `formacion-ia-empresas.astro`, `automatizaciones-con-ia.astro`, `google-negocios.astro`, `consultoria.astro`, `diseno-web-gijon.astro`
- **Effort:** 2 hours

### C3. Convert Author Photo — 2.1MB PNG → 10KB WebP

**Impact:** Every blog page loads 4.2MB of unnecessary image data. Mobile LCP estimated 3–5s — this fix alone could bring it below 2.5s.

**Fix:**
1. Convert `public/images/arturo-vieiros-foto.png` (2,165KB) to WebP 256×256px (~10KB)
2. Update all references in blog frontmatter and components to use `.webp`
3. Add `width="64" height="64" loading="lazy"` to both author image instances (ArticleHero + AuthorCard)
4. **Effort:** 15 minutes

### C4. Fix Oviedo Schema Address

**Impact:** `/seo-local-oviedo/` schema sets `addressLocality: "Oviedo"`. The business is physically in Gijón. Google sees contradictory location signals.

**Fix in `src/pages/seo-local-oviedo.astro`:**
- Remove `addressLocality: "Oviedo"` from LocalBusiness
- Set `addressLocality: "Gijón"` (physical business address)
- Use `areaServed` to indicate Oviedo as a service area
- **Effort:** 5 minutes

### C5. Add Security Headers

**Impact:** Site has zero security headers. This is a minor ranking signal and a basic web standard.

**Fix via `.htaccess` or Cloudflare Dashboard:**
```
Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains; preload"
Header always set X-Content-Type-Options "nosniff"
Header always set X-Frame-Options "SAMEORIGIN"
Header always set Referrer-Policy "strict-origin-when-cross-origin"
```
- **Effort:** 10 minutes in Cloudflare

### C6. Fix Custom 404 Page

**Impact:** LiteSpeed default 404 serves a generic unbranded error page. Astro's `dist/404.html` exists but is not configured.

**Fix:** Add to `.htaccess`:
```
ErrorDocument 404 /404.html
```
- **Effort:** 2 minutes

### C7. Add `/seo-gijon/` to Sitemap

**Impact:** A 5,500-word page with unique content is invisible to sitemap-based discovery. Directly contributes to indexing gap (11 indexed vs 18 in sitemap).

**Fix in `src/pages/sitemap.xml.ts`:**
- Add `'seo-gijon/'` to the hardcoded `pages` array
- **Effort:** 5 minutes

### C8. Generate OG JPG Image

**Impact:** Facebook, Twitter, LinkedIn, WhatsApp do not support SVG OG images. Shared links appear without preview images → suppressed CTR from social.

**Fix:**
1. Create `public/og-default.jpg` — 1200×630px, ~50KB
2. Update `SEO.astro` to reference `.jpg` as primary OG image
3. **Effort:** 20 minutes

---

## HIGH — Fix Within 2 Weeks

### H1. Differentiate Oviedo Page from Gijón (~60% Duplicate)

**Impact:** Google's helpful content system (merged into core, Sept 2025) may devalue both pages due to near-duplicate content.

**Minimum unique content required:**
- Rewrite Benefits section with Oviedo-specific local data
- Rewrite all 5 duplicated FAQ answers with different angles
- Rewrite at least 5 of 10 Expert Tasks with Oviedo-specific examples
- Add Oviedo-specific statistics or market data
- **Effort:** 4 hours

### H2. Create Team/About Page

**Impact:** E-E-A-T is the single biggest ranking suppressor. Zero verifiable expertise exists on the site.

**Create `/equipo/` or `/sobre-nosotros/`:**
- Team member names, photos, roles
- Professional certifications and years of experience
- LinkedIn profiles linked
- Company history (founding date, mission)
- Industry affiliations or awards
- **Effort:** 4 hours

### H3. Add FAQPage Schema to All Service Pages

**Impact:** FAQ content exists on most pages but without JSON-LD. Rich results and AI extraction impossible.

**Pages needing FAQPage schema added:**
- `/inteligencia-artificial-empresas/` (has FAQ content, missing schema)
- `/automatizaciones-con-ia/` (has FAQ content, missing schema — also add WebPage)
- Verify all other service pages have FAQPage in their `@graph`

**Template (add to page's @graph array):**
```json
{
  "@type": "FAQPage",
  "@id": "https://pymempresas.com/[slug]/#faq",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Question text here",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Answer text here"
      }
    }
  ]
}
```
- **Effort:** 2 hours (can be automated since FAQs come from frontmatter)

### H4. Complete LocalBusiness Schema on Service Pages

**Impact:** 7 of 11 pages with LocalBusiness are missing `streetAddress`, `postalCode`, `geo`, `image`/`logo`. Google needs these for local relevance signals.

**Add to all service page LocalBusiness entities:**
```
streetAddress, postalCode, geo (43.54124, -5.66205), openingHoursSpecification, image, sameAs
```
- **Effort:** 1 hour (copy from BaseLayout once centralized)

### H5. Restrict Fonts to Latin-Only woff2

**Impact:** 42 @font-face declarations vs 3 needed. Inline CSS shrinks ~6KB. 81 unused font files eliminated from dist (~1.3MB). Font discovery ~500ms faster.

**Fix in `src/styles/global.css`:**
Replace the 5 `@import "@fontsource/inter/..."` lines with:
```css
@font-face {
  font-family: 'Inter';
  font-style: normal;
  font-display: swap;
  font-weight: 400;
  src: url('/_astro/inter-latin-400-normal.HASH.woff2') format('woff2');
  unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+2000-206F, U+2074, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;
}
/* Repeat for 600 and 700 */
```
- **Effort:** 30 minutes (may need build to discover hashed filenames)

### H6. Preload Critical Resources

**Impact:** LCP improves ~500–1000ms on mobile. Browser discovers hero image and fonts before parsing 97KB CSS.

**Add to `BaseLayout.astro` `<head>`:**
```html
<link rel="preload" href="/images/hero-bg-DF654TP8.webp" as="image" type="image/webp" fetchpriority="high">
<link rel="preconnect" href="https://www.googletagmanager.com" crossorigin>
```
- **Effort:** 10 minutes

### H7. Create Avilés Landing Page

**Impact:** Avilés (78K pop.) is referenced in footer, nav, areaServed, and google-negocios page (marked "Próximamente") but has no dedicated page. Missed local market.

**Create `/seo-local-aviles/`:**
- Follow Gijón/Oviedo template but with 100% unique content
- Avilés-specific neighborhoods: Sabugo, Versalles, La Carriona, El Quirinal, Llaranes, Villalegre
- City-specific search examples and business context
- **Effort:** 4 hours

### H8. Add Location Keywords to Title Tags

**Fix titles:**
- Homepage: "Agencia de Posicionamiento Web y SEO Local en Gijón, Asturias | PYMEMPRESAS"
- IA page: "Inteligencia Artificial para Empresas en Gijón y Asturias | PYMEMPRESAS"
- Blog: "Blog de SEO y Marketing Digital para PYMES en Asturias | PYMEMPRESAS"
- **Effort:** 15 minutes

### H9. Remove/Replace Deprecated sameAs URL

**Fix in homepage schema:**
- Remove: `"https://share.google/PbUpboFKMelaHcNgg"` (Google Posts, decommissioned 2023)
- Add: LinkedIn company page, Twitter/X profile
- **Effort:** 5 minutes

### H10. Fix Missing Schema Types

**Add to these pages:**
- `/automatizaciones-con-ia/`: WebPage, FAQPage, serviceType, image
- `/consultoria/`: WebPage, BreadcrumbList
- `/diseno-web-gijon/`: WebPage, BreadcrumbList
- `/contacto/`: mainEntity pointing to `#business`
- **Effort:** 2 hours

---

## MEDIUM — Fix Within 1 Month

### M1. Expand Homepage Content to 800+ Words

**Current:** ~300 words substantive. Reads as gateway page, not landing page.

**Add:** Company history/philosophy section (200+ words), expanded services section with unique value propositions, named client examples or industry experience.
- **Effort:** 2 hours

### M2. Fix Internal Linking — Move from Footer to Body Text

**Current:** Cross-links between service pages appear only in small gray 14px footer paragraphs.

**Implementation:** INTERLINKING.md already defines the strategy. Weave GSC-verified anchor text naturally into body content. Example: In /seo-local-gijon/ Expert Tasks, link "estrategia de contenido" to `/posicionamiento-web-asturias/` with anchor "posicionamiento web en Asturias".
- **Effort:** 2 hours

### M3. Fix Broken Blog Images

**4 of 6 blog images return 404:**
- `precio-SEO-asturias.webp` — create or rename file
- `google-my-business-guia-pymempresas-asturias.webp` — create or rename file
- `posicionamiento web gijon.webp` — **spaces in filename!** Rename to `posicionamiento-web-gijon.webp` and update blog frontmatter
- `seo-local-asturias.webp` — create or rename file
- **Effort:** 1 hour

### M4. Fix Broken #portfolio Links

**Appears on:** Homepage CTA, service page CTAs. No `#portfolio` anchor exists on any page.

**Options:**
- Create a portfolio section on the homepage
- Link to a dedicated `/portfolio/` page with real work examples
- Remove the button if no portfolio content is available
- **Effort:** 30 minutes (remove) to 4 hours (create portfolio)

### M5. Add Google Maps Embed

Add a Google Maps iframe on:
- Contact page (primary location)
- Homepage footer
- **Effort:** 15 minutes

### M6. Add width/height to All Blog Images

**Components affected:** ArticleHero, ArticleCard, FeaturedCard, AuthorCard.

Without explicit dimensions, images cause CLS on blog pages (~0.05–0.15 extra).
- **Effort:** 30 minutes

### M7. Collect + Publish Real Testimonials

**Current:** 3 testimonials with generic names and no verifiable business details. "95% satisfacción" stat without source.

**Action:**
- Reach out to past clients for permission to publish names and companies
- Create `aggregateRating` schema with real review count and rating
- Add `Review` schema for individual testimonials
- Embed Google Reviews widget
- **Effort:** 2–4 hours (outreach) + 2 hours (implementation)

### M8. Standardize Pricing Presentation

**Current:** "Básico" vs "Esencial", different price points, no explanation of differences between service types.

**Fix:** Add a brief comparison or methodology note explaining why posicionamiento-web (397–1,197€) costs more than seo-local (297–897€). Unify category naming.
- **Effort:** 1 hour

---

## LOW — Backlog

### L1. Publish 2–3 Blog Posts per Month

**Current:** 6 posts total for an SEO agency. Insufficient topical authority.

**Priority topics from GSC data:**
- "cuánto cuesta SEO en Asturias" (22 imp, pos 48–50)
- "SEO local para pymes" (existing page at pos 37)
- "agencia SEO Oviedo" (68–73 imp, pos 73)
- "diseño web Gijón precio" (high intent, low competition)
- **Ongoing effort**

### L2. Create YouTube Channel

**Impact:** YouTube mentions have strongest correlation (~0.737) with AI citations. Zero video content exists.

**Initial content:** 5–10 videos on "SEO tips for Asturias businesses", "Cómo aparecer en Google Maps", "n8n automation tutorial".
- **Effort:** 2 hours setup + ongoing

### L3. Create Company LinkedIn Page

**Impact:** LinkedIn presence correlates with AI citation. Currently only individual profile exists.

**Action:** Create company page, link from website footer and schema `sameAs`.
- **Effort:** 30 minutes

### L4. Fix Horizontal Overflow on /posicionamiento-web-asturias/

Process/timeline section overflows 354px on mobile. Cards do not stack vertically at 375px viewport.
- **Effort:** 1 hour (CSS fix)

### L5. Implement IndexNow Protocol

Submit URL changes to Bing, Yandex, Seznam automatically.
- **Effort:** 1 hour (API key + build hook)

### L6. Conduct Original Research

**Single highest-impact content investment for AI citation.**

**Proposal:** "Estado del Marketing Digital en PYMES de Asturias 2026" — survey 50–100 local businesses, analyze results, publish as report page with methodology, sample size, and unique findings.
- **Effort:** 2–3 weeks (survey design, outreach, analysis, writing)

---

## Implementation Sequence

### Week 1 (Critical fixes)

```
Day 1: C3 (author photo) + C5 (security headers) + C6 (404 page) + C7 (sitemap) + C8 (OG image)
Day 2: C1 (cookie banner) + C4 (Oviedo address) + C2 (schema @id — BaseLayout part)
Day 3: C2 (schema @id — all service pages) + H9 (sameAs) + H10 (missing schema types)
Day 4: H5 (fonts) + H6 (preload) + H8 (title tags)
Day 5: H1 start (Oviedo page differentiation)
```

### Week 2 (High priority)

```
Day 1: H1 complete (Oviedo unique content) + H3 (FAQPage schema on remaining pages)
Day 2: H2 (Team/About page) + H4 (complete LocalBusiness schemas)
Day 3: H7 (Avilés landing page) + M4 (fix #portfolio links)
Day 4: M3 (fix broken blog images) + M6 (blog image dimensions)
Day 5: M5 (Google Maps embed) + review/catch-up
```

### Week 3–4 (Medium priority)

```
M1 (homepage content) → M2 (internal linking) → M7 (testimonials) → M8 (pricing)
```

### Ongoing

```
L1 (blog posts) → L2 (YouTube) → L3 (LinkedIn company page)
L4 (overflow fix) → L5 (IndexNow) → L6 (original research)
```

---

## Expected Impact Timeline

| Timeframe | Expected Change |
|-----------|----------------|
| 1–2 weeks | Schema fixed → GSC rich results eligible. Security headers added. 404 fixed. |
| 2–4 weeks | Mobile LCP passes CWV (font + image fixes). Cookie banner no longer blocks users. |
| 1–2 months | Oviedo content differentiation → de-duplication penalty lifted. Avilés page indexed. Blog growing. |
| 3–6 months | E-E-A-T signals (team page, testimonials, reviews) → ranking improvements on competitive terms. Original research citable by AI. |

---

## Files Modified Summary

| File | Changes |
|------|---------|
| `src/layouts/BaseLayout.astro` | Add LocalBusiness to @graph, add preload hints |
| `src/pages/index.astro` | Fix provider @id, fix sameAs, add location to title |
| `src/pages/seo-local-gijon.astro` | Fix provider @id, complete LocalBusiness |
| `src/pages/seo-local-oviedo.astro` | **Fix addressLocality (critical!)**, fix provider @id |
| `src/pages/seo-gijon.astro` | Fix provider @id |
| `src/pages/posicionamiento-web-asturias.astro` | Fix provider @id, fix horizontal overflow |
| `src/pages/inteligencia-artificial-empresas.astro` | Fix relative URLs to absolute, fix provider @id, fix title |
| `src/pages/formacion-ia-empresas.astro` | Remove duplicate Organization, fix lat/lng types |
| `src/pages/automatizaciones-con-ia.astro` | Add WebPage + FAQPage + serviceType, fix provider @id |
| `src/pages/google-negocios.astro` | Fix provider @id, add LocalBusiness |
| `src/pages/consultoria.astro` | Add WebPage + BreadcrumbList, fix provider @id |
| `src/pages/contacto.astro` | Add mainEntity to ContactPage |
| `src/pages/diseno-web-gijon.astro` | Add WebPage + BreadcrumbList |
| `src/pages/sitemap.xml.ts` | Add seo-gijon/ to pages array, fix lastmod logic |
| `src/pages/blog.astro` | Fix title to include location |
| `src/pages/[slug].astro` | Add author.url and author.image with absolute URLs |
| `src/styles/global.css` | Replace 42 @font-face with 3 Latin-only woff2 |
| `src/components/CookieBanner.astro` | Change from full-screen overlay to bottom bar |
| `src/components/SEO.astro` | Update default OG image to .jpg |
| `src/content/config.ts` | Add `updatedAt` to servicios + blog schemas |
| `public/images/` | Convert author PNG to WebP, create missing blog images, create og-default.jpg |
| `.htaccess` (root) | Add security headers, 404 ErrorDocument, charset |

---

*Action plan generated 2026-05-15. Prioritization based on: real GSC data, live site testing, 8 specialist audits. Review after each implementation phase.*
