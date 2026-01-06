// Personal Information Configuration
export const PERSONAL_INFO = {
  // Basic Info
  name: 'Carlos Sánchez',
  title: 'Desarrollador Full Stack',
  email: 'cjsatlas@hotmail.com',
  phone: '+57 317 691 3321',
  location: 'Santiago de Cali, Colombia',
  
  // Bio
  bio: {
    short: 'Desarrollador Full Stack apasionado por crear soluciones digitales innovadoras que transforman ideas en experiencias excepcionales.',
    long: `Soy un desarrollador full stack con 1 año de experiencia en el desarrollo de aplicaciones web y móviles. Mi pasión es desarrollar productos tecnológicos que impacten y mejoren la vida tecnológica de las personas.

He trabajado en proyectos que van desde aplicaciones de gestión empresarial hasta plataformas de inteligencia artificial, siempre enfocándome en la calidad del código, la experiencia del usuario y las mejores prácticas de desarrollo.

Cuando no estoy programando, me gusta aprender nuevas tecnologías, contribuir a proyectos open source y compartir conocimientos con la comunidad de desarrolladores.`
  },
  
  // Stats
  stats: {
    experience: '1',
    projects: 1,
    technologies: 10,
    satisfaction: 100
  },
  
  // Social Links
  social: {
    github: 'https://github.com/CarlosJSanchezdev',
    linkedin: 'https://www.linkedin.com/in/carlos-sánchez-b9311b32b',
    twitter: 'https://twitter.com/carlosjsanchez',
    email: 'mailto:cjsatlas@hotmail.com'
  },
  
  // Work Info
  availability: {
    freelance: true,
    remote: true,
    schedule: 'Lun - Vie: 9:00 AM - 6:00 PM',
    responseTime: 'menos de 24 horas'
  }
};

// Skills Configuration
export const SKILLS = {
  frontend: [
    { name: 'Angular', icon: '🅰️', level: 85 },
    { name: 'React', icon: '⚛️', level: 75 },
    { name: 'TypeScript', icon: '📘', level: 90 },
    { name: 'HTML/CSS', icon: '🎨', level: 95 },
    { name: 'Tailwind CSS', icon: '💨', level: 80 }
  ],
  backend: [
    { name: 'Node.js', icon: '🟢', level: 80 },
    { name: 'Python', icon: '🐍', level: 85 },
    { name: 'Flask/FastAPI', icon: '⚡', level: 80 },
    { name: 'PostgreSQL', icon: '🐘', level: 75 },
    { name: 'MongoDB', icon: '🍃', level: 70 }
  ],
  mobile: [
    { name: 'React Native', icon: '📱', level: 75 },
    { name: 'Expo', icon: '🚀', level: 80 },
    //{ name: 'iOS/Android', icon: '📲', level: 70 }
  ],
  tools: [
    { name: 'Git', icon: '🔧', level: 90 },
    //{ name: 'Docker', icon: '🐳', level: 70 },
    { name: 'Supabase', icon: '⚡', level: 75 },
    { name: 'Firebase', icon: '🔥', level: 75 },
    { name: 'REST APIs', icon: '🌐', level: 90 }
  ]
};

