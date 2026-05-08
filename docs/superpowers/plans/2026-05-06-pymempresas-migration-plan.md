# PYMEMPRESAS — Migración WordPress a Astro Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Migrar pymempresas.com de WordPress a sitio estático Astro 5 con diseño idéntico mejorado.

**Architecture:** Astro 5 + Tailwind CSS 4 static build. Content via MDX collections (servicios). Contact form via n8n webhook. No CMS, no database, no SSR.

**Tech Stack:** Astro 5, Tailwind CSS 4, TypeScript, MDX, n8n webhook, Cloudflare Pages

---

## File Map

```
pymempresas-web/
├── astro.config.mjs
├── package.json
├── tsconfig.json
├── public/
│   ├── favicon.svg
│   ├── og-default.jpg
│   └── images/                          # Copiar imágenes desde raíz del proyecto
├── src/
│   ├── env.d.ts
│   ├── content/
│   │   ├── config.ts
│   │   ├── home.mdx
│   │   └── servicios/                   # 9 MDX files
│   ├── pages/
│   │   ├── index.astro
│   │   ├── [slug].astro
│   │   ├── consultoria.astro
│   │   ├── contacto.astro
│   │   ├── politica-privacidad.astro
│   │   ├── 404.astro
│   │   ├── sitemap.xml.ts
│   │   ├── robots.txt.ts
│   │   └── llms.txt.ts
│   ├── layouts/
│   │   └── BaseLayout.astro
│   ├── components/
│   │   ├── Header.astro
│   │   ├── Footer.astro
│   │   ├── HeroSection.astro
│   │   ├── ServicesGrid.astro
│   │   ├── AboutSection.astro
│   │   ├── StatsCounter.astro
│   │   ├── WhyChooseUs.astro
│   │   ├── FinalCTA.astro
│   │   ├── ContactForm.astro
│   │   ├── CookieBanner.astro
│   │   ├── Breadcrumbs.astro
│   │   └── SEO.astro
│   ├── lib/
│   │   └── constants.ts
│   └── styles/
│       └── global.css
```

---

### Task 1: Scaffolding del proyecto

**Files:**
- Create: `package.json`, `tsconfig.json`, `astro.config.mjs`, `src/env.d.ts`, `.gitignore`

- [ ] **Step 1: Crear package.json**

```json
{
  "name": "pymempresas-web",
  "type": "module",
  "version": "1.0.0",
  "scripts": {
    "dev": "astro dev",
    "build": "astro build",
    "preview": "astro preview"
  },
  "dependencies": {
    "@astrojs/mdx": "^4.0.0",
    "astro": "^5.0.0",
    "sharp": "^0.33.0"
  },
  "devDependencies": {
    "@tailwindcss/vite": "^4.0.0",
    "tailwindcss": "^4.0.0",
    "typescript": "^5.7.0"
  }
}
```

- [ ] **Step 2: Crear tsconfig.json**

```json
{
  "extends": "astro/tsconfigs/strict",
  "include": [".astro/types.d.ts", "src/**/*"],
  "exclude": ["dist"]
}
```

- [ ] **Step 3: Crear astro.config.mjs**

```js
import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  site: 'https://pymempresas.com',
  trailingSlash: 'always',
  integrations: [mdx()],
  vite: {
    plugins: [tailwindcss()],
  },
  build: {
    inlineStylesheets: 'always',
  },
});
```

- [ ] **Step 4: Crear src/env.d.ts**

```ts
/// <reference path="../.astro/types.d.ts" />
/// <reference types="astro/client" />
```

- [ ] **Step 5: Instalar dependencias y verificar build vacío**  

Run: `npm install`  
Run: `npm run build`  
Expected: Build exitoso (puede dar warning de páginas vacías, es normal)

- [ ] **Step 6: Commit**

```bash
git add package.json package-lock.json tsconfig.json astro.config.mjs src/env.d.ts
git commit -m "feat: scaffold Astro 5 + Tailwind 4 project"
```

---

### Task 2: Sistema de diseño — global.css

**Files:**
- Create: `src/styles/global.css`

- [ ] **Step 1: Crear global.css con Tailwind 4 + tokens**

```css
@import "tailwindcss";

@theme {
  --color-black: #0A0A0A;
  --color-card: #111111;
  --color-orange: #F5A623;
  --color-orange-dark: #E89B1F;
  --color-gray-light: #F5F5F5;
  --color-white: #FFFFFF;
  --font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", "Helvetica Neue", Arial, sans-serif;
}

/* Base */
html {
  scroll-behavior: smooth;
}

body {
  font-family: var(--font-sans);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-rendering: optimizeLegibility;
  color: var(--color-white);
  background: var(--color-black);
}

/* Heading hierarchy */
h1, h2, h3 {
  font-weight: 700;
  letter-spacing: -0.02em;
}

/* Focus visible */
:focus-visible {
  outline: 2px solid var(--color-orange);
  outline-offset: 2px;
}

/* Skip link */
.skip-link {
  position: absolute;
  top: -100%;
  left: 16px;
  background: var(--color-orange);
  color: var(--color-black);
  padding: 8px 16px;
  border-radius: 6px;
  font-weight: 600;
  z-index: 10000;
}
.skip-link:focus {
  top: 8px;
}

/* Container utility */
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
}

/* Section spacing */
.section {
  padding: 80px 0;
}

@media (max-width: 768px) {
  .section {
    padding: 60px 0;
  }
  .container {
    padding: 0 16px;
  }
}
```

- [ ] **Step 2: Commit**

```bash
git add src/styles/global.css
git commit -m "feat: add design system — Tailwind 4 tokens, typography, base styles"
```

---

### Task 3: Constantes y utilidades

**Files:**
- Create: `src/lib/constants.ts`

- [ ] **Step 1: Crear constants.ts**

```ts
export const SITE = {
  name: 'PYMEMPRESAS',
  url: 'https://pymempresas.com',
  defaultTitle: 'Posicionamiento WEB SEO ASTURIAS — PYMEMPRESAS',
  defaultDescription:
    'Posicionamiento WEB SEO para Empresas. Impulsa tu negocio en Gijón y Asturias con estrategias de SEO Local e Inteligencia Artificial.',
  slogan: 'Tu éxito digital, nuestra misión',
  ogImage: '/og-default.jpg',
  locale: 'es_ES',
} as const;

export const CONTACT = {
  email: 'info@pymempresas.com',
  emailForm: 'avieiros@gmail.com',
  phone: '+34 684 62 00 40',
  address: 'C. Rodríguez San Pedro, 12, 33206 Gijón, Asturias',
  googleMaps: 'https://maps.google.com/?q=Spaces+Coworking+Gijón',
  hours: 'Lun–Vie 9:00–18:00',
} as const;

export const SOCIAL = {
  linkedin: 'https://www.linkedin.com/in/arturovieiros/',
} as const;

export const NAV_ITEMS = [
  { label: 'Inicio', href: '/' },
  {
    label: 'Google Negocios',
    href: '#',
    children: [
      { label: 'SEO Local Gijón', href: '/seo-local-gijon/' },
      { label: 'SEO Local Oviedo', href: '/seo-local-oviedo/' },
    ],
  },
  {
    label: 'Servicios',
    href: '#',
    children: [
      { label: 'Diseño Web', href: '/diseno-web-gijon/' },
      { label: 'IA para Empresas', href: '/inteligencia-artificial-empresas/' },
      { label: 'Formación IA', href: '/formacion-ia-empresas/' },
      { label: 'Automatizaciones IA', href: '/automatizaciones-con-ia/' },
      { label: 'Posicionamiento Web', href: '/posicionamiento-web-asturias/' },
      { label: 'Google Negocios', href: '/google-negocios/' },
    ],
  },
  { label: 'Contacto', href: '/contacto/' },
] as const;

export const FOOTER_SERVICES = [
  { label: 'SEO Local', href: '/seo-local-gijon/' },
  { label: 'Diseño Web', href: '/diseno-web-gijon/' },
  { label: 'IA para Empresas', href: '/inteligencia-artificial-empresas/' },
  { label: 'Formación IA', href: '/formacion-ia-empresas/' },
  { label: 'Automatizaciones', href: '/automatizaciones-con-ia/' },
  { label: 'Posicionamiento Web', href: '/posicionamiento-web-asturias/' },
] as const;

export const FOOTER_LEGAL = [
  { label: 'Aviso Legal', href: '/aviso-legal/' },
  { label: 'Política de Privacidad', href: '/politica-privacidad/' },
  { label: 'Política de Cookies', href: '/politica-privacidad/' },
] as const;

export const WHY_CHOOSE_US = [
  {
    title: 'Aumenta tu visibilidad',
    description: 'Tu negocio aparece en los primeros resultados cuando tus clientes te buscan.',
    icon: 'eye',
  },
  {
    title: 'Más clientes locales',
    description: 'Atrae clientes cualificados de tu zona geográfica con estrategias de SEO local.',
    icon: 'users',
  },
  {
    title: 'Resultados medibles',
    description: 'Informes mensuales con métricas claras de posicionamiento y tráfico.',
    icon: 'chart',
  },
  {
    title: 'Ahorra tiempo',
    description: 'Céntrate en tu negocio mientras nosotros optimizamos tu presencia digital.',
    icon: 'clock',
  },
  {
    title: 'Reputación sólida',
    description: 'Construye una presencia online de confianza con reseñas y contenido de calidad.',
    icon: 'star',
  },
  {
    title: 'Expertos locales',
    description: 'Conocemos el mercado asturiano y sabemos qué funciona en cada sector.',
    icon: 'map-pin',
  },
] as const;
```

- [ ] **Step 2: Commit**

```bash
git add src/lib/constants.ts
git commit -m "feat: add site constants — nav, contact, social, services"
```

---

### Task 4: Componente SEO

**Files:**
- Create: `src/components/SEO.astro`

- [ ] **Step 1: Crear SEO.astro**

