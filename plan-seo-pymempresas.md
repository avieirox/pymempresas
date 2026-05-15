# Plan de mejoras SEO — pymempresas.com
> Generado a partir de datos de Google Search Console (feb–may 2026) y Screaming Frog.
> Este documento es una instrucción directa para Claude Code. Ejecutar los cambios en orden de prioridad.

---

## Contexto del proyecto

- Web en **Astro** (estática)
- Dominio: `https://pymempresas.com`
- Nicho: agencia SEO y posicionamiento web local en Asturias (Gijón, Oviedo, Avilés)
- Problema principal: 12.500 impresiones en 90 días pero solo 7 clics — posición media 65, demasiado lejos de página 1

---

## PRIORIDAD 1 — Correcciones técnicas on-page (hacer primero)

### 1.1 Títulos que superan 60 caracteres — truncados en Google

Corregir los siguientes `<title>` en sus respectivos archivos de página Astro:

| Página | Título actual (chars) | Título propuesto |
|--------|----------------------|-----------------|
| `/posicionamiento-web-asturias/` | `Posicionamiento Web SEO + LLM | Aparece en Google y ChatGPT | PYMEMPRESAS` (73) | `Posicionamiento Web en Asturias | SEO + IA | PYMEMPRESAS` (57) |
| `/formacion-ia-empresas/` | `Formación en Inteligencia Artificial para Empresas en Gijón | PYMEMPRESAS` (73) | `Formación en IA para Empresas en Gijón | PYMEMPRESAS` (52) |
| `/automatizaciones-con-ia/` | `Automatizaciones con Inteligencia Artificial para Empresas en Gijón | PYMEMPRESAS` (81) | `Automatizaciones con IA para Empresas en Gijón | PYMEMPRESAS` (60) |
| `/google-negocios/` | `Google para Negocios - Optimización de Perfil de Empresa | PYMEMPRESAS` (70) | `Google My Business en Asturias — Optimización | PYMEMPRESAS` (59) |

**Regla:** máximo 60 caracteres incluyendo el separador y la marca.

---

### 1.2 Meta descriptions fuera de rango

Ajustar las siguientes meta descriptions. Rango óptimo: 140–155 caracteres.

**`/automatizaciones-con-ia/`** — actual 179 chars, recortar a:
```
Automatiza tu negocio con IA en Gijón y Asturias. Ahorra tiempo, reduce errores y aumenta la productividad. Soluciones personalizadas para empresas.
```
(149 chars)

**`/`** (home) — actual 168 chars, recortar a:
```
Agencia SEO Local en Asturias con más de 10 años de experiencia. Posicionamos tu negocio en Google. Consultoría gratuita sin compromiso.
```
(137 chars)

---

### 1.3 Snippet de `/google-negocios/` — posición 11, cero clics

Esta página aparece en posición media 11 (casi en la primera página) pero no recibe ningún clic. El problema es el snippet. Actualizar:

**Title actual:** `Google para Negocios - Optimización de Perfil de Empresa | PYMEMPRESAS`
**Title nuevo:** `Google My Business en Asturias — Optimización | PYMEMPRESAS`

**Meta actual:** `Especialistas en optimizar tu Perfil de Empresa de Google (Google My Business) en Asturias. Aparece en Google Maps y domina las búsquedas locales. Desde 297€/mes.`
**Meta nueva:** `¿Tu negocio no aparece en Google Maps? Lo optimizamos. Más reseñas, más llamadas, más clientes en Gijón y Asturias. Primera consulta gratis.`

El cambio clave: añadir una pregunta al inicio de la meta description y un CTA claro. Las preguntas disparan el CTR en snippets de servicios locales.

---

## PRIORIDAD 2 — Refuerzo de páginas estratégicas

### 2.1 `/posicionamiento-web-asturias/` — 5.053 impresiones, posición 72

Es la página con más visibilidad pero peor posición. Necesita refuerzo de contenido.

**Acciones a realizar en el archivo de esta página:**

1. **Añadir sección FAQ** al final de la página con las siguientes preguntas (en formato `<details>` o componente Astro equivalente):
   - ¿Cuánto tarda en funcionar el posicionamiento web?
   - ¿Cuánto cuesta el posicionamiento web en Asturias?
   - ¿Qué diferencia hay entre SEO y posicionamiento web?
   - ¿Necesito una web nueva para posicionarme?
   - ¿Funcionáis solo en Gijón o también en Oviedo y Avilés?

2. **Añadir datos estructurados JSON-LD** de tipo `FAQPage` en el `<head>` de esta página con las preguntas anteriores.

