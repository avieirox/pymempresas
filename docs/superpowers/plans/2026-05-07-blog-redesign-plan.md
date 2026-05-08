# Blog Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace plain blog UI with 10 modern magazine-style components — CSS-only animations, brand-consistent, zero dependencies.

**Architecture:** New components under `src/components/blog/`. Each component scoped with its own `<style>` (no `is:global` except where keyframes need sharing). Shared animation primitives (keyframes, reveal classes) go in `global.css`. Two existing pages (`blog.astro`, `[slug].astro`) updated to consume new components.

**Tech Stack:** Astro 5, Tailwind CSS 4 (Vite plugin), vanilla TypeScript in `<script>` blocks. No new npm packages.

---

### Task 1: Foundation — Animation tokens and keyframes in global.css

**Files:**
- Modify: `src/styles/global.css`

- [ ] **Step 1: Add blog brand tokens and animation keyframes to global.css**

Add below the existing `@theme` block (after `--font-sans` line, inside `@theme`):

```css
@theme {
  --color-black: #0A0A0A;
  --color-card: #111111;
  --color-orange: #F5A623;
  --color-orange-dark: #E89B1F;
  --color-orange-light: #FFF8E8;
  --color-gray-light: #F5F5F5;
  --color-gray-border: #EAECEF;
  --color-text: #333333;
  --color-text-muted: #777777;
  --color-text-subtle: #AAAAAA;
  --color-white: #FFFFFF;
  --font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", "Helvetica Neue", Arial, sans-serif;
}
```

Add at the end of `global.css`:

```css
/* ============================================
   Blog animation utilities
   ============================================ */

/* Scroll reveal base */
.scroll-reveal {
  opacity: 0;
  transform: translateY(30px);
  transition: opacity 0.6s ease-out, transform 0.6s ease-out;
}
.scroll-reveal.revealed {
  opacity: 1;
  transform: translateY(0);
}

/* Stagger children — each child needs --i set inline */
.stagger-children > * {
  opacity: 0;
  transform: translateY(24px);
}
.stagger-children.revealed > * {
  animation: cardReveal 0.5s ease-out forwards;
  animation-delay: calc(var(--i, 0) * 80ms);
}

@keyframes cardReveal {
  from {
    opacity: 0;
    transform: translateY(24px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Geometric background shift (BlogHero) */
@keyframes bgShift {
  from { background-position: 0 0; }
  to { background-position: 60px 60px; }
}

/* Parallax via scroll-timeline (ArticleHero) */
@keyframes parallaxDown {
  from { transform: translateY(-12%); }
  to { transform: translateY(0); }
}

/* Reading progress bar */
@keyframes readProgress {
  from { transform: scaleX(0); }
  to { transform: scaleX(1); }
}
.reading-progress {
  transform-origin: left;
  animation: readProgress auto linear;
  animation-timeline: scroll(root);
}

/* Drop cap — applies to first paragraph in article body */
.article-prose > p:first-of-type::first-letter {
  font-size: 52px;
  font-weight: 700;
  color: #F5A623;
  float: left;
  line-height: 1;
  margin-right: 10px;
  margin-top: 4px;
}

/* Pull quote */
.article-prose blockquote {
  font-size: 20px;
  color: #F5A623;
  font-style: italic;
  border-left: 3px solid #F5A623;
  padding-left: 24px;
  margin: 40px 0;
  quotes: none;
}
.article-prose blockquote p {
  margin: 0;
}

/* Wide image breakout */
.article-prose img.wide,
.article-prose figure.wide {
  width: calc(100vw - 48px);
  max-width: 1100px;
  margin: 32px calc(-1 * (100vw - 760px) / 2);
  border-radius: 16px;
}
@media (max-width: 860px) {
  .article-prose img.wide,
  .article-prose figure.wide {
    width: 100%;
    margin: 32px 0;
  }
}

/* Callout box */
.article-callout {
  background: #FFF8E8;
  border-left: 3px solid #F5A623;
  padding: 20px 24px;
  border-radius: 0 12px 12px 0;
  margin: 32px 0;
  font-size: 15px;
  color: #333;
  line-height: 1.6;
}
.article-callout a {
  color: #E8960F;
  font-weight: 600;
  text-decoration: underline;
}

/* Reduced motion */
@media (prefers-reduced-motion: reduce) {
  .scroll-reveal {
    opacity: 1;
    transform: none;
    transition: none;
  }
  .stagger-children > * {
    opacity: 1;
    transform: none;
    animation: none;
  }
  .reading-progress {
    display: none;
  }
  .article-prose > p:first-of-type::first-letter {
    font-size: inherit;
    font-weight: inherit;
    color: inherit;
    float: none;
    line-height: inherit;
    margin: 0;
  }
}
```

- [ ] **Step 2: Verify dev server starts**

```bash
npm run dev
```

Check `http://localhost:4321` loads without CSS errors.

- [ ] **Step 3: Commit**

```bash
git add src/styles/global.css
git commit -m "feat: add blog animation tokens, keyframes, and prose styles"
```

---

### Task 2: ScrollReveal wrapper component

**Files:**
- Create: `src/components/blog/ScrollReveal.astro`

