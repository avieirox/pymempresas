import type { APIRoute } from 'astro';

export const GET: APIRoute = ({ site }) => {
  const robots = `User-agent: *
Allow: /
Disallow: /cdn-cgi/
Sitemap: ${site}sitemap.xml

# Bloqueo de crawlers de entrenamiento IA
User-agent: GPTBot
Disallow: /

User-agent: CCBot
Disallow: /

User-agent: anthropic-ai
Disallow: /

User-agent: Claude-Web
Disallow: /

User-agent: Google-Extended
Disallow: /

User-agent: PerplexityBot
Disallow: /

User-agent: Omgilibot
Disallow: /

User-agent: FacebookBot
Disallow: /
`;

  return new Response(robots, {
    headers: { 'Content-Type': 'text/plain' },
  });
};