3. **Añadir datos estructurados JSON-LD** de tipo `LocalBusiness` en el `<head>` con:
   ```json
   {
     "@context": "https://schema.org",
     "@type": "LocalBusiness",
     "name": "PYMEMPRESAS",
     "url": "https://pymempresas.com",
     "telephone": "[teléfono actual]",
     "address": {
       "@type": "PostalAddress",
       "addressLocality": "Gijón",
       "addressRegion": "Asturias",
       "addressCountry": "ES"
     },
     "areaServed": ["Gijón", "Oviedo", "Avilés", "Asturias"],
     "priceRange": "€€"
   }
   ```

4. **Aumentar el wordcount** de 1.709 a al menos 2.200 palabras añadiendo:
   - Sección "¿Cómo trabajamos?" con proceso en pasos
   - Sección "Resultados reales" (aunque sean genéricos de sector)
   - La FAQ mencionada arriba

---

### 2.2 `/seo-local-gijon/` y `/seo-local-oviedo/` — páginas con más clics

Estas dos páginas son las que más clics generan (3 y 2 respectivamente) con posiciones 55 y 59. Pequeñas mejoras para empujar a página 1.

**Para ambas páginas:**

1. Añadir la misma estructura de **datos estructurados `LocalBusiness`** descrita en 2.1, cambiando `addressLocality` según corresponda.

2. Añadir **schema `Service`** en JSON-LD:
   ```json
   {
     "@context": "https://schema.org",
     "@type": "Service",
     "name": "SEO Local en Gijón",
     "provider": {
       "@type": "LocalBusiness",
       "name": "PYMEMPRESAS"
     },
     "areaServed": "Gijón",
     "description": "Servicio de SEO Local para negocios y pymes en Gijón..."
   }
   ```

3. En `/seo-local-gijon/`: añadir internamente un enlace a `/posicionamiento-web-asturias/` con anchor text "posicionamiento web en Asturias".

4. En `/seo-local-oviedo/`: añadir internamente un enlace a `/seo-local-gijon/` con anchor text "SEO Local en Gijón".

---

## PRIORIDAD 3 — Nueva página de servicio

### 3.1 Crear `/seo-gijon/` (nueva página)

**Justificación:** Las queries "seo gijón" (283 imp, pos 48), "seo en gijón" (91 imp, pos 37) y "consultor seo gijón" (186 imp, pos 41) tienen volumen real y están en posición 37–48. No existe una página que las capture directamente — `/seo-local-gijon/` va a "SEO Local" pero no a "SEO" a secas. Una página dedicada puede capturar este tráfico.

**Crear el archivo:** `src/pages/seo-gijon.astro` (o la estructura que use el proyecto)

**Especificaciones de contenido:**

- **Title:** `SEO en Gijón — Consultoría y Posicionamiento Web | PYMEMPRESAS` (60 chars)
- **Meta description:** `Consultor SEO en Gijón especializado en negocios locales. Auditoría gratuita, estrategia personalizada y resultados medibles. Más de 10 años de experiencia.` (155 chars)
- **H1:** `Consultor SEO en Gijón`
- **URL:** `/seo-gijon/`

**Estructura de contenido (secciones / H2s):**
1. ¿Qué hace un consultor SEO en Gijón?
2. Servicios SEO para negocios en Gijón
3. ¿Por qué elegir PYMEMPRESAS como tu agencia SEO en Gijón?
4. Proceso de trabajo
5. Preguntas frecuentes sobre SEO en Gijón
6. CTA — Solicita tu auditoría gratuita

**Wordcount objetivo:** mínimo 1.400 palabras.

**Enlazar desde:** home, `/seo-local-gijon/` y `/posicionamiento-web-asturias/`.

---

## PRIORIDAD 4 — Blog: plan de contenidos

El blog está prácticamente vacío (246 palabras en el índice, solo 2 artículos). Es la principal palanca de autoridad temática disponible.

### Artículos a crear (por orden de prioridad)

Crear los siguientes archivos en la carpeta de blog del proyecto:

---

**Artículo 1**
- **Slug:** `/blog/que-es-el-seo-local/`
- **Title:** `Qué es el SEO Local y cómo funciona para negocios en Asturias`
- **Meta:** `Guía completa sobre SEO Local: qué es, cómo funciona y por qué es clave para negocios en Gijón, Oviedo y Asturias. Con ejemplos reales.`
- **H1:** `Qué es el SEO Local y cómo funciona`
- **Wordcount:** 1.500 palabras
- **Keywords objetivo:** "seo local asturias" (296 imp, pos 41), "seo local gijón"
- **Enlazar a:** `/seo-local-gijon/`, `/seo-local-oviedo/`