- [ ] **Step 1: Create ScrollReveal.astro**

```astro
---
interface Props {
  direction?: 'up' | 'left' | 'right';
  threshold?: number;
  rootMargin?: string;
  class?: string;
}

const {
  direction = 'up',
  threshold = 0.15,
  rootMargin = '0px 0px -50px 0px',
  class: extraClass = '',
} = Astro.props;

const dirMap = {
  up: 'translateY(30px)',
  left: 'translateX(-30px)',
  right: 'translateX(30px)',
};
const initialTransform = dirMap[direction];
---

<div
  class={`scroll-reveal ${extraClass}`}
  style={`transform: ${initialTransform};`}
  data-threshold={String(threshold)}
  data-root-margin={rootMargin}
>
  <slot />
</div>

<script>
  function setupScrollReveal() {
    const elements = document.querySelectorAll('.scroll-reveal:not(.revealed)');
    if (!elements.length) return;

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('revealed');
            observer.unobserve(entry.target);
          }
        });
      },
      {
        threshold: parseFloat(elements[0].getAttribute('data-threshold') || '0.15'),
        rootMargin: elements[0].getAttribute('data-root-margin') || '0px 0px -50px 0px',
      }
    );

    elements.forEach((el) => observer.observe(el));
  }

  // Run on load + after Astro page transitions
  document.addEventListener('astro:page-load', setupScrollReveal);
  setupScrollReveal();
</script>
```

- [ ] **Step 2: Verify build succeeds**

```bash
npm run build
```

- [ ] **Step 3: Commit**

```bash
git add src/components/blog/ScrollReveal.astro
git commit -m "feat: add ScrollReveal wrapper component with IntersectionObserver"
```

---

### Task 3: ArticleCard component

**Files:**
- Create: `src/components/blog/ArticleCard.astro`

- [ ] **Step 1: Create ArticleCard.astro**

```astro
---
export interface Props {
  slug: string;
  title: string;
  description: string;
  image?: string;
  tags?: string[];
  date: Date;
  author: string;
  index?: number;
}

const {
  slug,
  title,
  description,
  image,
  tags = [],
  date,
  author,
  index = 0,
} = Astro.props;

const dateStr = date.toLocaleDateString('es-ES', {
  year: 'numeric',
  month: 'long',
  day: 'numeric',
});
---

<article
  class="blog-card"
  style={`--i: ${index};`}
>
  {image && (
    <div class="blog-card-img-wrap">
      <a href={`/${slug}/`} class="blog-card-img-link">
        <img
          src={image}
          alt={title}
          loading="lazy"
          decoding="async"
          class="blog-card-img"
        />
      </a>
    </div>
  )}
  <div class="blog-card-body">
    {tags.length > 0 && (
      <div class="blog-card-tags">
        {tags.slice(0, 3).map((tag) => (
          <span class="blog-tag">{tag}</span>
        ))}
      </div>
    )}
    <h2 class="blog-card-title">
      <a href={`/${slug}/`}>{title}</a>
    </h2>
    <p class="blog-card-desc">{description}</p>
    <div class="blog-card-meta">
      <time datetime={date.toISOString()}>{dateStr}</time>
      <span aria-hidden="true">·</span>
      <span>{author}</span>
    </div>
  </div>
</article>

<style>
  .blog-card {
    background: #fff;
    border: 1px solid #EAECEF;
    border-radius: 16px;
    overflow: hidden;
    transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1),
                box-shadow 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  }
  .blog-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.08);
  }

  .blog-card-img-wrap {
    overflow: hidden;
    aspect-ratio: 16 / 9;
    background: #F0F1F3;
  }
  .blog-card-img-link {
    display: block;
    width: 100%;
    height: 100%;
  }
  .blog-card-img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.5s cubic-bezier(0.4, 0, 0.2, 1),
                filter 0.5s cubic-bezier(0.4, 0, 0.2, 1);
  }
  .blog-card:hover .blog-card-img {
    transform: scale(1.05);
    filter: brightness(1.1);
  }

  .blog-card-body {
    padding: 24px;
  }

  .blog-card-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin-bottom: 12px;
  }
  .blog-tag {
    background: #FFF8E8;
    color: #D4850B;
    font-size: 11px;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 100px;
    letter-spacing: 0.01em;
  }

  .blog-card-title {
    margin: 0 0 10px;
    font-size: 20px;
    font-weight: 700;
    line-height: 1.3;
    letter-spacing: -0.01em;
  }
  .blog-card-title a {
    color: #1a1a1a;
    text-decoration: none;
    transition: color 0.15s ease;
  }
  .blog-card-title a:hover {
    color: #F5A623;
  }

  .blog-card-desc {
    color: #777;
    font-size: 14px;
    line-height: 1.55;
    margin: 0 0 16px;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }

  .blog-card-meta {
    color: #AAA;
    font-size: 13px;
    display: flex;
    align-items: center;
    gap: 8px;
  }
</style>
```

- [ ] **Step 2: Verify build**

```bash
npm run build
```

- [ ] **Step 3: Commit**

```bash
git add src/components/blog/ArticleCard.astro
git commit -m "feat: add ArticleCard with hover zoom and brand styling"
```

---

