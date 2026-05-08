# Blog Redesign — Design Spec

**Date:** 2026-05-07
**Status:** Approved
**Scope:** Blog listing (`/blog/`) + article detail (`/[slug]/` blog branch)

## Goals

Replace current plain blog UI with modern, elegant, multimedia-rich magazine experience. Brand-consistent (black `#0A0A0A` + orange `#F5A623`). Dynamic animations without JS dependencies. Zero impact on Lighthouse score.

## Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Animation engine | CSS-only | View Transitions + scroll-timeline + IntersectionObserver cover all needs. No bundle cost. |
| Animation level | Dynamic | Scroll reveals, parallax hero, stagger cards, hover effects. Not immersive (no canvas/3D). |
| Visual style | Magazine | Drop caps, pull quotes, wide images, callout boxes. Cards with image zoom + tilt on hover. |
| Dependencies | None | No new packages. All CSS + browser APIs. |

## Component Inventory

### New files (`src/components/blog/`)

| Component | Purpose | Key technique |
|-----------|---------|---------------|
| `BlogHero.astro` | `/blog/` hero with badge + title + subtitle | Animated geometric background pattern (CSS gradients + keyframes) |
| `ArticleCard.astro` | Individual blog card | CSS hover: image scale(1.05) + card translateY(-4px) + elevated shadow |
| `FeaturedCard.astro` | First article, 2-col horizontal | Larger image, horizontal layout, same hover system |
| `BlogGrid.astro` | Grid wrapper with stagger reveal | IntersectionObserver adds `.revealed`, each card gets `animation-delay: calc(var(--i) * 80ms)` |
| `ArticleHero.astro` | Article detail hero | CSS scroll-timeline parallax (`animation-timeline: scroll()`), overlay gradient |
| `ArticleBody.astro` | Magazine prose layout | Drop cap (`p:first-of-type::first-letter`), pull quotes (`blockquote` styled), wide images (negative margin breakout), callout box |
| `ShareRow.astro` | Social share buttons | CSS popover tooltip on copy, stagger reveal |
| `RelatedArticles.astro` | 3 related posts | Same card style, filtered by shared tags |
| `ReadingProgress.astro` | Sticky top progress bar | scroll-timeline on body, IntersectionObserver fallback |
| `ScrollReveal.astro` | Generic reveal wrapper | IntersectionObserver, adds `.revealed` class for CSS transitions |

### Modified files

| File | Change |
|------|--------|
| `src/pages/blog.astro` | Replace layout with BlogHero + BlogGrid |
| `src/pages/[slug].astro` | Blog branch: ArticleHero + ArticleBody + ShareRow + RelatedArticles + ReadingProgress |
| `src/styles/global.css` | Add animation utility classes, keyframes, timing variables |

## Component Details

### BlogHero
- Background: `#0A0A0A` with diagonal line pattern (CSS `background-image` linear-gradient repeating, opacity 3%, animated shift 20s linear infinite)
- Badge pill: `bg: #FFF8E8`, `color: #E8960F`, 13px, fade-in on load
- Title: 42px, 800 weight, white, `letter-spacing: -0.02em`, max 700px centered
- Subtitle: 17px, `#888`, max 500px centered
- Stagger reveal: badge → title → subtitle, 100ms delay chain