---

**Artículo 2**
- **Slug:** `/blog/cuanto-cuesta-seo-asturias/`
- **Title:** `¿Cuánto cuesta el SEO en Asturias? Precios reales en 2025`
- **Meta:** `Descubre cuánto cuesta contratar SEO en Asturias. Comparativa de precios, qué incluye cada servicio y cómo elegir sin equivocarte.`
- **H1:** `¿Cuánto cuesta el SEO en Asturias? Precios y qué incluyen`
- **Wordcount:** 1.400 palabras
- **Keywords objetivo:** long-tail de precio SEO, "empresa posicionamiento web asturias" (261 imp)
- **Enlazar a:** `/posicionamiento-web-asturias/`, `/consultoria/`

---

**Artículo 3**
- **Slug:** `/blog/google-my-business-guia/`
- **Title:** `Guía de Google My Business para negocios locales en Asturias`
- **Meta:** `Aprende a optimizar tu ficha de Google My Business paso a paso. Más reseñas, más visibilidad en Maps y más clientes para tu negocio en Asturias.`
- **H1:** `Guía completa de Google My Business para negocios en Asturias`
- **Wordcount:** 1.600 palabras
- **Keywords objetivo:** "google my business asturias", "perfil empresa google"
- **Enlazar a:** `/google-negocios/`

---

**Artículo 4**
- **Slug:** `/blog/posicionamiento-web-gijon/`
- **Title:** `Posicionamiento Web en Gijón: guía para PYMES locales`
- **Meta:** `Todo lo que necesitas saber sobre posicionamiento web en Gijón. Estrategias SEO para PYMES, errores comunes y cómo empezar desde cero.`
- **H1:** `Posicionamiento Web en Gijón para PYMES`
- **Wordcount:** 1.400 palabras
- **Keywords objetivo:** "posicionamiento web gijon" (654 imp, pos 66), "posicionamiento seo gijon" (801 imp)
- **Enlazar a:** `/seo-local-gijon/`, `/seo-gijon/`

---

## PRIORIDAD 5 — Enlazado interno (linkbuilding interno)

Añadir los siguientes enlaces entre páginas existentes. El sitio tiene muy poco enlazado interno y Google no está distribuyendo bien el PageRank entre páginas.

| Página origen | Anchor text | Página destino |
|--------------|-------------|----------------|
| `/` (home) | "SEO Local en Gijón" | `/seo-local-gijon/` |
| `/` (home) | "posicionamiento web en Asturias" | `/posicionamiento-web-asturias/` |
| `/posicionamiento-web-asturias/` | "SEO Local en Gijón" | `/seo-local-gijon/` |
| `/posicionamiento-web-asturias/` | "SEO Local en Oviedo" | `/seo-local-oviedo/` |
| `/seo-local-gijon/` | "consultor SEO en Gijón" | `/seo-gijon/` (nueva) |
| `/seo-local-oviedo/` | "posicionamiento web en Asturias" | `/posicionamiento-web-asturias/` |
| `/inteligencia-artificial-empresas/` | "automatizaciones con IA" | `/automatizaciones-con-ia/` |
| `/google-negocios/` | "SEO Local para tu negocio" | `/seo-local-gijon/` |

---

## Notas técnicas para Claude Code

- El proyecto es **Astro estático** (`output: 'static'`). No hay SSR.
- Los metadatos (title, meta description) probablemente están en un componente `<SEO>` o directamente en el `<head>` del layout. Identificar el patrón antes de editar.
- Los datos estructurados JSON-LD van dentro de `<script type="application/ld+json">` en el `<head>` de cada página.
- Para los artículos de blog, seguir el mismo formato/frontmatter que los artículos existentes en `src/content/blog/` o la ruta equivalente del proyecto.
- No modificar archivos de layout global sin revisar el impacto en todas las páginas.
- Tras cualquier cambio, verificar con `astro build` que no hay errores.

---

## Métricas de referencia (Search Console, feb–may 2026)

| Métrica | Valor actual |
|---------|-------------|
| Clics totales (90 días) | 7 |
| Impresiones totales | 12.509 |
| CTR medio | 0.06% |
| Posición media | 65.6 |
| Página con más impresiones | `/posicionamiento-web-asturias/` (5.053) |
| Página con más clics | `/seo-local-gijon/` (3) |
| Keyword con más impresiones | "posicionamiento web asturias" (1.784) |

**Objetivo a 3 meses:** posición media < 35, CTR > 0.5%, clics > 80/mes.