// Projects Configuration
export const PROJECTS = [
  {
    id: 'portfolio',
    title: 'My Portfolio',
    description: 'Portafolio profesional con Angular 19 y diseño moderno',
    longDescription: 'Portafolio personal desarrollado con Angular 19, implementando las últimas características del framework. Diseño moderno con glassmorphism, animaciones suaves y optimización SEO.',
    technologies: ['Angular 19', 'TypeScript', 'CSS', 'SSR'],
    github_url: 'https://github.com/CarlosJSanchezdev/My_port_folio',
    live_demo_url: '',
    featured_image: '/assets/projects/portfolio.png',
    is_featured: true,
    category: 'Web',
    status: 'completed' // ✅ Completado
  },
  {
    id: 'comai',
    title: 'Comai',
    description: 'Aplicación móvil de recetas inteligentes con IA y delivery multi-proveedor (En Desarrollo)',
    longDescription: 'Aplicación móvil completa que combina inteligencia artificial, gestión de despensa y delivery para revolucionar la forma de cocinar. Incluye recomendaciones personalizadas con GPT-4, análisis de imágenes con Google Cloud Vision, y integración con múltiples proveedores de delivery. Actualmente en desarrollo.',
    technologies: ['React Native', 'TypeScript', 'Supabase', 'OpenAI GPT-4', 'PostgreSQL', 'Expo'],
    github_url: 'https://github.com/CarlosJSanchezdev/Comai',
    live_demo_url: '',
    featured_image: '/assets/projects/comai.png',
    is_featured: true,
    category: 'Mobile',
    status: 'in-development' // 🚧 En desarrollo
  },
  {
    id: 'app-message',
    title: 'App Message',
    description: 'Sistema de mensajería con FastAPI y arquitectura moderna (En Desarrollo)',
    longDescription: 'Aplicación de mensajería desarrollada con FastAPI, implementando arquitectura limpia y mejores prácticas de desarrollo backend. Incluye autenticación JWT, WebSockets para mensajes en tiempo real y base de datos SQLite. Actualmente en desarrollo.',
    technologies: ['Python', 'FastAPI', 'SQLAlchemy', 'SQLite', 'WebSockets'],
    github_url: 'https://github.com/CarlosJSanchezdev/app_message',
    live_demo_url: '',
    featured_image: '/assets/projects/app-message.png',
    is_featured: true,
    category: 'Backend',
    status: 'in-development' // 🚧 En desarrollo
  },
  {
    id: 'salon-scheduler',
    title: 'Salon Scheduler',
    description: 'Sistema de gestión de citas para salones de belleza (En Desarrollo)',
    longDescription: 'Aplicación web para la gestión de citas y clientes en salones de belleza. Permite agendar citas, gestionar servicios, clientes y generar reportes. Actualmente en desarrollo.',
    technologies: ['Python', 'Flask', 'SQLite', 'HTML', 'CSS', 'JavaScript'],
    github_url: 'https://github.com/CarlosJSanchezdev/salon_scheduler',
    live_demo_url: '',
    featured_image: '/assets/projects/salon-scheduler.png',
    is_featured: false,
    category: 'Web',
    status: 'in-development' // 🚧 En desarrollo
  },
  {
    id: 'url-shortener',
    title: 'URL Shortener',
    description: 'Acortador de URLs con análisis de estadísticas (En Desarrollo)',
    longDescription: 'Servicio de acortamiento de URLs con seguimiento de clicks, análisis de estadísticas y dashboard administrativo. Actualmente en desarrollo.',
    technologies: ['Python', 'Flask', 'SQLite', 'REST API'],
    github_url: 'https://github.com/CarlosJSanchezdev/url_shortener',
    live_demo_url: '',
    featured_image: '/assets/projects/url-shortener.png',
    is_featured: false,
    category: 'Backend',
    status: 'in-development' // 🚧 En desarrollo
  },
  {
    id: 'worklist',
    title: 'WorkList',
    description: 'Aplicación de gestión de tareas y productividad (En Desarrollo)',
    longDescription: 'Sistema de gestión de tareas con funcionalidades de organización, priorización y seguimiento de proyectos personales. Actualmente en desarrollo.',
    technologies: ['JavaScript', 'Node.js', 'Express', 'MongoDB'],
    github_url: 'https://github.com/CarlosJSanchezdev/workList',
    live_demo_url: '',
    featured_image: '/assets/projects/worklist.png',
    is_featured: false,
    category: 'Web',
    status: 'in-development' // 🚧 En desarrollo
  },
  {
    id: 'san-rafael',
    title: 'San Rafael Desarrollo',
    description: 'Plataforma web corporativa con múltiples servicios (En Desarrollo)',
    longDescription: 'Plataforma web empresarial que integra múltiples servicios y funcionalidades para la gestión de proyectos y comunicación interna. Actualmente en desarrollo.',
    technologies: ['Python', 'Flask', 'PostgreSQL', 'HTML', 'CSS'],
    github_url: 'https://github.com/CarlosJSanchezdev/San_Rafael_desarrollo',
    live_demo_url: '',
    featured_image: '/assets/projects/san-rafael.png',
    is_featured: false,
    category: 'Web',
    status: 'in-development' // 🚧 En desarrollo
  },
  {
    id: 'frontend-coms',
    title: 'Frontend COMS',
    description: 'Frontend para sistema de comunicaciones (En Desarrollo)',
    longDescription: 'Interfaz de usuario moderna para sistema de comunicaciones empresariales con diseño responsive y experiencia de usuario optimizada. Actualmente en desarrollo.',
    technologies: ['React', 'TypeScript', 'Tailwind CSS'],
    github_url: 'https://github.com/CarlosJSanchezdev/frontend-coms',
    live_demo_url: '',
    featured_image: '/assets/projects/frontend-coms.png',
    is_featured: false,
    category: 'Web',
    status: 'in-development' // 🚧 En desarrollo
  }
];

// SEO Configuration
export const SEO = {
  title: 'Carlos Sánchez - Desarrollador Full Stack',
  description: 'Portafolio profesional de Carlos Sánchez, desarrollador full stack de Santiago de Cali, Colombia. Especializado en Angular, React, Python y Node.js.',
  keywords: 'Carlos Sánchez, Desarrollador Full Stack, Angular, React, Python, Node.js, Web Development, Mobile Development, Santiago de Cali, Colombia',
  author: 'Carlos Sánchez',
  url: 'https://carlosjsanchez.dev',
  image: '/assets/og-image.png'
};