### Task 4: FeaturedCard component

**Files:**
- Create: `src/components/blog/FeaturedCard.astro`

- [ ] **Step 1: Create FeaturedCard.astro**

```astro
---
import type { Props as CardProps } from './ArticleCard.astro';

type Props = CardProps;
const { slug, title, description, image, tags = [], date, author } = Astro.props;

const dateStr = date.toLocaleDateString('es-ES', {
  year: 'numeric', month: 'long', day: 'numeric',
});
---

<article class="featured-card">
  {image && (
    <a href={`/${slug}/`} class="featured-img-wrap">
      <img
        src={image}
        alt={title}
        class="featured-img"
        loading="eager"
        decoding="async"
      />
    </a>
  )}
  <div class="featured-body">
    {tags.length > 0 && (
      <div class="featured-tags">
        {tags.slice(0, 3).map((tag) => (
          <span class="featured-tag">{tag}</span>
        ))}
      </div>
    )}
    <h2 class="featured-title">
      <a href={`/${slug}/`}>{title}</a>
    </h2>
    <p class="featured-desc">{description}</p>
    <div class="featured-meta">
      <time datetime={date.toISOString()}>{dateStr}</time>
      <span aria-hidden="true">·</span>
      <span>{author}</span>
    </div>
  </div>
</article>

<style>
  .featured-card {
    display: grid;
    grid-template-columns: 1.15fr 1fr;
    background: #fff;
    border: 1px solid #EAECEF;
    border-radius: 16px;
    overflow: hidden;
    transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1),
                box-shadow 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    grid-column: 1 / -1;
  }
  .featured-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.08);
  }

  .featured-img-wrap {
    overflow: hidden;
    aspect-ratio: 16 / 9;
    background: #F0F1F3;
    display: block;
  }
  .featured-img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.5s cubic-bezier(0.4, 0, 0.2, 1);
  }
  .featured-card:hover .featured-img {
    transform: scale(1.03);
  }

  .featured-body {
    padding: 36px 32px;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }

  .featured-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin-bottom: 14px;
  }
  .featured-tag {
    background: #FFF8E8;
    color: #D4850B;
    font-size: 11px;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 100px;
  }

  .featured-title {
    margin: 0 0 12px;
    font-size: 26px;
    font-weight: 700;
    line-height: 1.25;
    letter-spacing: -0.02em;
  }
  .featured-title a {
    color: #1a1a1a;
    text-decoration: none;
    transition: color 0.15s ease;
  }
  .featured-title a:hover {
    color: #F5A623;
  }

  .featured-desc {
    color: #777;
    font-size: 15px;
    line-height: 1.6;
    margin: 0 0 18px;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }

  .featured-meta {
    color: #AAA;
    font-size: 13px;
    display: flex;
    align-items: center;
    gap: 8px;
  }

  @media (max-width: 700px) {
    .featured-card {
      grid-template-columns: 1fr;
      grid-column: auto;
    }
    .featured-body {
      padding: 24px;
    }
    .featured-title {
      font-size: 22px;
    }
  }
</style>
```

- [ ] **Step 2: Verify build**

```bash
npm run build
```

- [ ] **Step 3: Commit**

```bash
git add src/components/blog/FeaturedCard.astro
git commit -m "feat: add FeaturedCard horizontal card for first article"
```

---

### Task 5: BlogHero component

**Files:**
- Create: `src/components/blog/BlogHero.astro`

- [ ] **Step 1: Create BlogHero.astro**

```astro
---
interface Props {
  badge?: string;
  title?: string;
  subtitle?: string;
}

const {
  badge = 'Blog',
  title = 'Artículos y Recursos',
  subtitle = 'SEO, marketing digital, IA y automatizaciones para hacer crecer tu empresa en Asturias',
} = Astro.props;
---

<section class="blog-hero">
  <div class="blog-hero-inner">
    <span class="blog-hero-badge">{badge}</span>
    <h1 class="blog-hero-title">{title}</h1>
    <p class="blog-hero-subtitle">{subtitle}</p>
  </div>
</section>

<style>
  .blog-hero {
    width: 100%;
    padding: 120px 20px 80px;
    background-color: #0A0A0A;
    background-image:
      repeating-linear-gradient(
        45deg,
        transparent,
        transparent 40px,
        rgba(245, 166, 35, 0.02) 40px,
        rgba(245, 166, 35, 0.02) 42px
      ),
      repeating-linear-gradient(
        -45deg,
        transparent,
        transparent 40px,
        rgba(245, 166, 35, 0.02) 40px,
        rgba(245, 166, 35, 0.02) 42px
      );
    animation: bgShift 20s linear infinite;
    position: relative;
    overflow: hidden;
  }

  .blog-hero-inner {
    max-width: 700px;
    margin: 0 auto;
    text-align: center;
    position: relative;
    z-index: 1;
  }

  .blog-hero-badge {
    display: inline-block;
    background: #FFF8E8;
    color: #E8960F;
    font-size: 13px;
    font-weight: 600;
    padding: 6px 18px;
    border-radius: 100px;
    margin-bottom: 20px;
    letter-spacing: 0.02em;
    animation: heroFadeIn 0.5s ease-out both;
  }

  .blog-hero-title {
    color: #fff;
    font-size: clamp(32px, 5vw, 48px);
    font-weight: 800;
    margin: 0 0 16px;
    letter-spacing: -0.02em;
    line-height: 1.15;
    animation: heroFadeIn 0.5s 0.1s ease-out both;
  }

  .blog-hero-subtitle {
    color: #888;
    font-size: clamp(16px, 2vw, 18px);
    max-width: 520px;
    margin: 0 auto;
    line-height: 1.6;
    animation: heroFadeIn 0.5s 0.2s ease-out both;
  }

  @keyframes heroFadeIn {
    from {
      opacity: 0;
      transform: translateY(16px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  @media (max-width: 768px) {
    .blog-hero {
      padding: 100px 20px 60px;
    }
  }
</style>
```

