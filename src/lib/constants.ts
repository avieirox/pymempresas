export const SITE = {
  name: 'PYMEMPRESAS',
  url: 'https://pymempresas.com',
  defaultTitle: 'Agencia de Posicionamiento WEB SEO Local | PYMEMPRESAS',
  defaultDescription:
    'Agencia de SEO Local en Asturias con más de 10 años de experiencia. Posicionamos tu negocio en Google para que tus clientes te encuentren primero. Consultoría gratuita.',
  ogImage: '/og-default.svg',
  locale: 'es_ES',
} as const;

export const CONTACT = {
  email: 'info@pymempresas.com',
  phone: '+34 697 71 13 44',
  address: 'Spaces Coworking, C. Rodríguez San Pedro, 1, Centro, 33206 Gijón, Asturias',
  hours: 'Lun–Vie 9:00–18:00',
} as const;

export const NAV_ITEMS = [
  { label: 'Inicio', href: '/' },
  {
    label: 'Google Negocios',
    href: '/google-negocios/',
    children: [
      { label: 'SEO Local Gijón', href: '/seo-local-gijon/' },
      { label: 'SEO Local Oviedo', href: '/seo-local-oviedo/' },
    ],
  },
  {
    label: 'Servicios',
    href: '/#servicios',
    children: [
      { label: 'Posicionamiento Web', href: '/posicionamiento-web-asturias/' },
      { label: 'Diseño Web', href: '/diseno-web-gijon/' },
      { label: 'IA para Empresas', href: '/inteligencia-artificial-empresas/' },
      { label: 'Formación', href: '/formacion-ia-empresas/' },
      { label: 'Automatizaciones n8n', href: '/automatizaciones-con-ia/' },
    ],
  },
  { label: 'Blog', href: '/blog/' },
  { label: 'Contacto', href: '/contacto/' },
] as const;

export const FOOTER_SERVICES = [
  { label: 'SEO Local', href: '/seo-local-gijon/' },
  { label: 'Diseño Web', href: '/diseno-web-gijon/' },
  { label: 'IA para Empresas', href: '/inteligencia-artificial-empresas/' },
  { label: 'Formación IA', href: '/formacion-ia-empresas/' },
  { label: 'Automatizaciones', href: '/automatizaciones-con-ia/' },
  { label: 'Posicionamiento Web', href: '/posicionamiento-web-asturias/' },
] as const;

export const FOOTER_LEGAL = [
  { label: 'Aviso Legal', href: '/aviso-legal/' },
  { label: 'Política de Privacidad', href: '/politica-privacidad/' },
] as const;

export const WHY_CHOOSE_US = [
  { title: 'Aumenta tu visibilidad', description: 'Tu negocio aparece en los primeros resultados cuando tus clientes te buscan.', icon: 'eye' },
  { title: 'Más clientes locales', description: 'Atrae clientes cualificados de tu zona geográfica con estrategias de SEO local.', icon: 'users' },
  { title: 'Resultados medibles', description: 'Informes mensuales con métricas claras de posicionamiento y tráfico.', icon: 'chart' },
  { title: 'Ahorra tiempo', description: 'Céntrate en tu negocio mientras nosotros optimizamos tu presencia digital.', icon: 'clock' },
  { title: 'Reputación sólida', description: 'Construye una presencia online de confianza con reseñas y contenido de calidad.', icon: 'star' },
  { title: 'Expertos locales', description: 'Conocemos el mercado asturiano y sabemos qué funciona en cada sector.', icon: 'map-pin' },
] as const;