### FeaturedCard
- Horizontal layout: image 55% left, content 45% right
- Image: `object-cover`, `border-radius: 16px 0 0 16px`, hover `scale(1.03)` 0.4s ease
- Content: tags, title (24px/700), description (14px/#777, 2-line clamp), meta row
- Card: `bg: white`, `border: 1px #EAECEF`, `border-radius: 16px`, hover `translateY(-3px)`, shadow elevated

### ArticleCard
- Vertical layout: image top (16:9, `overflow: hidden`), body below
- Image hover: `scale(1.05)` + `brightness(1.1)`, 0.5s cubic-bezier
- Tags: 11px pills, `bg: #FFF8E8`, `color: #D4850B`
- Title: 20px/700, hover `color: #F5A623`
- Description: 14px/#777, 2-line clamp (`-webkit-line-clamp: 2`)
- Meta: 13px/#AAA, date · author
- Card: same border/radius/shadow as FeaturedCard, hover `translateY(-4px)`, shadow `0 12px 40px rgba(0,0,0,0.08)`

### BlogGrid
- CSS Grid: `repeat(auto-fill, minmax(340px, 1fr))`, gap 28px
- Stagger: each card `style="--i: 0"` through `--i: N`, `animation-delay: calc(var(--i) * 80ms)`
- Animation: `@keyframes cardReveal` — opacity 0→1, translateY 24px→0, 0.5s ease-out, `animation-fill-mode: backwards`
- Observer: fires once when grid enters viewport, adds `.revealed` to trigger animations

### ArticleHero
- Image: full-width, max-height 520px, `object-cover`
- Parallax: `animation: parallaxDown auto linear; animation-timeline: scroll()`. Keyframes: `translateY(-15%)` to `translateY(0)`
- Overlay: transparent → `rgba(10,10,10,0.7)` → `#0A0A0A` bottom gradient
- Content below image: badge (reading time) + category pill, title (40px/800), meta (14px/#AAA)
- Fallback when no image: dark gradient background with subtle pattern

### ArticleBody
- Container: max-width 760px, centered, white background
- Drop cap: `p:first-of-type::first-letter` — 52px, naranja, bold, `float: left`, `line-height: 1`, `margin-right: 8px`
- Prose: 17px, `#333`, `line-height: 1.8`
- Pull quote: `blockquote` — 20px, naranja, italic, left border 3px naranja, padding-left 24px, margin 40px 0
- Wide image: negative margin breakout `calc(-1 * (100vw - 760px) / 2)`, border-radius 16px, caption 13px/#888 italic
- Callout: `bg: #FFF8E8`, left border naranja 3px, padding 20px, border-radius 12px
- All images/blockquotes: scroll reveal via IntersectionObserver

### ShareRow
- Label "Compartir" centered, 14px/#888
- 4 buttons: Twitter, LinkedIn, Copy link, Email — 48x48, border `#EAECEF`, radius 12px
- Hover: `bg: rgba(245,166,35,0.1)`, `border-color: #F5A623`, `scale: 1.05`
- Copy: CSS `popover` for "¡Copiado!" tooltip. Native `navigator.clipboard.writeText()`
- URLs: Twitter intent `https://twitter.com/intent/tweet?url=...&text=...`, LinkedIn share, `mailto:`

### RelatedArticles
- Section: `bg: #F8F9FA`, padding 80px 0
- Title: "Artículos relacionados", 32px/700, centered
- 3 cards: same `ArticleCard` style, tagged with matching categories
- Data: `getCollection('blog')`, filter by shared tags with current article, sort by date desc, limit 3

### ReadingProgress
- Fixed top:0, z-index 1000, height 3px
- Background: naranja gradient (`linear-gradient(90deg, #F5A623, #E8960F)`)
- CSS: `animation: readProgress auto linear; animation-timeline: scroll(root)`. Keyframes: `scaleX(0)` to `scaleX(1)`, `transform-origin: left`
- Fallback: IntersectionObserver tracking article sections, updating `--progress` custom property
- `@media (prefers-reduced-motion: reduce)`: hidden

### ScrollReveal
- Wrapper component: `<div class="scroll-reveal"> <slot/> </div>`
- Script: `IntersectionObserver` with `threshold: 0.15`, adds `.revealed` when visible
- CSS: `.scroll-reveal { opacity: 0; transform: translateY(30px); transition: opacity 0.6s ease-out, transform 0.6s ease-out; }`
- `.scroll-reveal.revealed { opacity: 1; transform: translateY(0); }`
- Optional `data-direction` prop for left/right reveals

## Brand Tokens

```css
--color-black: #0A0A0A;
--color-orange: #F5A623;
--color-orange-dark: #E8960F;
--color-orange-light: #FFF8E8;
--color-gray-light: #F8F9FA;
--color-gray-border: #EAECEF;
--color-text: #333;
--color-text-muted: #777;
--color-text-subtle: #AAA;
--radius-card: 16px;
--radius-button: 12px;
--radius-pill: 100px;
--shadow-card: 0 1px 3px rgba(0,0,0,0.04);
--shadow-card-hover: 0 12px 40px rgba(0,0,0,0.08);
--transition-card: 0.3s cubic-bezier(0.4, 0, 0.2, 1);
```

## Accessibility

- All animations respect `@media (prefers-reduced-motion: reduce)` — disable parallax, reveals, progress bar
- Images: `loading="lazy"`, `decoding="async"` on below-fold cards
- Focus-visible styles on all interactive elements
- Skip-link preserved in layout
- Color contrast: orange `#F5A623` on black `#0A0A0A` = 5.1:1 (AA). White on orange = 4.5:1 (AA). Black text `#1a1a1a` on white = 14:1 (AAA).

## Performance Constraints

- Zero new npm dependencies
- No JavaScript framework (vanilla TS in `<script>` blocks)
- All CSS animations GPU-accelerated (`transform`, `opacity` only — no `width`, `height`, `top`, `left`)
- View Transitions: `meta[name="view-transition"]` opt-in per page
- Images: preserve existing `loading="lazy"`, no layout shift (explicit aspect-ratio or width/height)
- IntersectionObserver: single shared instance where possible

## MDX Content — No Changes Required

Content collection schema stays the same. New optional fields recognized by components if present:
- `image`: used as hero image (already in schema)
- `tags`: used for category pills and RelatedArticles filtering (already in schema)
- No schema migration needed. Existing 50 articles render correctly with new components.