```astro
---
interface Props {
  title: string;
  description: string;
  canonicalURL: string;
  ogImage?: string;
  ogType?: string;
  noindex?: boolean;
  schema?: Record<string, unknown>;
}

const {
  title,
  description,
  canonicalURL,
  ogImage = '/og-default.jpg',
  ogType = 'website',
  noindex = false,
  schema,
} = Astro.props;

const fullTitle = title.includes('PYMEMPRESAS') ? title : `${title} — PYMEMPRESAS`;
---
<title>{fullTitle}</title>
<meta name="description" content={description} />
<meta name="robots" content={noindex ? 'noindex, follow' : 'index, follow, max-snippet:-1, max-image-preview:large'} />
<link rel="canonical" href={canonicalURL} />
<link rel="sitemap" href="/sitemap.xml" />

<meta property="og:locale" content="es_ES" />
<meta property="og:type" content={ogType} />
<meta property="og:title" content={fullTitle} />
<meta property="og:description" content={description} />
<meta property="og:url" content={canonicalURL} />
<meta property="og:site_name" content="Pymempresas" />
<meta property="og:image" content={new URL(ogImage, Astro.site).href} />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />

<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content={fullTitle} />
<meta name="twitter:description" content={description} />
<meta name="twitter:image" content={new URL(ogImage, Astro.site).href} />

<script type="application/ld+json" set:html={JSON.stringify(schema)} />
```

- [ ] **Step 2: Commit**

```bash
git add src/components/SEO.astro
git commit -m "feat: add SEO component — meta tags, OG, Twitter, JSON-LD"
```

---

### Task 5: BaseLayout

**Files:**
- Create: `src/layouts/BaseLayout.astro`

- [ ] **Step 1: Crear BaseLayout.astro**

```astro
---
import '../styles/global.css';
import SEO from '../components/SEO.astro';
import Header from '../components/Header.astro';
import Footer from '../components/Footer.astro';
import CookieBanner from '../components/CookieBanner.astro';

interface Props {
  metaTitle: string;
  metaDescription: string;
  canonicalURL?: string;
  ogImage?: string;
  ogType?: string;
  noindex?: boolean;
  schema?: Record<string, unknown>;
}

const canonicalURL = Astro.props.canonicalURL ?? new URL(Astro.url.pathname, Astro.site).href;
---
<!doctype html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
    <SEO
      title={Astro.props.metaTitle}
      description={Astro.props.metaDescription}
      canonicalURL={canonicalURL}
      ogImage={Astro.props.ogImage}
      ogType={Astro.props.ogType}
      noindex={Astro.props.noindex}
      schema={Astro.props.schema}
    />
  </head>
  <body>
    <a href="#main-content" class="skip-link">Saltar al contenido</a>
    <Header />
    <main id="main-content">
      <slot />
    </main>
    <Footer />
    <CookieBanner />
  </body>
</html>
```

- [ ] **Step 2: Commit**

```bash
git add src/layouts/BaseLayout.astro
git commit -m "feat: add BaseLayout — HTML shell, SEO, Header, Footer, CookieBanner"
```

---

### Task 6: Header

**Files:**
- Create: `src/components/Header.astro`

- [ ] **Step 1: Crear Header.astro**

```astro
---
import { NAV_ITEMS } from '../lib/constants';
---
<header class="fixed top-0 left-0 right-0 z-50 bg-black/70 backdrop-blur-[15px] transition-all duration-300" id="site-header">
  <div class="container flex items-center justify-between py-2">
    <a href="/" class="flex items-center shrink-0" aria-label="PYMEMPRESAS — Ir al inicio">
      <img
        src="/images/cropped-pymempresas-logo-4k__1_-removebg-preview.png"
        alt="PYMEMPRESAS"
        class="h-[35px] w-auto"
        width="160"
        height="35"
      />
    </a>

    <nav class="hidden lg:flex items-center gap-1" aria-label="Navegación principal">
      {NAV_ITEMS.map((item) => (
        item.children ? (
          <div class="relative group">
            <button class="px-4 py-2 text-sm font-medium text-white hover:text-orange transition-colors flex items-center gap-1">
              {item.label}
              <svg class="w-3 h-3 group-hover:rotate-180 transition-transform" viewBox="0 0 12 12" fill="currentColor">
                <path d="M6 8L1 3h10z"/>
              </svg>
            </button>
            <div class="absolute top-full left-0 mt-1 min-w-[220px] bg-black/98 backdrop-blur-[20px] border border-white/10 rounded-lg shadow-2xl opacity-0 invisible translate-y-2 group-hover:opacity-100 group-hover:visible group-hover:translate-y-0 transition-all duration-300 py-2">
              {item.children.map((child) => (
                <a href={child.href} class="block px-5 py-3 text-sm text-white hover:text-orange hover:bg-orange/10 hover:pl-6 transition-all duration-200">
                  {child.label}
                </a>
              ))}
            </div>
          </div>
        ) : (
          <a href={item.href} class="relative px-4 py-2 text-sm font-medium text-white hover:text-orange transition-colors group">
            {item.label}
            <span class="absolute bottom-0 left-1/2 w-0 h-[2px] bg-orange -translate-x-1/2 group-hover:w-[70%] transition-all duration-300"></span>
          </a>
        )
      ))}
    </nav>

    <a href="/consultoria/" class="hidden lg:inline-flex items-center bg-gradient-to-br from-orange to-orange-dark text-black font-semibold text-sm px-5 py-2.5 rounded-[10px] shadow-[0_4px_15px_rgba(245,166,35,0.4)] hover:-translate-y-0.5 hover:shadow-[0_6px_25px_rgba(245,166,35,0.6)] transition-all duration-300">
      Consultoría Gratis
    </a>

    <!-- Mobile menu button -->
    <button id="mobile-menu-btn" class="lg:hidden p-2.5 bg-black/50 border border-white/20 rounded-lg text-white hover:bg-orange/20 hover:border-orange transition-all" aria-label="Abrir menú">
      <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 6h16M4 12h16M4 18h16"/></svg>
    </button>
  </div>

  <!-- Mobile menu -->
  <div id="mobile-menu" class="hidden lg:hidden bg-black/98 backdrop-blur-[20px] mx-4 mb-4 rounded-xl p-4 shadow-2xl">
    <nav class="flex flex-col gap-1">
      {NAV_ITEMS.map((item) => (
        item.children ? (
          <details class="group">
            <summary class="px-4 py-3 text-sm font-medium text-white hover:text-orange cursor-pointer list-none flex items-center justify-between">
              {item.label}
              <svg class="w-3 h-3 group-open:rotate-180 transition-transform" viewBox="0 0 12 12" fill="currentColor"><path d="M6 8L1 3h10z"/></svg>
            </summary>
            <div class="ml-4 pl-4 border-l-2 border-orange py-1">
              {item.children.map((child) => (
                <a href={child.href} class="block px-3 py-2.5 text-sm text-white/80 hover:text-orange transition-colors">{child.label}</a>
              ))}
            </div>
          </details>
        ) : (
          <a href={item.href} class="px-4 py-3 text-sm font-medium text-white hover:text-orange transition-colors border-b border-white/5 last:border-none">{item.label}</a>
        )
      ))}
    </nav>
    <a href="/consultoria/" class="block text-center mt-3 bg-gradient-to-br from-orange to-orange-dark text-black font-semibold text-sm px-5 py-3 rounded-[10px] shadow-[0_4px_15px_rgba(245,166,35,0.4)]">
      Consultoría Gratis
    </a>
  </div>
</header>

<script>
  const btn = document.getElementById('mobile-menu-btn');
  const menu = document.getElementById('mobile-menu');
  btn?.addEventListener('click', () => menu?.classList.toggle('hidden'));

  // Sticky header: solid background on scroll
  const header = document.getElementById('site-header');
  window.addEventListener('scroll', () => {
    header?.classList.toggle('!bg-black/98', window.scrollY > 50);
  });
</script>
```

- [ ] **Step 2: Commit**

```bash
git add src/components/Header.astro
git commit -m "feat: add Header — sticky nav, dropdowns, mobile menu, scroll effect"
```

---

### Task 7: Footer

**Files:**
- Create: `src/components/Footer.astro`

- [ ] **Step 1: Crear Footer.astro**

```astro
---
import { CONTACT, FOOTER_SERVICES, FOOTER_LEGAL } from '../lib/constants';
---
<footer class="bg-black border-t border-white/5 pt-16 pb-8">
  <div class="container">
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-10 mb-12">
      <!-- Col 1: Brand -->
      <div>
        <img
          src="/images/cropped-pymempresas-logo-4k__1_-removebg-preview.png"
          alt="PYMEMPRESAS"
          class="h-[35px] w-auto mb-4"
          width="160"
          height="35"
          loading="lazy"
        />
        <p class="text-sm text-white/60 leading-relaxed">
          Agencia SEO en Asturias. Posicionamiento web, diseño y marketing digital
          para PYMES en Gijón, Oviedo y Avilés.
        </p>
      </div>

      <!-- Col 2: Servicios -->
      <div>
        <h4 class="text-sm font-semibold text-white uppercase tracking-wider mb-4">Servicios</h4>
        <ul class="space-y-2.5">
          {FOOTER_SERVICES.map((s) => (
            <li><a href={s.href} class="text-sm text-white/60 hover:text-orange transition-colors">{s.label}</a></li>
          ))}
        </ul>
      </div>

      <!-- Col 3: Contacto -->
      <div>
        <h4 class="text-sm font-semibold text-white uppercase tracking-wider mb-4">Contacto</h4>
        <ul class="space-y-2.5 text-sm text-white/60">
          <li>{CONTACT.address}</li>
          <li><a href={`tel:${CONTACT.phone}`} class="hover:text-orange transition-colors">{CONTACT.phone}</a></li>
          <li><a href={`mailto:${CONTACT.email}`} class="hover:text-orange transition-colors">{CONTACT.email}</a></li>
        </ul>
      </div>

      <!-- Col 4: CTA -->
      <div>
        <h4 class="text-sm font-semibold text-white uppercase tracking-wider mb-4">¿Empezamos?</h4>
        <a href="/consultoria/" class="inline-flex items-center bg-gradient-to-br from-orange to-orange-dark text-black font-semibold text-sm px-6 py-3 rounded-[10px] shadow-[0_4px_15px_rgba(245,166,35,0.4)] hover:-translate-y-0.5 hover:shadow-[0_6px_25px_rgba(245,166,35,0.6)] transition-all duration-300 mb-4">
          Consulta Gratis
        </a>
      </div>
    </div>

    <!-- Bottom bar -->
    <div class="border-t border-white/5 pt-6 flex flex-col sm:flex-row items-center justify-between gap-4">
      <p class="text-xs text-white/40">&copy; {new Date().getFullYear()} PYMEMPRESAS. Todos los derechos reservados.</p>
      <nav class="flex gap-4" aria-label="Enlaces legales">
        {FOOTER_LEGAL.map((l) => (
          <a href={l.href} class="text-xs text-white/40 hover:text-white/60 transition-colors">{l.label}</a>
        ))}
      </nav>
    </div>
  </div>
</footer>
```