- [ ] **Step 2: Verify build**

```bash
npm run build
```

- [ ] **Step 3: Commit**

```bash
git add src/components/blog/BlogHero.astro
git commit -m "feat: add BlogHero with animated geometric pattern"
```

---

### Task 6: BlogGrid component

**Files:**
- Create: `src/components/blog/BlogGrid.astro`

- [ ] **Step 1: Create BlogGrid.astro**

```astro
---
import ScrollReveal from './ScrollReveal.astro';
---

<div class="blog-grid-wrap">
  <ScrollReveal threshold={0.1} rootMargin="0px 0px -40px 0px">
    <div class="blog-grid stagger-children">
      <slot />
    </div>
  </ScrollReveal>
</div>

<style>
  .blog-grid-wrap {
    width: 100%;
    padding: 0 20px 80px;
    background: #F8F9FA;
  }
  .blog-grid {
    max-width: 1100px;
    margin: 0 auto;
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
    gap: 28px;
  }

  @media (max-width: 768px) {
    .blog-grid {
      grid-template-columns: 1fr;
    }
    .blog-grid-wrap {
      padding: 0 20px 60px;
    }
  }
</style>
```

- [ ] **Step 2: Verify build**

```bash
npm run build
```

- [ ] **Step 3: Commit**

```bash
git add src/components/blog/BlogGrid.astro
git commit -m "feat: add BlogGrid with stagger reveal grid layout"
```

---

### Task 7: Rewrite /blog/ page with new components

**Files:**
- Modify: `src/pages/blog.astro`

- [ ] **Step 1: Replace blog.astro**

```astro
---
import { getCollection } from 'astro:content';
import BaseLayout from '../layouts/BaseLayout.astro';
import BlogHero from '../components/blog/BlogHero.astro';
import BlogGrid from '../components/blog/BlogGrid.astro';
import FeaturedCard from '../components/blog/FeaturedCard.astro';
import ArticleCard from '../components/blog/ArticleCard.astro';
import FinalCTA from '../components/FinalCTA.astro';
import { SITE } from '../lib/constants';

const posts = await getCollection('blog');
const sorted = posts.sort((a, b) => b.data.date.getTime() - a.data.date.getTime());

const blogListingSchema = {
  '@context': 'https://schema.org',
  '@type': 'Blog',
  name: 'Blog de PYMEMPRESAS',
  description: 'Artículos sobre SEO, marketing digital, IA y automatizaciones para empresas.',
  url: `${SITE.url}/blog/`,
  blogPost: sorted.map((p) => ({
    '@type': 'BlogPosting',
    headline: p.data.title,
    description: p.data.description,
    datePublished: p.data.date.toISOString(),
    url: `${SITE.url}/${p.slug}/`,
    author: { '@type': 'Organization', name: p.data.author },
  })),
};
---

<BaseLayout
  metaTitle="Blog — PYMEMPRESAS"
  metaDescription="Artículos sobre SEO, marketing digital, IA y automatizaciones para empresas en Asturias."
  canonicalURL={`${SITE.url}/blog/`}
  schema={blogListingSchema}
>
  <BlogHero />

  {sorted.length > 0 ? (
    <BlogGrid>
      {sorted.map((post, i) =>
        i === 0 ? (
          <FeaturedCard
            slug={post.slug}
            title={post.data.title}
            description={post.data.description}
            image={post.data.image}
            tags={post.data.tags}
            date={post.data.date}
            author={post.data.author}
          />
        ) : (
          <ArticleCard
            index={i}
            slug={post.slug}
            title={post.data.title}
            description={post.data.description}
            image={post.data.image}
            tags={post.data.tags}
            date={post.data.date}
            author={post.data.author}
          />
        )
      )}
    </BlogGrid>
  ) : (
    <section class="blog-empty-section">
      <div class="blog-empty-inner">
        <p class="blog-empty-text">Próximamente publicaremos artículos. ¡Vuelve pronto!</p>
      </div>
    </section>
  )}

  <FinalCTA />
</BaseLayout>

<style>
  .blog-empty-section {
    padding: 80px 20px;
    background: #F8F9FA;
  }
  .blog-empty-inner {
    max-width: 600px;
    margin: 0 auto;
    text-align: center;
  }
  .blog-empty-text {
    color: #888;
    font-size: 16px;
  }
</style>
```

- [ ] **Step 2: Verify build and check the listing page**

