# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Git — IMPORTANTE
El repo raíz es `C:\Users\aviei` (monorepo con todos los proyectos). Este proyecto vive en `Documents/Pymempresas/pymempresas-web/`. Siempre hacer `git add` y `git commit` scoped a esta carpeta para no mezclar cambios de otros proyectos:
```bash
git add Documents/Pymempresas/pymempresas-web/<path>
```
O ejecutar comandos git desde este directorio con rutas relativas.

## Commands
```bash
npm run dev      # http://localhost:4321
npm run build    # 17 páginas → dist/
npm run preview
```

## Stack
Astro 5.14 + Tailwind CSS 4.1 + MDX. 100% estático. Dependencias: `@astrojs/mdx`, `sharp`, `@tailwindcss/vite`. Inter (Google Fonts) + Tabler Icons CDN. ViewTransitions activado en BaseLayout.

## URLs
`/` — home con hero full-width, servicios, about, stats, ventajas, CTA
Servicios: `/seo-local-gijon/` `/seo-local-oviedo/` `/diseno-web-gijon/` `/posicionamiento-web-asturias/` `/inteligencia-artificial-empresas/` `/formacion-ia-empresas/` `/automatizaciones-con-ia/` `/google-negocios/`
Formularios: `/consultoria/` `/contacto/`
Blog: `/blog/` `/[slug]/`
Legales: `/aviso-legal/` `/politica-privacidad/`
Técnicas: `/sitemap.xml` `/robots.txt` `/llms.txt` (generadas dinámicamente en build)

## Arquitectura

### Layouts
`src/layouts/BaseLayout.astro` — Shell global. Props: `metaTitle`, `metaDescription`, `canonicalURL?`, `ogImage?`, `ogType?`, `noindex?`, `schema?`, `bodyTheme?`. Incluye `<Header />`, `<slot />`, `<Footer />`, `<CookieBanner />`, `<SEO />`, ViewTransitions. El `bodyTheme` controla el fondo: `'dark'` (default, bg-black text-white) o `'light'` (bg-white text-black). Blog y consultoría usan light.

### Páginas
Cada `.astro` en `src/pages/` es standalone. Las páginas de servicio (seo-local-gijon, diseno-web-gijon, etc.) siguen este patrón:
1. Cargar MDX de `src/content/servicios/<slug>.mdx` vía `getCollection('servicios')`
2. Schema LocalBusiness o Service en la página
3. Hero con bg-image + overlay + badge + checks + botones
4. Secciones de features, benefits, FAQ (del frontmatter MDX)
5. FinalCTA al final

El blog usa `[slug].astro` que resuelve posts de `src/content/blog/`.

### Content Collections (`src/content/config.ts`)
- **servicios** — título, subtítulo, features (iconos), benefits, FAQ, relatedServices, heroChecks
- **home** — hero, services grid, about, stats, advantages. Datos en `src/content/home/home.mdx`
- **blog** — title, description, date, author, tags, image, authorLinkedin, authorTwitter, authorBio, authorImage

### Componentes clave
- `SEO.astro` — meta tags + OG + Twitter Card + JSON-LD schema. Default OG image es `/og-default.svg`.
- `ContactForm.astro` / `ConsultoriaForm.astro` — formularios con webhooks n8n hardcodeados. `import.meta.env` no funciona en build estático.
- `CookieBanner.astro` — modal glassmorphism con toggles de categorías
- Blog (10 componentes en `src/components/blog/`): ArticleCard, ArticleHero, ArticleBody, BlogHero, BlogGrid, FeaturedCard, ReadingProgress, RelatedArticles, ScrollReveal, ShareRow

### Estilos
`src/styles/global.css` — Tailwind `@theme` con design tokens (colors, font). Utilidades de animación: scroll-reveal, stagger-children, drop cap, pull quotes, callouts, wide images. `ArticleBody` usa `is:global` para estilos de prosa.

## Diseño
Negro `#0A0A0A` + Naranja `#F5A623`. BodyTheme controla modo oscuro/claro por página. Hero sections usan `100vw` + `margin-left: -50vw` para romper el contenedor de Astro. Callouts en blog: `<div class="article-callout"><div class="callout-icon"><i class="ti ti-bolt"></i></div><div class="callout-body">...</div></div>`.

## Formularios (webhooks hardcodeados)
- **Contacto:** `https://n8n.vieirox.es/webhook/contact-form` (workflow: `kSGMTFtlZHxiP4QK`)
- **Consultoría:** `https://n8n.vieirox.es/webhook/consultoria-form` (workflow: `No7xdiDEIKkQBDhh`)
- Van a Gmail + Google Sheets vía n8n

## n8n
Instancia: `https://n8n.vieirox.es`. Workflows JSON en `n8n/`. Credenciales: Gmail OAuth2 `dYf4b9b9QiLUD45M`, Google Sheets OAuth2 `pZEaWkIrQCaEMNed`, Project owner `CBRQ9ec6kcXUv4bC`.

## Deploy
- **Producción:** `https://pymempresas.com` — LiteSpeed, cPanel en `https://pymempresas.com:2083`
- **cPanel API:** `uncredit` / `n0ses@be71` — usar solo `execute/Fileman/list_files` y `execute/Fileman/upload_files` (multipart POST). No usar `savefile`.
- **GitHub:** `https://github.com/avieirox/pymempresas.git`
- **Flujo:** build local → subir archivos modificados vía cPanel `upload_files`
- **Git auto-deploy en cPanel:** NO configurado. Configurar manualmente en cPanel → Git Version Control.

## Blog
Posts en `src/content/blog/` como MDX. Schema: title, description, date, author, tags, image, authorLinkedin, authorTwitter, authorBio, authorImage. Script `scripts/import-blog.mjs` para importar desde CSV (columnas: Título, Fase, Pilar, Slug, Publicar, Fecha, Descripción).

## Interlinking
Crear contenido nuevo → consultar `docs/INTERLINKING.md`. Datos GSC en `pymempresas.com_csv-gsc/`: 17K impresiones, CTR 0.01%, posiciones 55-97. Anchors deben usar queries exactas del CSV.

## SEO — Pendiente
1. Crear `og-default.jpg` 1200x630 en `public/` (actualmente hay `og-default.svg`)
2. Añadir schema Service a automatizaciones y contacto
3. Cambiar `ComputerRepair` por `ProfessionalService` en schema IA
4. Optimizar logos (WebP, ~20KB)