- [ ] **Step 2: Commit**

```bash
git add src/components/Footer.astro
git commit -m "feat: add Footer — 4-column layout, services, contact, legal"
```

---

### Task 8: HeroSection

**Files:**
- Create: `src/components/HeroSection.astro`

- [ ] **Step 1: Crear HeroSection.astro**

```astro
---
interface Props {
  title: string;
  subtitle: string;
  cta: string;
  ctaHref: string;
  ctaSecondary?: string;
  ctaSecondaryHref?: string;
  badge?: string;
  checks?: string[];
  bgImage: string;
}

const { title, subtitle, cta, ctaHref, ctaSecondary, ctaSecondaryHref, badge, checks, bgImage } = Astro.props;
---

<section class="relative min-h-[100vh] flex items-center overflow-hidden">
  <img
    src={bgImage}
    alt=""
    class="absolute inset-0 w-full h-full object-cover object-center"
    loading="eager"
    decoding="async"
    width="1920"
    height="1080"
  />
  <div class="absolute inset-0 bg-gradient-to-br from-black/75 to-black/55"></div>

  <div class="container relative z-10 pt-24 pb-16">
    <div class="max-w-[600px]">
      {badge && (
        <span class="inline-flex items-center gap-2 bg-white/15 backdrop-blur-[10px] border border-white/25 rounded-full px-4 py-1.5 text-xs text-white font-semibold tracking-wider mb-5">
          <svg class="w-4 h-4 text-orange" viewBox="0 0 24 24" fill="currentColor"><circle cx="12" cy="12" r="10"/></svg>
          {badge}
        </span>
      )}

      <h1 class="text-[clamp(2.2rem,4.5vw,3.2rem)] font-bold leading-[1.15] mb-5 text-white [text-shadow:0_2px_20px_rgba(0,0,0,0.3)]">
        {title}
      </h1>

      <p class="text-[clamp(0.95rem,1.8vw,1.05rem)] leading-relaxed mb-6 text-white/90 max-w-[560px]">
        {subtitle}
      </p>

      {checks && checks.length > 0 && (
        <div class="flex flex-wrap gap-5 mb-8">
          {checks.map((check) => (
            <span class="flex items-center gap-2 text-sm text-white/95">
              <svg class="w-[22px] h-[22px] bg-orange rounded-full p-1 text-black shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><path d="M5 13l4 4L19 7"/></svg>
              {check}
            </span>
          ))}
        </div>
      )}

      <div class="flex flex-wrap gap-4">
        <a href={ctaHref} class="inline-flex items-center justify-center bg-gradient-to-br from-orange to-orange-dark text-black font-semibold text-[15px] px-7 py-3.5 rounded-[10px] shadow-[0_4px_15px_rgba(245,166,35,0.4)] hover:-translate-y-0.5 hover:shadow-[0_6px_25px_rgba(245,166,35,0.6)] transition-all duration-300 no-underline">
          {cta}
        </a>
        {ctaSecondary && ctaSecondaryHref && (
          <a href={ctaSecondaryHref} class="inline-flex items-center justify-center bg-white/10 backdrop-blur-[10px] text-white font-semibold text-[15px] px-7 py-3.5 rounded-[10px] border border-white/30 hover:bg-white/15 hover:border-white/50 hover:-translate-y-0.5 transition-all duration-300 no-underline">
            {ctaSecondary}
          </a>
        )}
      </div>
    </div>
  </div>
</section>
```

- [ ] **Step 2: Commit**

```bash
git add src/components/HeroSection.astro
git commit -m "feat: add HeroSection — full-width bg, overlay, badge, checks, CTAs"
```

---

### Task 9: ServicesGrid + ServiceCard

**Files:**
- Create: `src/components/ServicesGrid.astro`

- [ ] **Step 1: Crear ServicesGrid.astro**

```astro
---
import type { CollectionEntry } from 'astro:content';

interface Props {
  servicios: CollectionEntry<'servicios'>[];
}

const { servicios } = Astro.props;
---

<section class="section bg-gray-light" id="servicios">
  <div class="container">
    <div class="text-center mb-14">
      <span class="text-orange text-sm font-semibold uppercase tracking-wider">Nuestros Servicios</span>
      <h2 class="text-3xl font-bold text-black mt-2">Soluciones digitales para tu negocio</h2>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {servicios.map((s) => (
        <a href={`/${s.slug}/`} class="group block bg-card rounded-xl p-6 border border-white/5 hover:border-orange/30 transition-all duration-300 hover:-translate-y-1">
          <h3 class="text-lg font-bold text-white mb-3 group-hover:text-orange transition-colors">{s.data.title}</h3>
          <p class="text-sm text-white/60 leading-relaxed mb-4">{s.data.subtitle}</p>
          <ul class="space-y-2 mb-6">
            {s.data.features.slice(0, 3).map((f) => (
              <li class="flex items-start gap-2 text-sm text-white/70">
                <svg class="w-4 h-4 text-orange shrink-0 mt-0.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><path d="M5 13l4 4L19 7"/></svg>
                {f.title}
              </li>
            ))}
          </ul>
          <span class="text-orange text-sm font-semibold group-hover:translate-x-1 transition-transform inline-block">
            Más información &rarr;
          </span>
        </a>
      ))}
    </div>
  </div>
</section>
```

- [ ] **Step 2: Commit**

```bash
git add src/components/ServicesGrid.astro
git commit -m "feat: add ServicesGrid — 3-col card grid from services collection"
```

---

### Task 10: AboutSection + StatsCounter

**Files:**
- Create: `src/components/AboutSection.astro`, `src/components/StatsCounter.astro`

- [ ] **Step 1: Crear AboutSection.astro**

```astro
---
import { CONTACT } from '../lib/constants';
---

<section class="section bg-black" id="sobre-nosotros">
  <div class="container">
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
      <div>
        <span class="text-orange text-sm font-semibold uppercase tracking-wider">Sobre Nosotros</span>
        <h2 class="text-3xl font-bold text-white mt-2 mb-6">Agencia SEO local en el corazón de Asturias</h2>
        <div class="space-y-4 text-white/70 leading-relaxed">
          <p>
            En <strong class="text-white">PYMEMPRESAS</strong> ayudamos a negocios locales
            a conseguir más clientes a través de estrategias de posicionamiento web y SEO local.
            Trabajamos desde Gijón para toda Asturias.
          </p>
          <p>
            Nuestro enfoque combina <strong class="text-white">SEO técnico, optimización de Google Business Profile
            e inteligencia artificial</strong> para que tu negocio aparezca donde tus clientes te buscan.
          </p>
          <p>
            Sin fórmulas mágicas. Solo trabajo constante, datos reales y estrategias personalizadas
            adaptadas a tu sector y zona geográfica.
          </p>
        </div>
        <a href="/contacto/" class="inline-flex items-center gap-2 text-orange font-semibold text-sm mt-6 hover:gap-3 transition-all">
          Conoce más sobre nosotros
          <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
        </a>
      </div>

      <div class="bg-card rounded-xl p-8 border border-white/5">
        <h3 class="text-lg font-bold text-white mb-6">Ficha verificada en Google My Business</h3>
        <div class="aspect-[4/3] bg-black/50 rounded-lg flex items-center justify-center mb-4">
          <span class="text-white/40 text-sm">Mapa — {CONTACT.address}</span>
        </div>
        <p class="text-sm text-white/50">{CONTACT.address}</p>
      </div>
    </div>
  </div>
</section>
```

- [ ] **Step 2: Crear StatsCounter.astro**

```astro
---
const stats = [
  { value: '10+', label: 'Años de experiencia' },
  { value: '150+', label: 'Proyectos completados' },
  { value: '95%', label: 'Clientes satisfechos' },
  { value: '1ª', label: 'Página de Google' },
];
---

<section class="bg-card py-12 border-y border-white/5">
  <div class="container">
    <div class="grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
      {stats.map((s) => (
        <div>
          <div class="text-3xl md:text-4xl font-bold text-orange mb-1">{s.value}</div>
          <div class="text-sm text-white/50">{s.label}</div>
        </div>
      ))}
    </div>
  </div>
</section>
```

- [ ] **Step 3: Commit**

```bash
git add src/components/AboutSection.astro src/components/StatsCounter.astro
git commit -m "feat: add AboutSection + StatsCounter — about copy, GMB card, stat counters"
```

---

### Task 11: WhyChooseUs + FinalCTA

**Files:**
- Create: `src/components/WhyChooseUs.astro`, `src/components/FinalCTA.astro`

- [ ] **Step 1: Crear WhyChooseUs.astro**