```bash
npm run build && npm run preview
```

Visit `http://localhost:4321/blog/` — verify BlogHero renders, cards grid visible, featured card spans 2 cols.

- [ ] **Step 3: Commit**

```bash
git add src/pages/blog.astro
git commit -m "feat: rewrite /blog/ page with BlogHero, FeaturedCard, and BlogGrid"
```

---

### Task 8: ReadingProgress component

**Files:**
- Create: `src/components/blog/ReadingProgress.astro`

- [ ] **Step 1: Create ReadingProgress.astro**

```astro
---
---

<div class="reading-progress" id="reading-progress" aria-hidden="true"></div>

<script>
  const bar = document.getElementById('reading-progress');
  if (bar && !CSS.supports('animation-timeline', 'scroll()')) {
    // Fallback for browsers without scroll-timeline (Firefox, Safari)
    bar.style.animation = 'none';
    bar.style.transform = 'scaleX(0)';

    function updateProgress() {
      const scrollTop = document.documentElement.scrollTop;
      const scrollHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
      const progress = scrollHeight > 0 ? scrollTop / scrollHeight : 0;
      bar.style.transform = `scaleX(${Math.min(progress, 1)})`;
    }

    let ticking = false;
    document.addEventListener('scroll', () => {
      if (!ticking) {
        requestAnimationFrame(() => {
          updateProgress();
          ticking = false;
        });
        ticking = true;
      }
    }, { passive: true });

    updateProgress();
  }
</script>

<style>
  .reading-progress {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, #F5A623, #E8960F);
    z-index: 1000;
    transform-origin: left;
  }
</style>
```

- [ ] **Step 2: Verify build**

```bash
npm run build
```

- [ ] **Step 3: Commit**

```bash
git add src/components/blog/ReadingProgress.astro
git commit -m "feat: add ReadingProgress bar with scroll-timeline + fallback"
```

---

### Task 9: ArticleHero component

**Files:**
- Create: `src/components/blog/ArticleHero.astro`

- [ ] **Step 1: Create ArticleHero.astro**

```astro
---
import ScrollReveal from './ScrollReveal.astro';

interface Props {
  title: string;
  slug: string;
  image?: string;
  tags?: string[];
  date: Date;
  author: string;
}

const { title, slug, image, tags = [], date, author } = Astro.props;

const safeImageId = slug.replace(/[^a-z0-9-]/g, '');
const dateStr = date.toLocaleDateString('es-ES', {
  year: 'numeric', month: 'long', day: 'numeric',
});
---

<header class="article-hero">
  {image ? (
    <div class="article-hero-img-wrap">
      <img
        src={image}
        alt={title}
        class="article-hero-img"
        decoding="async"
        style={`view-transition-name: article-img-${safeImageId}`}
      />
      <div class="article-hero-overlay" aria-hidden="true"></div>
    </div>
  ) : (
    <div class="article-hero-no-img" aria-hidden="true"></div>
  )}

  <div class="article-hero-content" style={image ? 'margin-top: -80px;' : ''}>
    <ScrollReveal>
      <div class="article-hero-meta-top">
        {tags.length > 0 && (
          <span class="article-hero-category">{tags[0]}</span>
        )}
        <span class="article-hero-divider" aria-hidden="true">·</span>
        <span class="article-hero-date">
          <time datetime={date.toISOString()}>{dateStr}</time>
        </span>
        <span class="article-hero-divider" aria-hidden="true">·</span>
        <span class="article-hero-author">{author}</span>
      </div>
    </ScrollReveal>

    <ScrollReveal>
      <h1 class="article-hero-title">{title}</h1>
    </ScrollReveal>
  </div>
</header>

<style>
  .article-hero {
    position: relative;
    background: #0A0A0A;
  }

  .article-hero-img-wrap {
    position: relative;
    width: 100%;
    max-height: 520px;
    overflow: hidden;
  }
  .article-hero-img {
    width: 100%;
    height: 100%;
    max-height: 520px;
    object-fit: cover;
    display: block;
  }
  @supports (animation-timeline: scroll()) {
    .article-hero-img {
      animation: parallaxDown auto linear;
      animation-timeline: scroll();
    }
  }

  .article-hero-overlay {
    position: absolute;
    inset: 0;
    background: linear-gradient(
      to bottom,
      transparent 40%,
      rgba(10, 10, 10, 0.6) 70%,
      #0A0A0A 100%
    );
  }

  .article-hero-no-img {
    height: 120px;
    background: linear-gradient(
      135deg,
      #111 0%,
      #1a1a1a 50%,
      #111 100%
    );
  }

  .article-hero-content {
    position: relative;
    z-index: 2;
    max-width: 800px;
    margin: 0 auto;
    padding: 0 24px 48px;
  }

  .article-hero-meta-top {
    display: flex;
    align-items: center;
    gap: 10px;
    flex-wrap: wrap;
    margin-bottom: 20px;
    color: #AAA;
    font-size: 14px;
  }
  .article-hero-category {
    background: rgba(245, 166, 35, 0.15);
    color: #F5A623;
    font-size: 12px;
    font-weight: 600;
    padding: 4px 12px;
    border-radius: 100px;
  }
  .article-hero-divider {
    color: #555;
  }
  .article-hero-date,
  .article-hero-author {
    color: #AAA;
  }

  .article-hero-title {
    color: #fff;
    font-size: clamp(28px, 4vw, 42px);
    font-weight: 800;
    line-height: 1.15;
    letter-spacing: -0.02em;
    margin: 0;
    max-width: 760px;
  }

  @media (max-width: 768px) {
    .article-hero-img-wrap,
    .article-hero-img {
      max-height: 320px;
    }
    .article-hero-content {
      margin-top: -40px;
      padding-bottom: 36px;
    }
  }
</style>
```

