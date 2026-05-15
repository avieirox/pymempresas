import type { APIRoute } from 'astro';
import { getCollection } from 'astro:content';

export const GET: APIRoute = async ({ site }) => {
  const servicios = await getCollection('servicios');
  const blogPosts = await getCollection('blog');

  const today = new Date().toISOString().split('T')[0];
  const pages = [
    { url: '', lastmod: today },
    { url: 'consultoria/', lastmod: today },
    { url: 'contacto/', lastmod: today },
    { url: 'blog/', lastmod: today },
    { url: 'seo-gijon/', lastmod: today },
  ];

  const servicioEntries = servicios.map((s) => ({
    url: `${s.slug}/`,
    lastmod: s.data.updatedAt
      ? new Date(s.data.updatedAt).toISOString().split('T')[0]
      : today,
  }));

  const blogEntries = blogPosts.map((p) => {
    const d = p.data.updatedAt
      ? new Date(p.data.updatedAt)
      : p.data.date
        ? new Date(p.data.date)
        : new Date();
    return {
      url: `${p.slug}/`,
      lastmod: d.toISOString().split('T')[0],
    };
  });

  const allUrls = [...pages, ...servicioEntries, ...blogEntries];

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