```astro
---
import { WHY_CHOOSE_US } from '../lib/constants';

const iconMap: Record<string, string> = {
  eye: '<path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/>',
  users: '<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/>',
  chart: '<path d="M18 20V10M12 20V4M6 20v-6"/>',
  clock: '<circle cx="12" cy="12" r="10"/><polyline points="12,6 12,12 16,14"/>',
  star: '<polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>',
  'map-pin': '<path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>',
};
---

<section class="section bg-black" id="por-que-elegirnos">
  <div class="container">
    <div class="text-center mb-14">
      <span class="text-orange text-sm font-semibold uppercase tracking-wider">Por Qué Elegirnos</span>
      <h2 class="text-3xl font-bold text-white mt-2">Razones para confiar en nosotros</h2>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {WHY_CHOOSE_US.map((item) => (
        <div class="bg-card rounded-xl p-6 border border-white/5 hover:border-orange/30 transition-all duration-300">
          <div class="w-10 h-10 bg-orange/10 rounded-lg flex items-center justify-center mb-4">
            <svg class="w-5 h-5 text-orange" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <Fragment set:html={iconMap[item.icon] ?? iconMap.star} />
            </svg>
          </div>
          <h3 class="font-bold text-white mb-2">{item.title}</h3>
          <p class="text-sm text-white/60 leading-relaxed">{item.description}</p>
        </div>
      ))}
    </div>
  </div>
</section>
```

- [ ] **Step 2: Crear FinalCTA.astro**

```astro
---
import { CONTACT } from '../lib/constants';
---

<section class="section bg-card">
  <div class="container text-center">
    <h2 class="text-3xl font-bold text-white mb-4">Empieza a posicionar tu negocio en Google</h2>
    <p class="text-white/70 max-w-[600px] mx-auto mb-10 leading-relaxed">
      Solicita tu consultoría gratuita y te mostraremos exactamente cómo podemos ayudarte
      a atraer más clientes. Sin compromiso.
    </p>

    <div class="flex flex-wrap justify-center gap-6 mb-10 text-sm text-white/50">
      <a href={`tel:${CONTACT.phone}`} class="flex items-center gap-2 hover:text-orange transition-colors">
        <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
        {CONTACT.phone}
      </a>
      <a href={`mailto:${CONTACT.email}`} class="flex items-center gap-2 hover:text-orange transition-colors">
        <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>
        {CONTACT.email}
      </a>
      <span class="flex items-center gap-2">{CONTACT.address}</span>
    </div>

    <div class="flex flex-wrap justify-center gap-4">
      <a href="/consultoria/" class="inline-flex items-center bg-gradient-to-br from-orange to-orange-dark text-black font-semibold text-[15px] px-7 py-3.5 rounded-[10px] shadow-[0_4px_15px_rgba(245,166,35,0.4)] hover:-translate-y-0.5 hover:shadow-[0_6px_25px_rgba(245,166,35,0.6)] transition-all duration-300">
        Solicitar Consultoría Gratis
      </a>
    </div>

    <p class="text-xs text-white/30 mt-6">Sin compromiso &middot; Respuesta en menos de 24 horas &middot; 100% confidencial</p>
  </div>
</section>
```

- [ ] **Step 3: Commit**

```bash
git add src/components/WhyChooseUs.astro src/components/FinalCTA.astro
git commit -m "feat: add WhyChooseUs + FinalCTA — benefit cards, contact strip, trust line"
```

---

### Task 12: Content Collections — Config + Schema

**Files:**
- Create: `src/content/config.ts`

- [ ] **Step 1: Crear content config con schemas**

```ts
import { defineCollection, z } from 'astro:content';

const serviciosCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    subtitle: z.string(),
    description: z.string(),
    heroCta: z.string(),
    heroCtaHref: z.string().default('/consultoria/'),
    badge: z.string().optional(),
    heroChecks: z.array(z.string()).optional(),
    heroBgImage: z.string().default('/images/hero-bg-DF654TP8.jpg'),
    features: z.array(
      z.object({
        title: z.string(),
        description: z.string(),
        icon: z.string(),
      })
    ),
    benefits: z.array(z.string()),
    faq: z
      .array(
        z.object({
          q: z.string(),
          a: z.string(),
        })
      )
      .optional(),
    relatedServices: z.array(z.string()).max(3).optional(),
    ogImage: z.string().optional(),
    schemaOverrides: z.record(z.unknown()).optional(),
  }),
});

export const collections = {
  servicios: serviciosCollection,
};
```

- [ ] **Step 2: Commit**

```bash
git add src/content/config.ts
git commit -m "feat: add content collections config — servicios schema with Zod"
```

---

### Task 13: MDX Content — Home + Servicios

**Files:**
- Create: `src/content/home.mdx`, `src/content/servicios/seo-local-gijon.mdx`, `src/content/servicios/seo-local-oviedo.mdx`, `src/content/servicios/diseno-web-gijon.mdx`, `src/content/servicios/inteligencia-artificial-empresas.mdx`, `src/content/servicios/formacion-ia-empresas.mdx`, `src/content/servicios/automatizaciones-con-ia.mdx`, `src/content/servicios/google-negocios.mdx`, `src/content/servicios/posicionamiento-web-asturias.mdx`

- [ ] **Step 1: Crear home.mdx**

```mdx
---
title: "Posicionamiento WEB SEO ASTURIAS"
subtitle: "Posicionamiento WEB SEO para Empresas. Impulsa tu negocio en Gijón y Asturias con estrategias de SEO Local e Inteligencia Artificial."
description: "Posicionamiento WEB SEO para Empresas. Impulsa tu negocio en Gijón y Asturias con estrategias de SEO Local e Inteligencia Artificial."
heroCta: "Solicitar Consultoría Gratis"
heroCtaHref: "/consultoria/"
heroCtaSecondary: "Ver Servicios"
heroCtaSecondaryHref: "/#servicios"
badge: "Agencia de SEO Local en Asturias"
heroChecks:
  - "Resultados en Google"
  - "Clientes locales cualificados"
  - "Estrategias personalizadas"
heroBgImage: "/images/hero-bg-DF654TP8.jpg"
ogImage: "/og-default.jpg"
---
```

- [ ] **Step 2: Crear seo-local-gijon.mdx**

```mdx
---
title: "SEO Local Gijón"
subtitle: "Posiciona tu negocio en Gijón para atraer clientes locales cualificados"
description: "¿Quieres conseguir clientes locales en Gijón? Especialistas en SEO Local, Google My Business y posicionamiento web. Planes desde 297€/mes."
heroCta: "Solicitar Consultoría Gratis"
heroCtaHref: "/consultoria/"
heroBgImage: "/images/hero-bg-DF654TP8.jpg"
features:
  - title: "Google Business Profile"
    description: "Optimización completa de tu ficha de Google My Business para aparecer en el mapa local."
    icon: "map-pin"
  - title: "Palabras clave locales"
    description: "Investigación de keywords con intención local para tu sector en Gijón."
    icon: "search"
  - title: "SEO On-Page"
    description: "Optimización técnica de tu web para los factores de posicionamiento local."
    icon: "code"
  - title: "Link Building Local"
    description: "Estrategia de enlaces desde directorios y medios locales de Asturias."
    icon: "link"
  - title: "Reseñas y reputación"
    description: "Gestión de reseñas de Google para mejorar tu valoración y atraer más clics."
    icon: "star"
  - title: "Informes mensuales"
    description: "Reportes claros con la evolución de tu posicionamiento y tráfico orgánico."
    icon: "chart"
benefits:
  - "Más visibilidad en búsquedas locales de Gijón"
  - "Atrae clientes que buscan tus servicios en tu zona"
  - "Supera a tu competencia local en Google"
  - "Resultados medibles desde el primer mes"
  - "Soporte personalizado y cercano"
  - "Planes adaptados a tu presupuesto"
faq:
  - q: "¿Cuánto se tarda en posicionar un negocio local en Gijón?"
    a: "Los primeros resultados suelen verse entre 2 y 4 meses, dependiendo de la competencia de tu sector y zona. El SEO local suele ser más rápido que el SEO nacional porque hay menos competencia."
  - q: "¿Necesito tener página web para hacer SEO local?"
    a: "No es imprescindible. Con una ficha de Google Business Profile optimizada ya puedes empezar a aparecer. Pero tener web propia acelera mucho los resultados."
  - q: "¿Qué diferencia hay entre SEO normal y SEO local?"
    a: "El SEO local se centra en aparecer en búsquedas con intención geográfica (ej. 'fontanero Gijón') y en Google Maps. El SEO normal apunta a palabras clave más genéricas sin componente local."
relatedServices:
  - "google-negocios"
  - "posicionamiento-web-asturias"
  - "diseno-web-gijon"
---
```

- [ ] **Step 3: Crear resto de MDX de servicios**

Crear `seo-local-oviedo.mdx`, `diseno-web-gijon.mdx`, `inteligencia-artificial-empresas.mdx`, `formacion-ia-empresas.mdx`, `automatizaciones-con-ia.mdx`, `google-negocios.mdx`, `posicionamiento-web-asturias.mdx`.

Cada uno sigue el mismo schema con contenido específico del servicio. Los títulos y descripciones base se extraen del XML de WordPress:

**seo-local-oviedo.mdx:**
```mdx
---
title: "SEO Local Oviedo"
subtitle: "Posiciona tu negocio en Oviedo y atrae más clientes locales"
description: "Especialistas en SEO Local en Oviedo. Optimizamos tu Google Business Profile y posicionamiento web para que tu negocio aparezca en las búsquedas locales."
heroCta: "Solicitar Consultoría Gratis"
heroCtaHref: "/consultoria/"
features:
  - title: "Google Business Profile Oviedo"
    description: "Optimización de tu ficha para búsquedas locales en Oviedo y alrededores."
    icon: "map-pin"
  - title: "Keywords locales"
    description: "Palabras clave con intención de búsqueda en Oviedo y área metropolitana."
    icon: "search"
  - title: "SEO On-Page local"
    description: "Optimización técnica con enfoque en términos geolocalizados de Oviedo."
    icon: "code"
  - title: "Competencia local"
    description: "Análisis de tu competencia en Oviedo para superarlos en Google."
    icon: "trending-up"
  - title: "Reseñas Google"
    description: "Estrategia para conseguir y gestionar reseñas de clientes en Oviedo."
    icon: "star"
  - title: "Informes de posicionamiento"
    description: "Seguimiento mensual de tu evolución en búsquedas locales de Oviedo."
    icon: "chart"
benefits:
  - "Domina las búsquedas locales en Oviedo"
  - "Consigue clientes de tu zona geográfica"
  - "Supera a tu competencia en Google Maps"
  - "Estrategia adaptada al mercado ovetense"
  - "Atención personalizada y cercana"
  - "Resultados medibles y transparentes"
---
```

