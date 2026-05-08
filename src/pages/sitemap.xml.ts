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
