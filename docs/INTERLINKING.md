# Estrategia de Internal Linking — PYMEMPRESAS

Basado en datos reales de Google Search Console. Actualizar con cada nuevo CSV.

## Datos GSC (Feb-May 2026)

- ~17K impresiones, 2 clicks, CTR ~0.01%
- Posiciones promedio 55-97
- 0 clics en la mayoría de queries

## Clusters de keywords (ordenados por impresiones)

### Cluster 1 — SEO / Posicionamiento Web
**Páginas:** `/posicionamiento-web-asturias/` `/seo-local-gijon/` `/seo-local-oviedo/` `/seo-gijon/`

| Query | Impresiones | Posición | Página destino |
|-------|------------|----------|----------------|
| posicionamiento web asturias | 1660 | 73.5 | posicionamiento-web-asturias |
| posicionamiento seo asturias | 1028 | 80.6 | posicionamiento-web-asturias |
| posicionamiento seo gijon | 775 | 61.2 | seo-local-gijon |
| posicionamiento web gijon | 625 | 65.2 | seo-local-gijon |
| posicionamiento web en asturias | 599 | 72.7 | posicionamiento-web-asturias |
| posicionamiento seo oviedo | 590 | 60.3 | seo-local-oviedo |
| posicionamiento web oviedo | 560 | 69.9 | seo-local-oviedo |
| posicionamiento web aviles | 349 | 76.1 | posicionamiento-web-asturias |
| seo local asturias | 302 | 37.8 | — (crear página) |
| seo gijon | 275 | 46.9 | seo-local-gijon |
| seo oviedo | 254 | 50.2 | seo-local-oviedo |

**Anchors recomendados:** "posicionamiento web en Asturias", "SEO en Gijón", "SEO local en Oviedo", "posicionamiento SEO Asturias"

### Cluster 2 — Diseño Web
**Páginas:** `/diseno-web-gijon/`

| Query | Impresiones | Posición |
|-------|------------|----------|
| diseño web gijon | 388 | 83.5 |
| diseño paginas web gijon | 299 | 72.1 |
| diseño web gijón | 142 | 71.8 |

**Anchors recomendados:** "diseño web en Gijón", "diseño de páginas web Gijón"

### Cluster 3 — IA + Automatización
**Páginas:** `/inteligencia-artificial-empresas/` `/formacion-ia-empresas/` `/automatizaciones-con-ia/`

| Query | Impresiones | Posición |
|-------|------------|----------|
| agencia ia asturias | 40 | 31.2 |
| consultoría inteligencia artificial pymes | 32 | 76.3 |
| inteligencia artificial para empresas oviedo | 20 | 46.3 |
| formación técnica ia para empresas | 15 | 63.3 |
| automatizaciones ia | 5 | 90.6 |

**Anchors recomendados:** "consultoría de IA para empresas", "formación en IA para pymes", "automatizaciones con IA", "automatizaciones inteligentes n8n"

### Cluster 4 — Google My Business
**Páginas:** `/google-negocios/`

| Query | Impresiones | Posición |
|-------|------------|----------|
| googlenegocios | 22 | 10.7 |
| google my business asturias | 12 | 18.5 |
| posicionamiento google my business asturias | 10 | 21.8 |

**Anchors recomendados:** "Google My Business Asturias", "perfil de empresa en Google", "optimización Google Negocios"

### Cluster 5 — Blog
**Páginas:** `/blog/` `/[slug]/`

Sin datos significativos aún. Usar anchors a servicios desde cada artículo.

## Reglas de interlinking

### Al crear un nuevo artículo
1. Identificar a qué cluster pertenece el tema
2. Enlazar mínimo 2-3 páginas de servicio del mismo cluster con anchors de las queries reales
3. Añadir un CTA al final hacia `/consultoria/`
4. Si el artículo menciona keywords de otro cluster, enlazar también cruzado

### Al crear una nueva página de servicio
1. Enlazar a las otras páginas de su cluster (ej: IA → formación, automatizaciones)
2. Enlazar a `/consultoria/` como CTA
3. Actualizar las páginas del cluster para que enlacen de vuelta (link recíproco)

### Anchors
- Usar EXACTAMENTE las queries del GSC como anchor text
- No usar "haz clic aquí" o "más información" — usar keywords
- Los anchors deben ser naturales dentro del contexto del párrafo
- Variar el anchor text entre páginas (no repetir siempre el mismo)

### Páginas que siempre deben recibir links
- `/consultoria/` — desde todas las páginas (CTA)
- `/posicionamiento-web-asturias/` — página con más impresiones (4706)
- `/seo-local-gijon/` — segunda con más impresiones (3093)

## CSV GSC
Ubicación: `pymempresas.com_csv-gsc/`
Actualizar este documento al importar nuevos datos.