**diseno-web-gijon.mdx:**
```mdx
---
title: "Diseño Web en Gijón"
subtitle: "Páginas web rápidas, modernas y optimizadas para convertir visitas en clientes"
description: "Diseño web en Gijón para PYMES. Webs rápidas, responsive y optimizadas para SEO. Presencia profesional que convierte visitas en clientes."
heroCta: "Solicitar Presupuesto"
heroCtaHref: "/consultoria/"
features:
  - title: "Diseño a medida"
    description: "Webs personalizadas que reflejan la identidad de tu negocio, sin plantillas genéricas."
    icon: "layout"
  - title: "Optimización SEO"
    description: "Cada web que diseñamos incluye SEO técnico para posicionar desde el día uno."
    icon: "search"
  - title: "Rendimiento máximo"
    description: "Webs que cargan en menos de 2 segundos para mejor experiencia y SEO."
    icon: "zap"
  - title: "Diseño responsive"
    description: "Tu web se ve perfecta en móviles, tablets y ordenadores."
    icon: "smartphone"
  - title: "Mantenimiento incluido"
    description: "Nos encargamos de actualizaciones, seguridad y backups de tu web."
    icon: "shield"
  - title: "Formación incluida"
    description: "Te enseñamos a gestionar tu web para que no dependas de nadie."
    icon: "book"
benefits:
  - "Presencia profesional 24/7 para tu negocio"
  - "Web optimizada para atraer y convertir clientes"
  - "Carga ultrarrápida que mejora tu SEO"
  - "Diseño adaptado a tu sector y público objetivo"
  - "Soporte y mantenimiento continuo"
  - "Integración con Google Business Profile y redes sociales"
---
```

**inteligencia-artificial-empresas.mdx:**
```mdx
---
title: "Inteligencia Artificial para Empresas en Gijón"
subtitle: "Automatiza procesos, reduce costes y escala tu negocio con IA"
description: "Implementamos inteligencia artificial en tu empresa para automatizar tareas, mejorar la atención al cliente y aumentar la productividad. Soluciones prácticas de IA para PYMES."
heroCta: "Solicitar Consultoría"
heroCtaHref: "/consultoria/"
features:
  - title: "Automatización de tareas"
    description: "Libera a tu equipo de tareas repetitivas con flujos de trabajo inteligentes."
    icon: "settings"
  - title: "Chatbots inteligentes"
    description: "Atención al cliente 24/7 con asistentes virtuales entrenados con tu información."
    icon: "message-circle"
  - title: "Análisis de datos"
    description: "Toma decisiones basadas en datos con dashboards y análisis predictivo con IA."
    icon: "bar-chart"
  - title: "Generación de contenido"
    description: "Crea textos, imágenes y documentos para tu marketing de forma automatizada."
    icon: "edit"
  - title: "Procesamiento documental"
    description: "Extrae y organiza información de facturas, contratos y documentos automáticamente."
    icon: "file-text"
  - title: "Consultoría y formación"
    description: "Te guiamos en la adopción de IA con formaciones prácticas para tu equipo."
    icon: "users"
benefits:
  - "Reduce costes operativos automatizando procesos manuales"
  - "Mejora el servicio al cliente 24/7 con IA"
  - "Toma decisiones más rápidas y basadas en datos"
  - "Escala tu negocio sin aumentar costes proporcionalmente"
  - "Ahorra horas de trabajo repetitivo cada semana"
  - "Tecnología accesible sin necesidad de conocimientos técnicos"
---
```

**formacion-ia-empresas.mdx:**
```mdx
---
title: "Formación en Inteligencia Artificial para Empresas"
subtitle: "Capacita a tu equipo en IA práctica para el día a día del negocio"
description: "Formación práctica en inteligencia artificial para empresas y PYMES. Cursos adaptados a tu sector para que tu equipo domine las herramientas de IA."
heroCta: "Solicitar Información"
heroCtaHref: "/consultoria/"
features:
  - title: "IA para directivos"
    description: "Visión estratégica de cómo la IA puede transformar tu modelo de negocio."
    icon: "briefcase"
  - title: "IA para marketing"
    description: "Creación de contenido, análisis de audiencias y automatización de campañas con IA."
    icon: "target"
  - title: "IA para ventas"
    description: "Optimización de procesos comerciales con herramientas de inteligencia artificial."
    icon: "dollar-sign"
  - title: "IA para administración"
    description: "Automatización de facturación, gestión documental y tareas administrativas con IA."
    icon: "file-text"
  - title: "IA para RRHH"
    description: "Optimización de selección, onboarding y gestión del talento con IA."
    icon: "users"
  - title: "Talleres prácticos"
    description: "Formaciones hands-on donde tu equipo aprende usando herramientas reales de IA."
    icon: "play"
benefits:
  - "Equipo más productivo usando herramientas de IA"
  - "Formación adaptada a las necesidades reales de tu empresa"
  - "Aplicación práctica desde el primer día"
  - "Materiales y recursos actualizados continuamente"
  - "Soporte post-formación para resolver dudas"
  - "Modalidad presencial en Asturias u online"
---
```

**automatizaciones-con-ia.mdx:**
```mdx
---
title: "Automatizaciones con IA"
subtitle: "Conecta tus herramientas y automatiza flujos de trabajo con n8n e inteligencia artificial"
description: "Automatizaciones inteligentes para empresas. Conectamos tus aplicaciones y automatizamos procesos con n8n e IA. Ahorra horas de trabajo manual cada semana."
heroCta: "Solicitar Consultoría"
heroCtaHref: "/consultoria/"
features:
  - title: "Automatización con n8n"
    description: "Flujos de trabajo que conectan tus apps sin código: CRM, email, facturación, etc."
    icon: "git-branch"
  - title: "IA en tus procesos"
    description: "Integración de ChatGPT, Claude y otros modelos de IA en tus automatizaciones."
    icon: "cpu"
  - title: "Integración de sistemas"
    description: "Conectamos herramientas que no se hablan entre sí para un flujo de datos unificado."
    icon: "link"
  - title: "Notificaciones inteligentes"
    description: "Alertas automáticas por email, WhatsApp o Slack basadas en eventos de tu negocio."
    icon: "bell"
  - title: "Reporting automatizado"
    description: "Informes que se generan solos con datos de múltiples fuentes."
    icon: "file-text"
  - title: "Mantenimiento y soporte"
    description: "Monitorizamos y mejoramos tus automatizaciones de forma continua."
    icon: "tool"
benefits:
  - "Ahorra decenas de horas de trabajo manual cada mes"
  - "Elimina errores humanos en procesos repetitivos"
  - "Escala operaciones sin contratar más personal"
  - "Integración nativa con +300 aplicaciones via n8n"
  - "Puesta en marcha rápida, primeras automatizaciones en días"
  - "ROI medible desde las primeras semanas"
---
```

**google-negocios.mdx:**
```mdx
---
title: "Google para Negocios"
subtitle: "Optimiza tu Google Business Profile y domina el mapa local"
description: "Optimización de Google Business Profile (Google My Business) para negocios. Aparece en Google Maps y atrae más clientes locales con tu ficha de negocio."
heroCta: "Optimizar mi Ficha"
heroCtaHref: "/consultoria/"
features:
  - title: "Optimización de ficha"
    description: "Configuración completa de tu perfil de Google Business Profile para máximo rendimiento."
    icon: "settings"
  - title: "Publicaciones y novedades"
    description: "Contenido regular en tu ficha para mantenerla activa y atractiva."
    icon: "edit"
  - title: "Gestión de reseñas"
    description: "Estrategia para conseguir reseñas positivas y gestionar las negativas."
    icon: "star"
  - title: "Fotos y contenido visual"
    description: "Fotografía profesional y optimización de imágenes para tu ficha."
    icon: "camera"
  - title: "Métricas e informes"
    description: "Análisis de visitas, llamadas, direcciones y consultas desde tu ficha."
    icon: "chart"
  - title: "Productos y servicios"
    description: "Catálogo optimizado con precios y descripciones para atraer más clics."
    icon: "package"
benefits:
  - "Aparece en el mapa de Google cuando te buscan"
  - "Atrae clientes listos para comprar en tu zona"
  - "Consigue más llamadas, visitas y direcciones a tu negocio"
  - "Destaca frente a competidores con fichas mal optimizadas"
  - "Gestión profesional sin que tú tengas que preocuparte"
  - "Resultados visibles desde el primer mes"
---
```

**posicionamiento-web-asturias.mdx:**
```mdx
---
title: "Posicionamiento Web Asturias"
subtitle: "Posiciona tu negocio en Google y llega a clientes en toda Asturias"
description: "Posicionamiento web en Asturias para PYMES y negocios locales. Estrategias SEO que te llevan a la primera página de Google en Gijón, Oviedo, Avilés y toda la región."
heroCta: "Solicitar Análisis Gratis"
heroCtaHref: "/consultoria/"
features:
  - title: "Auditoría SEO completa"
    description: "Análisis técnico, on-page y de competencia de tu web y sector."
    icon: "search"
  - title: "SEO On-Page Asturias"
    description: "Optimización de contenidos con palabras clave locales de Asturias."
    icon: "code"
  - title: "SEO Técnico"
    description: "Velocidad, estructura, indexación y todos los factores técnicos que Google valora."
    icon: "settings"
  - title: "Contenido SEO local"
    description: "Creación de páginas y artículos optimizados para búsquedas en Asturias."
    icon: "edit"
  - title: "Link building local"
    description: "Estrategia de enlaces desde medios, directorios y empresas de Asturias."
    icon: "link"
  - title: "Informes de resultados"
    description: "Dashboard mensual con evolución de rankings, tráfico y conversiones."
    icon: "chart"
benefits:
  - "Primera página de Google en búsquedas de tu sector"
  - "Más tráfico cualificado a tu web desde Asturias"
  - "Estrategia adaptada al mercado y competencia local"
  - "SEO white-hat que cumple las directrices de Google"
  - "Resultados sostenibles a largo plazo"
  - "Consultoría continua con un equipo local en Gijón"
faq:
  - q: "¿En cuánto tiempo veré resultados?"
    a: "Los primeros resultados en SEO suelen verse entre 3 y 6 meses, aunque depende de la competencia de tu sector en Asturias y del estado actual de tu web."
  - q: "¿Hacéis SEO para negocios de cualquier parte de Asturias?"
    a: "Sí, trabajamos con negocios de Gijón, Oviedo, Avilés, Mieres, Langreo, Villaviciosa y cualquier localidad de Asturias."
  - q: "¿Qué diferencia hay entre SEO y SEM?"
    a: "El SEO (orgánico) genera resultados a largo plazo sin pagar por clic. El SEM (anuncios) es inmediato pero pagas por cada visita. Lo ideal es combinar ambos."
relatedServices:
  - "seo-local-gijon"
  - "seo-local-oviedo"
  - "google-negocios"
---
```

