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
