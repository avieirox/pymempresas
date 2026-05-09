# SEO Action Plan: pymempresas.com

**Date:** 2026-05-09
**Overall Score:** 62/100

---

## CRITICAL — Fix Immediately (blocks indexing or causes penalties)

### 1. Add www → non-www 301 redirect
**Impact:** Prevents duplicate content, consolidates link equity.
**Effort:** 5 minutes
**How:** Add to `.htaccess`:
```apache
RewriteEngine On
RewriteCond %{HTTP_HOST} ^www\.pymempresas\.com [NC]
RewriteRule ^(.*)$ https://pymempresas.com/$1 [L,R=301]
```

### 2. De-duplicate Gijón and Oviedo landing pages
**Impact:** Eliminates doorway page risk. ~80% content overlap currently.
**Effort:** 4-6 hours
**How:**
- Add unique local case studies to each city page
- Add city-specific market data (search volume, competition level)
- Rewrite FAQ questions to be city-specific, not just city-name-swapped
- Add unique testimonials from each city
- Add neighborhood-specific content blocks
- Target: <40% content overlap between pages

### 3. Fix phone number on contact page
**Impact:** NAP consistency is #1 local ranking factor.
**Effort:** 2 minutes
**How:** On `/contacto/`, remove +34 697 711 344. Use only +34 697 71 13 44 (matches schema and all other pages).

### 4. Consolidate GBP share links
**Impact:** Conflicting GBP references weaken entity identity.
**Effort:** 10 minutes
**How:** Check both share links (`PbUpboFKMelaHcNgg` and `HdcSxhMtHLihuMzAg`). Keep the active one, remove the other from both schema `sameAs` and visible text.

### 5. Add security headers
**Impact:** Protects users, signals trust to Google.
**Effort:** 5 minutes
**How:** Add to `.htaccess`:
```apache
Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains"
Header always set X-Frame-Options "SAMEORIGIN"
Header always set X-Content-Type-Options "nosniff"
Header always set Referrer-Policy "strict-origin-when-cross-origin"
```

---

## HIGH — Fix Within 1 Week (significantly impacts rankings)

### 6. Create og-default.jpg
**Impact:** Fixes broken social previews on all pages without custom OG image.
**Effort:** 30 minutes
**How:** Replace `/public/og-default.svg` with `/public/og-default.jpg` (1200×630px, ~30-50KB). Update references in `SEO.astro` and `BaseLayout.astro`.

### 7. Extract critical CSS, defer rest
**Impact:** Reduces LCP by ~80ms on slow CPUs. HTML shrinks from 101KB to ~30KB.
**Effort:** 2-4 hours
**How:** Inline only above-the-fold CSS. Load full Tailwind via deferred external stylesheet with `<link rel="preload">` + `<noscript>` fallback.

### 8. Add schema to IA Empresas page
**Impact:** Currently has zero page-level schema — invisible to rich results.
**Effort:** 30 minutes
**How:** Add `Service` + `FAQPage` + `BreadcrumbList` schema matching the pattern used on other service pages. Use `ProfessionalService` type (not `ComputerRepair`).

### 9. Create testimonials/reviews section
**Impact:** Builds trust, enables review stars in SERPs via aggregateRating schema.
**Effort:** 2-3 hours
**How:**
- Add 3-5 real client testimonials with full names and permission
- Add `aggregateRating` to ProfessionalService schema
- Display on homepage and service pages
- Link to GBP reviews as social proof

### 10. Fix blog schema
**Impact:** Blog posts eligible for Article rich results.
**Effort:** 30 minutes
**How:** Add to blog post template: `@id`, `image`, `publisher`, `mainEntityOfPage`, `dateModified`. Fix author type mismatch (Organization vs Person for Arturo Vieiros Garcia).

### 11. Create and link social media profiles
**Impact:** Strengthens entity identity, adds sameAs signals.
**Effort:** 1-2 hours
**How:**
- Create LinkedIn company page (minimum)
- Add to footer, contact page, and schema `sameAs`
- Optional: Facebook, Instagram, Twitter/X

### 12. Fix broken schema @id references
**Impact:** Dead `provider` references on all service pages mean entity linking is broken.
**Effort:** 1 hour
**How:** Either embed the Organization/ProfessionalService node with its @id on every service page, or replicate the referenced entity inline within each page's JSON-LD graph.