- [ ] **Step 4: Commit**

```bash
git add src/content/
git commit -m "feat: add all MDX content — home + 9 servicios from WordPress XML"
```

---

### Task 14: Homepage — index.astro

**Files:**
- Create: `src/pages/index.astro`

- [ ] **Step 1: Crear index.astro**

```astro
---
import BaseLayout from '../layouts/BaseLayout.astro';
import HeroSection from '../components/HeroSection.astro';
import ServicesGrid from '../components/ServicesGrid.astro';
import AboutSection from '../components/AboutSection.astro';
import StatsCounter from '../components/StatsCounter.astro';
import WhyChooseUs from '../components/WhyChooseUs.astro';
import FinalCTA from '../components/FinalCTA.astro';
import { SITE } from '../lib/constants';
import { getCollection } from 'astro:content';

const servicios = await getCollection('servicios');

const schema = {
  '@context': 'https://schema.org',
  '@graph': [
    {
      '@type': 'LocalBusiness',
      '@id': `${SITE.url}/#business`,
      name: SITE.name,
      url: SITE.url,
      description: SITE.defaultDescription,
      slogan: SITE.slogan,
      foundingDate: '2014',
      image: `${SITE.url}/images/cropped-pymempresas-logo-4k__1_-removebg-preview.png`,
      address: {
        '@type': 'PostalAddress',
        streetAddress: 'C. Rodríguez San Pedro, 12',
        addressLocality: 'Gijón',
        addressRegion: 'Asturias',
        postalCode: '33206',
        addressCountry: 'ES',
      },
      telephone: '+34684620040',
      email: 'info@pymempresas.com',
      sameAs: ['https://www.linkedin.com/in/arturovieiros/'],
    },
  ],
};
---

<BaseLayout
  metaTitle={SITE.defaultTitle}
  metaDescription={SITE.defaultDescription}
  ogImage={SITE.ogImage}
  ogType="website"
  schema={schema}
>
  <HeroSection
    title="Posicionamiento WEB SEO en Gijón, Oviedo y Avilés: posicionamos tu negocio antes que tu competencia."
    subtitle="Tu negocio merece estar en Google cuando tus clientes te buscan. Somos especialistas en SEO local para PYMES en Asturias. Te ayudamos a llegar a más clientes, aumentar tus ventas y construir una presencia digital sólida."
    cta="Solicitar Consultoría Gratis"
    ctaHref="/consultoria/"
    ctaSecondary="Ver Servicios"
    ctaSecondaryHref="/#servicios"
    badge="Agencia de SEO Local en Asturias"
    checks={[
      "Resultados en Google garantizados",
      "Clientes locales cualificados",
      "Estrategias personalizadas para PYMES",
    ]}
    bgImage="/images/hero-bg-DF654TP8.jpg"
  />

  <ServicesGrid servicios={servicios} />

  <AboutSection />

  <StatsCounter />

  <WhyChooseUs />

  <FinalCTA />
</BaseLayout>
```

- [ ] **Step 2: Commit**

```bash
git add src/pages/index.astro
git commit -m "feat: add homepage — Hero, Services, About, Stats, WhyChooseUs, FinalCTA"
```

---

### Task 15: Template de servicios — [slug].astro

**Files:**
- Create: `src/pages/[slug].astro`, `src/components/Breadcrumbs.astro`

- [ ] **Step 1: Crear Breadcrumbs.astro**

```astro
---
interface Crumb {
  label: string;
  href?: string;
}

interface Props {
  items: Crumb[];
}

const { items } = Astro.props;
---

<nav aria-label="Breadcrumb" class="py-4">
  <ol class="flex items-center gap-2 text-sm text-white/50">
    {items.map((item, i) => (
      <li class="flex items-center gap-2">
        {i > 0 && (
          <svg class="w-3 h-3 text-white/30" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 18l6-6-6-6"/></svg>
        )}
        {item.href ? (
          <a href={item.href} class="hover:text-orange transition-colors">{item.label}</a>
        ) : (
          <span class="text-white/80">{item.label}</span>
        )}
      </li>
    ))}
  </ol>
</nav>
```

- [ ] **Step 2: Crear [slug].astro**

```astro
---
import { getCollection } from 'astro:content';
import BaseLayout from '../layouts/BaseLayout.astro';
import HeroSection from '../components/HeroSection.astro';
import Breadcrumbs from '../components/Breadcrumbs.astro';
import FinalCTA from '../components/FinalCTA.astro';
import { SITE } from '../lib/constants';

export async function getStaticPaths() {
  const servicios = await getCollection('servicios');
  return servicios.map((s) => ({
    params: { slug: s.slug },
    props: { servicio: s },
  }));
}

const { servicio } = Astro.props;
const { data } = servicio;

const schema = {
  '@context': 'https://schema.org',
  '@graph': [
    {
      '@type': 'Service',
      name: data.title,
      provider: { '@type': 'LocalBusiness', name: SITE.name },
      description: data.description,
      areaServed: { '@type': 'City', name: 'Gijón' },
      ...(data.faq && {
        hasFAQPage: {
          '@type': 'FAQPage',
          mainEntity: data.faq.map((f) => ({
            '@type': 'Question',
            name: f.q,
            acceptedAnswer: { '@type': 'Answer', text: f.a },
          })),
        },
      }),
    },
    {
      '@type': 'BreadcrumbList',
      itemListElement: [
        { '@type': 'ListItem', position: 1, name: 'Inicio', item: SITE.url },
        { '@type': 'ListItem', position: 2, name: data.title },
      ],
    },
    ...(data.schemaOverrides ? [data.schemaOverrides] : []),
  ],
};
---

<BaseLayout
  metaTitle={data.title}
  metaDescription={data.description}
  ogImage={data.ogImage}
  ogType="article"
  canonicalURL={new URL(`/${servicio.slug}/`, Astro.site).href}
  schema={schema}
>
  <HeroSection
    title={data.title}
    subtitle={data.subtitle}
    cta={data.heroCta}
    ctaHref={data.heroCtaHref}
    badge={data.badge}
    checks={data.heroChecks}
    bgImage={data.heroBgImage}
  />

  <div class="container">
    <Breadcrumbs
      items={[
        { label: 'Inicio', href: '/' },
        { label: data.title },
      ]}
    />
  </div>

  <!-- Features -->
  <section class="section bg-black">
    <div class="container">
      <h2 class="text-3xl font-bold text-white text-center mb-12">¿Qué incluye?</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {data.features.map((f) => (
          <div class="bg-card rounded-xl p-6 border border-white/5">
            <div class="w-10 h-10 bg-orange/10 rounded-lg flex items-center justify-center mb-4">
              <svg class="w-5 h-5 text-orange" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5"/><path d="M2 12l10 5 10-5"/>
              </svg>
            </div>
            <h3 class="font-bold text-white mb-2">{f.title}</h3>
            <p class="text-sm text-white/60 leading-relaxed">{f.description}</p>
          </div>
        ))}
      </div>
    </div>
  </section>

  <!-- Benefits -->
  <section class="section bg-gray-light">
    <div class="container">
      <h2 class="text-3xl font-bold text-black text-center mb-12">Beneficios</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 max-w-[800px] mx-auto">
        {data.benefits.map((b) => (
          <div class="flex items-start gap-3 bg-white rounded-xl p-4 shadow-sm">
            <svg class="w-5 h-5 text-orange shrink-0 mt-0.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><path d="M5 13l4 4L19 7"/></svg>
            <span class="text-black/80 text-sm">{b}</span>
          </div>
        ))}
      </div>
    </div>
  </section>

  <!-- FAQ -->
  {data.faq && data.faq.length > 0 && (
    <section class="section bg-black">
      <div class="container max-w-[800px]">
        <h2 class="text-3xl font-bold text-white text-center mb-12">Preguntas Frecuentes</h2>
        <div class="space-y-3">
          {data.faq.map((item) => (
            <details class="bg-card rounded-xl border border-white/5 group">
              <summary class="px-6 py-4 cursor-pointer list-none font-medium text-white group-hover:text-orange transition-colors flex items-center justify-between">
                {item.q}
                <svg class="w-4 h-4 shrink-0 group-open:rotate-180 transition-transform" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg>
              </summary>
              <div class="px-6 pb-4 text-sm text-white/60 leading-relaxed">{item.a}</div>
            </details>
          ))}
        </div>
      </div>
    </section>
  )}

  <!-- Related Services -->
  {
    data.relatedServices && data.relatedServices.length > 0 && (
      <section class="section bg-gray-light">
        <div class="container">
          <h2 class="text-3xl font-bold text-black text-center mb-10">Servicios relacionados</h2>
          <div class="flex flex-wrap justify-center gap-4">
            {data.relatedServices.map((slug: string) => (
              <a href={`/${slug}/`} class="inline-flex items-center bg-white rounded-xl px-5 py-3 border border-gray-200 hover:border-orange hover:text-orange transition-all text-sm font-medium text-black">
                {slug.split('-').map((w: string) => w.charAt(0).toUpperCase() + w.slice(1)).join(' ')}
                <svg class="w-4 h-4 ml-2" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
              </a>
            ))}
          </div>
        </div>
      </section>
    )
  }

  <FinalCTA />