- [ ] **Step 2: Verify build**

```bash
npm run build
```

- [ ] **Step 3: Commit**

```bash
git add src/components/blog/ArticleHero.astro
git commit -m "feat: add ArticleHero with parallax image and overlay gradient"
```

---

### Task 10: ArticleBody component

**Files:**
- Create: `src/components/blog/ArticleBody.astro`

- [ ] **Step 1: Create ArticleBody.astro**

```astro
---
import ScrollReveal from './ScrollReveal.astro';
---

<ScrollReveal>
  <div class="article-body-wrap">
    <div class="article-prose">
      <slot />
    </div>
  </div>
</ScrollReveal>

<style>
  .article-body-wrap {
    max-width: 760px;
    margin: 0 auto;
    padding: 0 24px;
  }

  .article-prose {
    color: #333;
    font-size: 17px;
    line-height: 1.85;
    background: #fff;
    padding: 60px 0;
  }

  .article-prose :global(h2) {
    font-size: 28px;
    font-weight: 700;
    color: #1a1a1a;
    margin: 48px 0 16px;
    line-height: 1.25;
    letter-spacing: -0.01em;
  }

  .article-prose :global(h3) {
    font-size: 22px;
    font-weight: 700;
    color: #1a1a1a;
    margin: 36px 0 12px;
    line-height: 1.3;
  }

  .article-prose :global(p) {
    margin: 0 0 20px;
  }

  .article-prose :global(a) {
    color: #F5A623;
    text-decoration: underline;
    font-weight: 500;
  }
  .article-prose :global(a:hover) {
    color: #E8960F;
  }

  .article-prose :global(ul),
  .article-prose :global(ol) {
    margin: 0 0 20px;
    padding-left: 24px;
  }
  .article-prose :global(li) {
    margin-bottom: 8px;
  }

  .article-prose :global(strong) {
    font-weight: 700;
    color: #1a1a1a;
  }

  .article-prose :global(img:not(.wide)) {
    border-radius: 12px;
    margin: 24px 0;
    max-width: 100%;
    height: auto;
  }

  .article-prose :global(pre) {
    background: #f5f5f5;
    border-radius: 12px;
    padding: 20px 24px;
    overflow-x: auto;
    font-size: 14px;
    margin: 24px 0;
  }

  .article-prose :global(code) {
    background: #f0f0f0;
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 0.9em;
  }
  .article-prose :global(pre code) {
    background: none;
    padding: 0;
  }

  .article-prose :global(hr) {
    border: none;
    border-top: 1px solid #EAECEF;
    margin: 40px 0;
  }

  @media (max-width: 768px) {
    .article-prose {
      font-size: 16px;
      padding: 40px 0;
    }
    .article-prose :global(h2) {
      font-size: 24px;
    }
    .article-prose :global(h3) {
      font-size: 19px;
    }
  }
</style>
```

- [ ] **Step 2: Verify build**

```bash
npm run build
```

- [ ] **Step 3: Commit**

```bash
git add src/components/blog/ArticleBody.astro
git commit -m "feat: add ArticleBody with magazine prose styles and drop cap"
```

---

### Task 11: ShareRow component

**Files:**
- Create: `src/components/blog/ShareRow.astro`

- [ ] **Step 1: Create ShareRow.astro**

```astro
---
interface Props {
  url: string;
  title: string;
}

const { url, title: articleTitle } = Astro.props;
const encodedUrl = encodeURIComponent(url);
const encodedTitle = encodeURIComponent(articleTitle);
---

<div class="share-row">
  <span class="share-label">Compartir</span>
  <div class="share-buttons">
    <a
      href={`https://twitter.com/intent/tweet?url=${encodedUrl}&text=${encodedTitle}`}
      target="_blank"
      rel="noopener noreferrer"
      class="share-btn"
      aria-label="Compartir en Twitter"
    >
      <svg class="share-icon" viewBox="0 0 24 24" fill="currentColor"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
    </a>

    <a
      href={`https://www.linkedin.com/sharing/share-offsite/?url=${encodedUrl}`}
      target="_blank"
      rel="noopener noreferrer"
      class="share-btn"
      aria-label="Compartir en LinkedIn"
    >
      <svg class="share-icon" viewBox="0 0 24 24" fill="currentColor"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 01-2.063-2.065 2.064 2.064 0 112.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>
    </a>

    <button
      class="share-btn share-btn-copy"
      aria-label="Copiar enlace"
      data-url={url}
    >
      <svg class="share-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1"/></svg>
      <span class="share-copy-tooltip" aria-live="polite"></span>
    </button>

    <a
      href={`mailto:?subject=${encodedTitle}&body=${encodedUrl}`}
      class="share-btn"
      aria-label="Compartir por email"
    >
      <svg class="share-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>
    </a>
  </div>
