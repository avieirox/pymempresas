import { readFileSync, writeFileSync, mkdirSync, existsSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const BLOG_DIR = join(__dirname, '..', 'src', 'content', 'blog');

function slugify(text) {
  return text
    .toLowerCase()
    .normalize('NFD')
    .replace(/[̀-ͯ]/g, '')
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '')
    .substring(0, 80);
}

function parseCSV(content) {
  const rows = [];
  let current = '';
  let inQuotes = false;

  for (let i = 0; i < content.length; i++) {
    const ch = content[i];
    if (ch === '"') {
      inQuotes = !inQuotes;
    } else if (ch === '\n' && !inQuotes) {
      rows.push(current.split(',').map(c => c.trim().replace(/^"|"$/g, '')));
      current = '';
    } else if (ch === '\r' && !inQuotes) {
      continue;
    } else {
      current += ch;
    }
  }
  if (current) {
    rows.push(current.split(',').map(c => c.trim().replace(/^"|"$/g, '')));
  }
  return rows;
}

function main() {
  const csvPath = process.argv[2];
  if (!csvPath) {
    console.log('Uso: node scripts/import-blog.mjs posts.csv');
    console.log('');
    console.log('Columnas esperadas en el CSV:');
    console.log('  Título del Contenido (Blog/Artículo)');
    console.log('  Fase');
    console.log('  Pilar Principal Relacionado');
    console.log('  Slug');
    console.log('  Publicar (TRUE/SI/X para publicar)');
    console.log('  Fecha (dd/mm/aaaa o yyyy-mm-dd)');
    console.log('  Descripción');
    process.exit(1);
  }

  const csv = readFileSync(csvPath, 'utf-8');
  const rows = parseCSV(csv);

  const header = rows[0];
  console.log('Columnas detectadas:', header.join(', '));

  const titleIdx = header.findIndex(h => h.toLowerCase().includes('título'));
  const faseIdx = header.findIndex(h => h.toLowerCase().includes('fase'));
  const pilarIdx = header.findIndex(h => h.toLowerCase().includes('pilar'));
  const slugIdx = header.findIndex(h => h.toLowerCase().includes('slug'));
  const publishIdx = header.findIndex(h => h.toLowerCase().includes('publicar'));
  const dateIdx = header.findIndex(h => h.toLowerCase().includes('fecha'));
  const descIdx = header.findIndex(h => h.toLowerCase().includes('descripci'));

  if (!existsSync(BLOG_DIR)) {
    mkdirSync(BLOG_DIR, { recursive: true });
  }

  let created = 0;
  let skipped = 0;

  for (let i = 1; i < rows.length; i++) {
    const row = rows[i];
    const title = titleIdx >= 0 ? row[titleIdx] : '';
    const pilar = pilarIdx >= 0 ? row[pilarIdx] : '';
    if (!title) continue;

    const slug = slugIdx >= 0 && row[slugIdx]
      ? row[slugIdx]
      : slugify(title);

    const shouldPublish = publishIdx >= 0
      ? ['TRUE', 'true', 'SI', 'si', 'SÍ', 'sí', 'X', 'x', '1', 'YES', 'yes'].includes(row[publishIdx])
      : true;

    if (!shouldPublish) {
      skipped++;
      continue;
    }

    let date;
    if (dateIdx >= 0 && row[dateIdx]) {
      const raw = row[dateIdx];
      if (raw.includes('/')) {
        const parts = raw.split('/');
        date = parts[2].length === 4
          ? `${parts[2]}-${parts[1].padStart(2, '0')}-${parts[0].padStart(2, '0')}`
          : raw;
      } else {
        date = raw;
      }
    } else {
      date = new Date().toISOString().split('T')[0];
    }

    const description = descIdx >= 0 && row[descIdx]
      ? row[descIdx]
      : `Artículo sobre ${title.toLowerCase()}. Descubre cómo mejorar tu presencia digital.`;

    const tags = pilar
      ? pilar.split(/ \+ | \/ /).map(t => t.trim()).filter(Boolean)
      : [];

    const frontmatter = [
      '---',
      `title: '${title.replace(/'/g, "\\'")}'`,
      `description: '${description.replace(/'/g, "\\'")}'`,
      `date: ${date}`,
      `author: 'PYMEMPRESAS'`,
      tags.length ? `tags: [${tags.map(t => `'${t}'`).join(', ')}]` : '',
      '---',
      '',
      '<!-- Escribe aquí el contenido del artículo -->',
      '',
      `> Artículo parte del pilar: **${pilar}**. Fase: **${row[faseIdx] || '—'}**.`,
      '',
    ].filter(Boolean).join('\n');

    const filePath = join(BLOG_DIR, `${slug}.mdx`);
    writeFileSync(filePath, frontmatter, 'utf-8');
    console.log(`  ✓ ${slug}.mdx`);
    created++;
  }

  console.log('');
  console.log(`Creados: ${created} | Saltados (sin Publicar): ${skipped}`);
  console.log(`Directorio: ${BLOG_DIR}`);
}

main();