</BaseLayout>
```

- [ ] **Step 3: Commit**

```bash
git add src/pages/[slug].astro src/components/Breadcrumbs.astro
git commit -m "feat: add servicio template + Breadcrumbs — features, benefits, FAQ, related"
```

---

### Task 16: Páginas estáticas — Contacto, Consultoría, Privacidad, 404

**Files:**
- Create: `src/components/ContactForm.astro`, `src/pages/contacto.astro`, `src/pages/consultoria.astro`, `src/pages/politica-privacidad.astro`, `src/pages/404.astro`

- [ ] **Step 1: Crear ContactForm.astro**

```astro
---
const n8nUrl = import.meta.env.N8N_WEBHOOK_URL ?? '';
---
<form id="contact-form" class="space-y-5" method="POST">
  <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
    <div>
      <label for="nombre" class="block text-sm font-medium text-white mb-1.5">Nombre *</label>
      <input type="text" id="nombre" name="nombre" required
        class="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-3 text-white text-sm focus:border-orange focus:outline-none transition-colors placeholder:text-white/30"
        placeholder="Tu nombre" />
    </div>
    <div>
      <label for="email" class="block text-sm font-medium text-white mb-1.5">Email *</label>
      <input type="email" id="email" name="email" required
        class="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-3 text-white text-sm focus:border-orange focus:outline-none transition-colors placeholder:text-white/30"
        placeholder="tu@email.com" />
    </div>
  </div>
  <div>
    <label for="telefono" class="block text-sm font-medium text-white mb-1.5">Teléfono</label>
    <input type="tel" id="telefono" name="telefono"
      class="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-3 text-white text-sm focus:border-orange focus:outline-none transition-colors placeholder:text-white/30"
      placeholder="+34 600 000 000" />
  </div>
  <div>
    <label for="asunto" class="block text-sm font-medium text-white mb-1.5">Asunto *</label>
    <input type="text" id="asunto" name="asunto" required
      class="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-3 text-white text-sm focus:border-orange focus:outline-none transition-colors placeholder:text-white/30"
      placeholder="¿En qué podemos ayudarte?" />
  </div>
  <div>
    <label for="mensaje" class="block text-sm font-medium text-white mb-1.5">Mensaje *</label>
    <textarea id="mensaje" name="mensaje" rows="4" required
      class="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-3 text-white text-sm focus:border-orange focus:outline-none transition-colors placeholder:text-white/30 resize-none"
      placeholder="Cuéntanos tu proyecto..."></textarea>
  </div>
  <button type="submit"
    class="w-full bg-gradient-to-br from-orange to-orange-dark text-black font-semibold text-[15px] px-8 py-3.5 rounded-[10px] shadow-[0_4px_15px_rgba(245,166,35,0.4)] hover:-translate-y-0.5 hover:shadow-[0_6px_25px_rgba(245,166,35,0.6)] transition-all duration-300">
    Enviar Mensaje
  </button>
  <div id="form-status" class="hidden text-sm text-center"></div>
</form>

<script>
  const form = document.getElementById('contact-form') as HTMLFormElement;
  const status = document.getElementById('form-status')!;

  form?.addEventListener('submit', async (e) => {
    e.preventDefault();
    status.classList.add('hidden');

    const data = Object.fromEntries(new FormData(form));
    const url = '${n8nUrl}';

    if (!url) {
      status.textContent = 'Error de configuración. Contacta por email.';
      status.className = 'text-sm text-center text-red-400 mt-4';
      return;
    }

    try {
      const res = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ...data, origen: window.location.href }),
      });

      if (res.ok) {
        status.textContent = '¡Mensaje enviado! Te responderemos en menos de 24 horas.';
        status.className = 'text-sm text-center text-green-400 mt-4';
        form.reset();
      } else {
        throw new Error('Server error');
      }
    } catch {
      status.textContent = 'Error al enviar. Inténtalo de nuevo o escríbenos a info@pymempresas.com.';
      status.className = 'text-sm text-center text-red-400 mt-4';
    }
  });
</script>
```

- [ ] **Step 2: Crear contacto.astro**

```astro
---
import BaseLayout from '../layouts/BaseLayout.astro';
import ContactForm from '../components/ContactForm.astro';
import { CONTACT, SITE } from '../lib/constants';

const schema = {
  '@context': 'https://schema.org',
  '@type': 'ContactPage',
  name: 'Contacto — PYMEMPRESAS',
  description: 'Contacta con PYMEMPRESAS para tu consultoría gratuita de SEO y marketing digital en Asturias.',
};
---

<BaseLayout
  metaTitle="Contacto"
  metaDescription="Contacta con PYMEMPRESAS. Solicita tu consultoría gratuita de SEO y marketing digital en Gijón, Asturias."
  schema={schema}
>
  <section class="section bg-black pt-32">
    <div class="container">
      <div class="max-w-[600px] mx-auto">
        <span class="text-orange text-sm font-semibold uppercase tracking-wider">Contacto</span>
        <h1 class="text-3xl font-bold text-white mt-2 mb-4">Hablemos de tu proyecto</h1>
        <p class="text-white/60 mb-10 leading-relaxed">
          Cuéntanos qué necesitas y te responderemos en menos de 24 horas con una propuesta personalizada y sin compromiso.
        </p>

        <ContactForm />

        <div class="mt-12 grid grid-cols-1 sm:grid-cols-3 gap-6 text-center">
          <div class="bg-card rounded-xl p-5 border border-white/5">
            <svg class="w-6 h-6 text-orange mx-auto mb-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
            <p class="text-sm font-medium text-white">Teléfono</p>
            <a href={`tel:${CONTACT.phone}`} class="text-sm text-white/50 hover:text-orange transition-colors">{CONTACT.phone}</a>
          </div>
          <div class="bg-card rounded-xl p-5 border border-white/5">
            <svg class="w-6 h-6 text-orange mx-auto mb-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>
            <p class="text-sm font-medium text-white">Email</p>
            <a href={`mailto:${CONTACT.email}`} class="text-sm text-white/50 hover:text-orange transition-colors">{CONTACT.email}</a>
          </div>
          <div class="bg-card rounded-xl p-5 border border-white/5">
            <svg class="w-6 h-6 text-orange mx-auto mb-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
            <p class="text-sm font-medium text-white">Oficina</p>
            <p class="text-sm text-white/50">{CONTACT.address}</p>
          </div>
        </div>
      </div>
    </div>
  </section>
</BaseLayout>
```

- [ ] **Step 3: Crear consultoria.astro**

```astro
---
import BaseLayout from '../layouts/BaseLayout.astro';
import ContactForm from '../components/ContactForm.astro';
---

<BaseLayout
  metaTitle="Consultoría Gratis"
  metaDescription="Solicita tu consultoría gratuita de SEO y marketing digital. Te mostramos cómo mejorar tu presencia online sin compromiso."
>
  <section class="section bg-black pt-32">
    <div class="container">
      <div class="max-w-[600px] mx-auto">
        <span class="text-orange text-sm font-semibold uppercase tracking-wider">Consultoría Gratis</span>
        <h1 class="text-3xl font-bold text-white mt-2 mb-4">Descubre cómo hacer crecer tu negocio online</h1>
        <p class="text-white/60 mb-10 leading-relaxed">
          Solicita tu consultoría gratuita y te mostraremos exactamente qué necesita tu negocio
          para atraer más clientes desde Google. Sin compromiso, sin permanencia.
        </p>

        <div class="bg-card rounded-xl p-6 border border-white/5 mb-10">
          <h3 class="font-bold text-white mb-4">¿Qué incluye?</h3>
          <ul class="space-y-3">
            {[
              'Análisis de tu presencia online actual',
              'Estudio de tu competencia en Google',
              'Plan de acción personalizado para tu negocio',
              'Presupuesto detallado sin compromiso',
            ].map((item) => (
              <li class="flex items-start gap-3 text-sm text-white/70">
                <svg class="w-5 h-5 text-orange shrink-0 mt-px" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><path d="M5 13l4 4L19 7"/></svg>
                {item}
              </li>
            ))}
          </ul>
        </div>

        <ContactForm />
      </div>
    </div>
  </section>
</BaseLayout>
```

- [ ] **Step 4: Crear politica-privacidad.astro**

```astro
---
import BaseLayout from '../layouts/BaseLayout.astro';
---

<BaseLayout
  metaTitle="Política de Privacidad"
  metaDescription="Política de privacidad de PYMEMPRESAS. Información sobre el tratamiento de datos personales conforme al RGPD."
  noindex={true}
>
  <section class="section bg-black pt-32">
    <div class="container max-w-[800px]">
      <h1 class="text-3xl font-bold text-white mb-8">Política de Privacidad</h1>
      <div class="prose prose-invert max-w-none text-white/70 leading-relaxed space-y-4">
        <h2 class="text-xl font-bold text-white mt-8 mb-4">1. Responsable del tratamiento</h2>
        <p>
          <strong>PYMEMPRESAS</strong><br/>
          Email: info@pymempresas.com<br/>
          Dirección: C. Rodríguez San Pedro, 12, 33206 Gijón, Asturias
        </p>

        <h2 class="text-xl font-bold text-white mt-8 mb-4">2. Datos recopilados</h2>
        <p>Recopilamos los datos que nos proporcionas a través del formulario de contacto: nombre, email, teléfono y mensaje. También recopilamos datos de navegación anónimos con fines estadísticos.</p>

        <h2 class="text-xl font-bold text-white mt-8 mb-4">3. Finalidad del tratamiento</h2>
        <p>Los datos se utilizan exclusivamente para responder a tus consultas, enviar presupuestos solicitados y mantener la relación comercial contigo. No se utilizarán para fines distintos sin tu consentimiento.</p>

        <h2 class="text-xl font-bold text-white mt-8 mb-4">4. Legitimación</h2>
        <p>El tratamiento de tus datos se basa en el consentimiento que nos prestas al enviar el formulario de contacto (art. 6.1.a RGPD).</p>

        <h2 class="text-xl font-bold text-white mt-8 mb-4">5. Conservación de datos</h2>
        <p>Los datos personales se conservan mientras exista interés mutuo para mantener el fin del tratamiento. Cuando ya no sean necesarios, se suprimirán con medidas de seguridad adecuadas.</p>

        <h2 class="text-xl font-bold text-white mt-8 mb-4">6. Derechos</h2>
        <p>Puedes ejercer tus derechos de acceso, rectificación, supresión, oposición, limitación y portabilidad escribiendo a info@pymempresas.com. También puedes presentar una reclamación ante la AEPD.</p>

        <h2 class="text-xl font-bold text-white mt-8 mb-4">7. Cookies</h2>
        <p>Este sitio utiliza exclusivamente cookies técnicas necesarias para su funcionamiento. No se utilizan cookies de seguimiento ni publicitarias sin consentimiento previo.</p>
      </div>
    </div>
  </section>
