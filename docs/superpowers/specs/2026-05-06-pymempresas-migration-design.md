# Spec: Migración WordPress a Astro — PYMEMPRESAS

**Fecha:** 2026-05-06
**Dominio:** pymempresas.com
**Objetivo:** Reemplazar WordPress por sitio estático Astro 5

---

## Stack

| Capa | Tecnología |
|------|-----------|
| Framework | Astro 5 |
| CSS | Tailwind CSS 4 |
| Lenguaje | TypeScript |
| Contenido | MDX (content collections) |
| Formulario | n8n webhook (VPS propio) |
| Hosting | Cloudflare Pages |
| Build | 100% estático |

---

## URLs preservadas (indexadas)

Todas las URLs mantienen exactamente el mismo slug de WordPress:

```
/                                          → Home
/seo-local-gijon/                          → Servicio
/seo-local-oviedo/                         → Servicio
/diseno-web-gijon/                         → Servicio
/inteligencia-artificial-empresas/         → Servicio
/formacion-ia-empresas/                    → Servicio
/automatizaciones-con-ia/                  → Servicio
/google-negocios/                          → Servicio
/posicionamiento-web-asturias/             → Servicio
/consultoria/                              → Landing consultoría
/contacto/                                 → Contacto + formulario
/politica-privacidad/                      → Legal
```

Sin cambios de slug. Si falta alguna, se añade antes del deploy.

---

## Estructura del proyecto

```
pymempresas-web/
├── astro.config.mjs
├── tailwind.config.mjs
├── tsconfig.json
├── package.json
├── public/
│   ├── favicon.svg
│   ├── og-default.jpg
│   ├── robots.txt
│   └── images/                    # Imágenes optimizadas
├── src/
│   ├── content/
│   │   ├── servicios/             # 11 MDX (una por servicio)
│   │   ├── home.mdx               # Contenido homepage
│   │   └── config.ts              # Zod schemas
│   ├── pages/
│   │   ├── index.astro            # Home
│   │   ├── servicios/[slug].astro # Template servicios
│   │   ├── consultoria.astro
│   │   ├── contacto.astro
│   │   ├── politica-privacidad.astro
│   │   ├── 404.astro
│   │   ├── robots.txt.ts
│   │   └── sitemap.xml.ts
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
│   │   └── SEO.astro
│   ├── lib/
│   │   ├── constants.ts
│   │   └── n8n.ts
│   └── styles/
│       └── global.css
```

---

## Sistema de diseño

### Colores

| Token | Hex | Uso |
|-------|-----|-----|
| Negro | #0A0A0A | Fondos principales, header, footer |
| Card BG | #111111 | Tarjetas de servicio, overlays |
| Naranja | #F5A623 | CTAs, acentos, hover states, íconos |
| Gris claro | #F5F5F5 | Fondos de sección alternos |
| Blanco | #FFFFFF | Texto sobre fondos oscuros |

### Tipografía

System UI stack: `-apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica Neue, Arial, sans-serif`

Cero Google Fonts. Cero requests externas de fuentes.

### Botones

- **Primario:** Gradiente #F5A623 → #E89B1F, texto negro, box-shadow glow
- **Secundario:** Fondo rgba(255,255,255,0.1), borde blanco 0.3, backdrop-blur
- **Hover:** translateY(-2px) + shadow expand

---

## Content Collections — Schema

### Servicios

```ts
servicios: defineCollection({
  schema: z.object({
    title: z.string(),
    subtitle: z.string(),
    description: z.string(),
    heroCta: z.string(),
    heroCtaHref: z.string(),
    features: z.array(z.object({
      title: z.string(),
      description: z.string(),
      icon: z.string(),
    })),
    benefits: z.array(z.string()),
    faq: z.array(z.object({ q: z.string(), a: z.string() })).optional(),
    relatedServices: z.array(z.string()).max(3).optional(),
    ogImage: z.string().optional(),
  }),
});
```

---

## Componentes — Props contracts

### BaseLayout
```
metaTitle, metaDescription, ogImage?, schema?, noindex?
```

### Header
Sin props. Nav items desde `constants.ts`.

### Footer
Sin props. Datos desde `constants.ts`.

### HeroSection
```
title, subtitle, cta, ctaHref, ctaSecondary?, ctaSecondaryHref?,
badge?, checks?[], bgImage
```

### ServicesGrid
```
servicios: CollectionEntry<"servicios">[]
```

### ContactForm
Sin props. POST a n8n webhook. Validación HTML5 + JS ligera.

### CookieBanner
Sin props. Auto-detecta necesidad. Guarda preferencia en localStorage.

---

## Formulario de contacto

- POST a webhook n8n (URL en variable de entorno `N8N_WEBHOOK_URL`)
- Campos: nombre, email, teléfono, asunto, mensaje
- Validación cliente: HTML5 required + pattern email
- Toast nativo de confirmación/error
- Sin estado React — vanilla JS

---

## SEO — Mejoras sobre WordPress

| Elemento | WordPress actual | Astro nuevo |
|----------|-----------------|-------------|
| Meta tags | OK | OK + mejorados |
| Schema | Solo Organization | LocalBusiness + Service + FAQ + BreadcrumbList + Review |
| OG Image | Logo genérico en todas | Imagen 1200x630 por página |
| llms.txt | No existe | Archivo para AI search |
| Sitemap | WP genérico | XML + lastmod + todas URLs |
| CSS | Múltiples archivos | Todo inline (<10KB) |
| HTML size | ~194KB | ~40-60KB |
| TTFB | 94ms (con cache) | <50ms (estático) |
| Robots.txt | WP genérico | Optimizado |
| Generator tag | Expuesto | Eliminado |

---

## Cookie Banner

- Personalizado, sin dependencias
- Overlay inferior fijo
- 3 botones: Aceptar / Rechazar / Configurar
- localStorage, 365 días
- Estilo consistente con diseño negro+naranja

---

## Deploy — Cloudflare Pages

1. Conectar repo GitHub
2. Build: `npm run build`
3. Output: `dist/`
4. Variable: `N8N_WEBHOOK_URL`
5. DNS: apuntar pymempresas.com a Cloudflare
6. SSL automático
