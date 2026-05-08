import { defineCollection, z } from 'astro:content';

const serviciosCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    subtitle: z.string(),
    description: z.string(),
    heroCta: z.string(),
    heroCtaHref: z.string().default('/consultoria/'),
    badge: z.string().optional(),
    heroChecks: z.array(z.string()).optional(),
    heroBgImage: z.string().default('/images/hero-bg-DF654TP8.webp'),
    features: z.array(
      z.object({
        title: z.string(),
        description: z.string(),
        icon: z.string(),
      })
    ),
    benefits: z.array(z.string()),
    faq: z
      .array(
        z.object({
          q: z.string(),
          a: z.string(),
        })
      )
      .optional(),
    relatedServices: z.array(z.string()).max(3).optional(),
    ogImage: z.string().optional(),
  }),
});

const homeCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    subtitle: z.string(),
    description: z.string(),
    heroCta: z.string(),
    heroCtaHref: z.string(),
    heroCtaSecondary: z.string(),
    heroCtaSecondaryHref: z.string(),
    badge: z.string(),
    heroChecks: z.array(z.string()),
    heroBgImage: z.string(),
    ogImage: z.string().optional(),
    heroSubtitleSecondary: z.string().optional(),
    services: z.array(
      z.object({
        title: z.string(),
        description: z.string(),
        features: z.array(z.string()),
        link: z.string(),
      })
    ),
    about: z.object({
      title: z.string(),
      paragraphs: z.array(z.string()),
      location: z.string(),
      googleBusinessUrl: z.string(),
      ctaHref: z.string(),
    }),
    stats: z.array(
      z.object({
        value: z.string(),
        label: z.string(),
      })
    ),
    advantages: z.array(
      z.object({
        title: z.string(),
        description: z.string(),
      })
    ),
  }),
});

const blogCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    date: z.date(),
    author: z.string().default('PYMEMPRESAS'),
    image: z.string().optional(),
    tags: z.array(z.string()).optional(),
    authorLinkedin: z.string().optional(),
    authorTwitter: z.string().optional(),
    authorBio: z.string().optional(),
    authorImage: z.string().optional(),
  }),
});

export const collections = {
  servicios: serviciosCollection,
  home: homeCollection,
  blog: blogCollection,
};