</div>

<script>
  document.querySelectorAll('.share-btn-copy').forEach((btn) => {
    btn.addEventListener('click', async () => {
      const url = (btn as HTMLElement).dataset.url;
      if (!url) return;
      try {
        await navigator.clipboard.writeText(url);
        const tooltip = btn.querySelector('.share-copy-tooltip') as HTMLElement;
        if (tooltip) {
          tooltip.textContent = '¡Copiado!';
          tooltip.classList.add('show');
          setTimeout(() => tooltip.classList.remove('show'), 2000);
        }
      } catch {
        // Fallback silently
      }
    });
  });
</script>

<style>
  .share-row {
    max-width: 760px;
    margin: 0 auto;
    padding: 40px 24px;
    text-align: center;
    border-top: 1px solid #EAECEF;
  }

  .share-label {
    display: block;
    color: #888;
    font-size: 13px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 16px;
  }

  .share-buttons {
    display: flex;
    justify-content: center;
    gap: 10px;
  }

  .share-btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 48px;
    height: 48px;
    border-radius: 12px;
    border: 1px solid #EAECEF;
    background: #fff;
    color: #555;
    cursor: pointer;
    transition: all 0.2s ease;
    position: relative;
    text-decoration: none;
  }
  .share-btn:hover {
    background: rgba(245, 166, 35, 0.08);
    border-color: #F5A623;
    color: #F5A623;
    transform: scale(1.08);
  }

  .share-icon {
    width: 18px;
    height: 18px;
  }

  .share-copy-tooltip {
    position: absolute;
    top: -36px;
    left: 50%;
    transform: translateX(-50%);
    background: #1a1a1a;
    color: #fff;
    font-size: 12px;
    padding: 4px 10px;
    border-radius: 6px;
    white-space: nowrap;
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.2s ease;
  }
  .share-copy-tooltip.show {
    opacity: 1;
  }
</style>
```

- [ ] **Step 2: Verify build**

```bash
npm run build
```

- [ ] **Step 3: Commit**

```bash
git add src/components/blog/ShareRow.astro
git commit -m "feat: add ShareRow with social buttons and copy tooltip"
```

---

### Task 12: RelatedArticles component

**Files:**
- Create: `src/components/blog/RelatedArticles.astro`

- [ ] **Step 1: Create RelatedArticles.astro**

```astro
---
import { getCollection } from 'astro:content';
import ArticleCard from './ArticleCard.astro';
import ScrollReveal from './ScrollReveal.astro';

interface Props {
  currentSlug: string;
  currentTags?: string[];
}

const { currentSlug, currentTags = [] } = Astro.props;

const allPosts = await getCollection('blog');
const sorted = allPosts.sort((a, b) => b.data.date.getTime() - a.data.date.getTime());

// Score posts by shared tags, exclude current post, take top 3
const scored = sorted
  .filter((p) => p.slug !== currentSlug)
  .map((p) => ({
    post: p,
    score: currentTags.length > 0
      ? p.data.tags?.filter((t) => currentTags.includes(t)).length ?? 0
      : 0,
  }))
  .sort((a, b) => b.score - a.score || b.post.data.date.getTime() - a.post.data.date.getTime());

const related = scored.slice(0, 3);
---

{related.length > 0 && (
  <section class="related-section">
    <div class="related-inner">
      <ScrollReveal>
        <h2 class="related-title">Artículos relacionados</h2>
      </ScrollReveal>
      <div class="related-grid">
        {related.map(({ post }, i) => (
          <ArticleCard
            index={i}
            slug={post.slug}
            title={post.data.title}
            description={post.data.description}
            image={post.data.image}
            tags={post.data.tags}
            date={post.data.date}
            author={post.data.author}
          />
        ))}
      </div>
    </div>
  </section>
)}

<style>
  .related-section {
    background: #F8F9FA;
    padding: 80px 20px;
  }
  .related-inner {
    max-width: 1100px;
    margin: 0 auto;
  }
  .related-title {
    text-align: center;
    font-size: 28px;
    font-weight: 700;
    color: #1a1a1a;
    margin: 0 0 40px;
    letter-spacing: -0.02em;
  }
  .related-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
    gap: 28px;
  }

  @media (max-width: 768px) {
    .related-section {
      padding: 60px 20px;
    }
    .related-grid {
      grid-template-columns: 1fr;
    }
    .related-title {
      font-size: 24px;
    }
  }
