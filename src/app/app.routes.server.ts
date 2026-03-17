import { RenderMode, ServerRoute } from '@angular/ssr';

export const serverRoutes: ServerRoute[] = [
  // Páginas estáticas → Prerender (máximo SEO y performance)
  {
    path: 'about',
    renderMode: RenderMode.Prerender
  },
  
  // Páginas con datos dinámicos → SSR (SEO + datos en tiempo real)
  {
    path: 'projects',
    renderMode: RenderMode.Server
  },
  {
    path: 'blog',
    renderMode: RenderMode.Server
  },
  
  // Páginas interactivas → Client (no necesitan SEO)
  {
    path: 'contact',
    renderMode: RenderMode.Client
  },
  {
    path: 'footer',
    renderMode: RenderMode.Client
  },
  
  // Fallback → SSR para cualquier otra ruta
  {
    path: '**',
    renderMode: RenderMode.Server
  }
];
