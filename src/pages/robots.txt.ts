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