</style>
```

- [ ] **Step 2: Verify build**

```bash
npm run build
```

- [ ] **Step 3: Commit**

```bash
git add src/components/blog/RelatedArticles.astro
git commit -m "feat: add RelatedArticles with tag-based scoring"
```

---

### Task 13: Update [slug].astro blog branch

**Files:**
- Modify: `src/pages/[slug].astro`

- [ ] **Step 1: Replace the blog branch in [slug].astro**

Replace the `isBlog ? (...)` content section. The existing file has the blog branch after `isBlog ? (`. Replace the entire blog branch (from `isBlog ? (` through the matching `) : (` that precedes the service branch) with:

```astro
{
  isBlog ? (
    <>
      <ReadingProgress />
      <ArticleHero
        title={data.title}
        slug={entry.slug}
        image={data.image}
        tags={data.tags}
        date={data.date ?? new Date()}
        author={data.author ?? 'PYMEMPRESAS'}
      />
      <section class="section bg-white" style="padding-top:0;padding-bottom:40px;">
        <div class="container" style="max-width:800px;">
          <Breadcrumbs
            items={[
              { label: 'Inicio', href: '/' },
              { label: 'Blog', href: '/blog/' },
              { label: data.title },
            ]}
          />
        </div>
      </section>
      <ArticleBody>
        <Body />
      </ArticleBody>
      <ShareRow
        url={new URL(`/${entry.slug}/`, Astro.site).href}
        title={data.title}
      />
      <RelatedArticles
        currentSlug={entry.slug}
        currentTags={data.tags ?? []}
      />
      <FinalCTA />
    </>
  ) : (
    // ... existing service branch stays unchanged
```

- [ ] **Step 2: Add imports at top of [slug].astro**

Add these imports near the existing ones (after FinalCTA import):

```astro
import ReadingProgress from '../components/blog/ReadingProgress.astro';
import ArticleHero from '../components/blog/ArticleHero.astro';
import ArticleBody from '../components/blog/ArticleBody.astro';
import ShareRow from '../components/blog/ShareRow.astro';
import RelatedArticles from '../components/blog/RelatedArticles.astro';
```

- [ ] **Step 3: Verify build**

```bash
npm run build
```

Ensure no import errors. Check that service pages still render correctly (the `) : (` branch is intact).

- [ ] **Step 4: Check an article page**

Run `npm run dev` and visit `http://localhost:4321/seo-local-empresas-asturias/` (or the first blog slug). Verify:
- ReadingProgress bar at top
- ArticleHero with image parallax
- ArticleBody with drop cap and prose styles
- ShareRow at bottom
- RelatedArticles grid

- [ ] **Step 5: Commit**

```bash
git add src/pages/\[slug\].astro
git commit -m "feat: wire blog detail page with ArticleHero, ArticleBody, ShareRow, and RelatedArticles"
```

---

### Task 14: Final integration — View Transitions and polish

**Files:**
- Modify: `src/layouts/BaseLayout.astro`
- Modify: `src/styles/global.css`

- [ ] **Step 1: Add View Transitions support to BaseLayout.astro**

Add the import after other imports:

```astro
import { ViewTransitions } from 'astro:transitions';
```

Add `<ViewTransitions />` inside `<head>`, after `<meta name="viewport" ...>`:

```astro
<meta name="viewport" content="width=device-width, initial-scale=1" />
<ViewTransitions />
```

- [ ] **Step 2: Enable view transition names for cards → hero crossfade**

In `ArticleCard.astro`, add to the image link:

```astro
<a href={`/${slug}/`} class="blog-card-img-link" style={`view-transition-name: article-img-${slug.replace(/[^a-z0-9-]/g, '')}`}>
```

In `ArticleHero.astro`, add to the image:

```astro
<img ... style={`view-transition-name: article-img-${title.replace(/[^a-z0-9-]/g, '')}`.toLowerCase()} />
```

In ArticleCard, compute the safe id (add after the existing destructuring):

```astro
const safeSlug = slug.replace(/[^a-z0-9-]/g, '');
```

And add to the link: `style={`view-transition-name: article-img-${safeSlug}`}`

- [ ] **Step 3: Add reduced-motion fallback for View Transitions**

In `global.css`, add:

```css
@media (prefers-reduced-motion: reduce) {
  ::view-transition-old(*),
  ::view-transition-new(*) {
    animation: none !important;
  }
}
```

- [ ] **Step 4: Full build verification**

```bash
npm run build
```

Check output:
- All pages generated in dist/
- No CSS warnings
- Blog listing and detail pages exist

- [ ] **Step 5: Commit**

```bash
git add src/layouts/BaseLayout.astro src/components/blog/ArticleCard.astro src/components/blog/ArticleHero.astro src/pages/\[slug\].astro src/styles/global.css
git commit -m "feat: add View Transitions for smooth listing→detail navigation"
```

---

### Task 15: Final verification and smoke test

- [ ] **Step 1: Run dev server**

```bash
npm run dev
```

- [ ] **Step 2: Manual checks**

- [ ] `/blog/` — BlogHero renders, FeaturedCard first, ArticleCards in grid, hover effects work
- [ ] `/seo-local-empresas-asturias/` — ReadingProgress bar, ArticleHero with image, ArticleBody prose, ShareRow buttons, RelatedArticles below
- [ ] Click a card → smooth page transition via View Transitions
- [ ] `prefers-reduced-motion` — animations disabled
- [ ] Mobile viewport — responsive grid, readable typography

- [ ] **Step 3: Run production build**

```bash
npm run build
npm run preview
```

Verify `dist/` contains all 13 static pages + blog listing + blog posts.

- [ ] **Step 4: Commit any final tweaks**

```bash
git add -A
git commit -m "chore: final polish and smoke test verification"
```