</BaseLayout>
```

- [ ] **Step 5: Crear 404.astro**

```astro
---
import BaseLayout from '../layouts/BaseLayout.astro';
---

<BaseLayout
  metaTitle="Página no encontrada"
  metaDescription="La página que buscas no existe."
  noindex={true}
>
  <section class="min-h-[70vh] flex items-center justify-center text-center pt-24">
    <div>
      <span class="text-7xl font-bold text-orange">404</span>
      <h1 class="text-2xl font-bold text-white mt-4 mb-2">Página no encontrada</h1>
      <p class="text-white/50 mb-8">La página que buscas no existe o ha sido movida.</p>
      <a href="/" class="inline-flex items-center bg-gradient-to-br from-orange to-orange-dark text-black font-semibold px-6 py-3 rounded-[10px] shadow-[0_4px_15px_rgba(245,166,35,0.4)] hover:-translate-y-0.5 transition-all duration-300">
        Volver al inicio
      </a>
    </div>
  </section>
</BaseLayout>
```

- [ ] **Step 6: Commit**

```bash
git add src/components/ContactForm.astro src/pages/contacto.astro src/pages/consultoria.astro src/pages/politica-privacidad.astro src/pages/404.astro
git commit -m "feat: add static pages — contacto, consultoria, privacidad, 404 + ContactForm with n8n"
```

---

### Task 17: Cookie Banner

**Files:**
- Create: `src/components/CookieBanner.astro`

- [ ] **Step 1: Crear CookieBanner.astro**

```astro
<div id="cookie-banner" class="hidden fixed bottom-0 left-0 right-0 z-[9999] bg-card border-t border-white/10 backdrop-blur-[20px] shadow-2xl">
  <div class="container py-4 flex flex-col sm:flex-row items-start sm:items-center gap-4">
    <p class="text-sm text-white/70 flex-1">
      Usamos cookies técnicas necesarias para el funcionamiento del sitio. Al continuar navegando aceptas su uso.
    </p>
    <div class="flex items-center gap-3 shrink-0">
      <button id="cookie-reject" class="text-sm text-white/50 hover:text-white px-4 py-2 rounded-lg transition-colors">
        Rechazar
      </button>
      <button id="cookie-accept" class="text-sm bg-gradient-to-br from-orange to-orange-dark text-black font-semibold px-5 py-2.5 rounded-[10px] shadow-[0_4px_15px_rgba(245,166,35,0.4)] hover:-translate-y-0.5 transition-all duration-300">
        Aceptar
      </button>
    </div>
  </div>
</div>

<script>
  const COOKIE_KEY = 'pymempresas-cookie-consent';
  const banner = document.getElementById('cookie-banner')!;

  if (!localStorage.getItem(COOKIE_KEY)) {
    banner.classList.remove('hidden');
  }

  document.getElementById('cookie-accept')?.addEventListener('click', () => {
    localStorage.setItem(COOKIE_KEY, 'accepted');
    banner.classList.add('hidden');
  });

  document.getElementById('cookie-reject')?.addEventListener('click', () => {
    localStorage.setItem(COOKIE_KEY, 'rejected');
    banner.classList.add('hidden');
  });
</script>
```

- [ ] **Step 2: Commit**

```bash
git add src/components/CookieBanner.astro
git commit -m "feat: add CookieBanner — localStorage consent, accept/reject, styled"
```

---

### Task 18: SEO files — Sitemap, Robots.txt, llms.txt

**Files:**
- Create: `src/pages/sitemap.xml.ts`, `src/pages/robots.txt.ts`, `src/pages/llms.txt.ts`

- [ ] **Step 1: Crear sitemap.xml.ts**

```ts
import type { APIRoute } from 'astro';
import { getCollection } from 'astro:content';

export const GET: APIRoute = async ({ site }) => {
  const servicios = await getCollection('servicios');

  const pages = [
    { url: '', lastmod: '2026-05-06' },
    { url: 'consultoria/', lastmod: '2026-05-06' },
    { url: 'contacto/', lastmod: '2026-05-06' },
    { url: 'politica-privacidad/', lastmod: '2026-05-06' },
  ];

  const servicioEntries = servicios.map((s) => ({
    url: `${s.slug}/`,
    lastmod: '2026-05-06',
  }));

  const allUrls = [...pages, ...servicioEntries];

  const sitemap = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${allUrls
  .map(
    (p) => `  <url>
    <loc>${site}${p.url}</loc>
    <lastmod>${p.lastmod}</lastmod>
    <priority>${p.url === '' ? '1.0' : '0.8'}</priority>
  </url>`
  )
  .join('\n')}
</urlset>`;

  return new Response(sitemap, {
    headers: { 'Content-Type': 'application/xml' },
  });
};
```

- [ ] **Step 2: Crear robots.txt.ts**

```ts
import type { APIRoute } from 'astro';

export const GET: APIRoute = ({ site }) => {
  const robots = `User-agent: *
Allow: /
Sitemap: ${site}sitemap.xml

Disallow: /cdn-cgi/
`;

  return new Response(robots, {
    headers: { 'Content-Type': 'text/plain' },
  });
};
```

- [ ] **Step 3: Crear llms.txt.ts**

```ts
import type { APIRoute } from 'astro';
import { getCollection } from 'astro:content';

export const GET: APIRoute = async ({ site }) => {
  const servicios = await getCollection('servicios');

  const lines = [
    `# PYMEMPRESAS`,
    `> Agencia de Marketing Digital en Gijón — SEO Local, Diseño Web, IA para PYMES en Asturias.`,
    '',
    `## Páginas principales`,
    `- [Inicio](${site}): Posicionamiento WEB SEO en Asturias.`,
    `- [Consultoría Gratis](${site}consultoria/): Solicita tu consultoría gratuita.`,
    `- [Contacto](${site}contacto/): Contacta con nosotros.`,
    '',
    `## Servicios`,
    ...servicios.map(
      (s) => `- [${s.data.title}](${site}${s.slug}/): ${s.data.subtitle}.`
    ),
    '',
    `## Contacto`,
    `- Email: info@pymempresas.com`,
    `- Teléfono: +34 684 62 00 40`,
    `- Dirección: C. Rodríguez San Pedro, 12, 33206 Gijón, Asturias`,
    `- Horario: Lun–Vie 9:00–18:00`,
  ].join('\n');

  return new Response(lines, {
    headers: { 'Content-Type': 'text/plain; charset=utf-8' },
  });
};
```

- [ ] **Step 4: Commit**

```bash
git add src/pages/sitemap.xml.ts src/pages/robots.txt.ts src/pages/llms.txt.ts
git commit -m "feat: add SEO files — sitemap.xml, robots.txt, llms.txt"
```

---

### Task 19: Imágenes y assets

**Files:**
- Create: `public/favicon.svg`, `public/og-default.jpg`
- Copy from project root to `public/images/`

- [ ] **Step 1: Crear favicon.svg**

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
  <rect width="32" height="32" rx="6" fill="#0A0A0A"/>
  <text x="16" y="21" font-family="Arial,sans-serif" font-size="16" font-weight="bold" fill="#F5A623" text-anchor="middle">P</text>
</svg>
```

- [ ] **Step 2: Copiar imágenes del proyecto al directorio public**

Run PowerShell:
```powershell
Copy-Item "C:\Users\aviei\Documents\Pymempresas\pymempresas-web\*.png" -Destination "C:\Users\aviei\Documents\Pymempresas\pymempresas-web\public\images\" -ErrorAction SilentlyContinue
Copy-Item "C:\Users\aviei\Documents\Pymempresas\pymempresas-web\*.jpg" -Destination "C:\Users\aviei\Documents\Pymempresas\pymempresas-web\public\images\" -ErrorAction SilentlyContinue
```

- [ ] **Step 3: Crear .gitignore si no existe**

```
node_modules/
dist/
.env
.DS_Store
```

- [ ] **Step 4: Commit**

```bash
git add public/ .gitignore
git commit -m "feat: add favicon, copy images to public/, add .gitignore"
```

---

### Task 20: Build verification

- [ ] **Step 1: Instalar dependencias**  

Run: `npm install`

- [ ] **Step 2: Build del proyecto**  

Run: `npm run build`  
Expected: Build exitoso sin errores. Todos los archivos en `dist/`.

- [ ] **Step 3: Verificar URLs generadas**  

Run: `ls dist/ && ls dist/seo-local-gijon/`  
Expected: Ver `index.html`, `consultoria/`, `contacto/`, `politica-privacidad/`, `seo-local-gijon/`, etc.

- [ ] **Step 4: Verificar sitemap**  

Run: `cat dist/sitemap.xml`  
Expected: XML con todas las URLs del sitio.

- [ ] **Step 5: Verificar llms.txt**  

Run: `cat dist/llms.txt`  
Expected: Texto con todas las páginas y servicios listados.

- [ ] **Step 6: Commit final**  

```bash
git add -A
git commit -m "chore: final build verification — all pages generated correctly"
```