---

## MEDIUM — Fix Within 1 Month (optimization opportunity)

### 13. Remove noindex pages from sitemap
**Effort:** 5 minutes
**How:** Exclude `/aviso-legal/` and `/politica-privacidad/` from sitemap generation (both have `noindex` meta robots).

### 14. Create custom 404 page
**Effort:** 1 hour
**How:** Create `src/pages/404.astro` with branded design, navigation links, search suggestion, and CTA to consultoría.

### 15. Thicken IA Empresas page
**Effort:** 2-3 hours
**How:** Add pricing table, FAQ section, benefits cards, and case studies. Target 1,500+ words. Match structure of other service pages.

### 16. Prune Inter font variants
**Effort:** 30 minutes
**How:** Configure `@fontsource/inter` to load only Latin subset with weights 400, 500, 600, 700. Removes ~200-300KB of unused font files.

### 17. Add Google Maps embed
**Effort:** 10 minutes
**How:** Embed Google Maps iframe on homepage and `/contacto/` showing Spaces Coworking location. Add "Get Directions" link.

### 18. Fix duplicate footer cookie link
**Effort:** 5 minutes
**How:** Either create dedicated cookie policy page or merge "Política de Cookies" label into the privacy link to avoid duplicate anchors to same URL.

### 19. Add "Last updated" dates to service pages
**Effort:** 30 minutes
**How:** Display last modified date on each service page. Use actual file modification time rather than blanket date.

### 20. Differentiate sitemap lastmod dates
**Effort:** 1 hour
**How:** Update `src/pages/sitemap.xml.ts` to use per-page last modified dates from content collections or file mtime instead of single hardcoded date.

### 21. Remove unused images from build
**Effort:** 30 minutes
**How:** Audit `public/images/` directory. Remove legacy PNGs not referenced by any page (saves ~8.5MB from build output).

### 22. Add contact details to ContactPage schema
**Effort:** 10 minutes
**How:** Add `telephone`, `email`, and `contactPoint` properties to the ContactPage JSON-LD on `/contacto/`.

### 23. Add author bio to all blog posts
**Effort:** 15 minutes
**How:** Ensure all blog posts use "Arturo Vieiros Garcia" (Person) not "PYMEMPRESAS" (Organization) as author. Display author image on blog cards.

---

## LOW — Backlog (nice to have)

### 24. Add image sitemap
**Effort:** 1-2 hours
**How:** Extend sitemap generation to include `<image:image>` tags for hero images and blog post images.

### 25. Add resource hints
**Effort:** 5 minutes
**How:** Add `<link rel="preload">` for hero image as LCP redundancy.

### 26. Cite statistics with sources
**Effort:** 1-2 hours (content)
**How:** Add inline source links for all factual claims (e.g., "Fuente: Google SEO Starter Guide, 2024"). Critical for AI citation readiness.

### 27. Refine GeoCoordinates precision
**Effort:** 2 minutes
**How:** Update schema `geo` to 5+ decimal places for exact coworking location.

### 28. Build Tier 1 citations
**Effort:** Ongoing
**How:** Claim/optimize listings on Yelp, Páginas Amarillas, Infoempresa, Directorio de Empresas Asturias. Ensure identical NAP on all.

### 29. Increase blog cadence
**Effort:** Ongoing
**How:** Publish 1-2 posts/month targeting local keywords from GSC data in `docs/INTERLINKING.md`. Current: 2 posts in 16 months.

### 30. Create dedicated cookie policy page
**Effort:** 30 minutes
**How:** Create `/politica-cookies/` page with cookie usage details. Update footer link.

---

## Summary

| Priority | Count | Est. Total Effort |
|----------|-------|-------------------|
| CRITICAL | 5 | ~5 hours |
| HIGH | 7 | ~10 hours |
| MEDIUM | 11 | ~8 hours |
| LOW | 7 | ~5 hours + ongoing |
| **Total** | **30** | **~28 hours + ongoing** |

### Quickest Wins (Under 30 minutes total)

1. www redirect (5 min)
2. Fix phone number (2 min)
3. GBP link consolidation (10 min)
4. Security headers (5 min)
5. Remove noindex from sitemap (5 min)

**These 5 fixes alone address 3 CRITICAL + 1 HIGH + 1 MEDIUM issue in under 30 minutes.**
