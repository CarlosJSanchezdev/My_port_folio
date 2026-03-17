import { Component } from '@angular/core';
import { HeaderComponent } from './header/header.component';
import { FooterComponent } from './footer/footer.component';
import { RouterOutlet } from '@angular/router';
import { Title, Meta } from '@angular/platform-browser';

@Component({
  selector: 'app-root',
  imports: [HeaderComponent, FooterComponent, RouterOutlet],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
})

export class AppComponent {
  constructor(private title: Title, private meta: Meta) {
    this.title.setTitle('Carlos Sánchez - Desarrollador Full Stack | Portafolio Profesional');
    this.meta.addTags([
      { name: 'description', content: 'Portafolio profesional de Carlos Sánchez, desarrollador web full stack especializado en Angular, React, Python y Node.js.' },
      { name: 'author', content: 'Carlos Sánchez' },
      { name: 'keywords', content: 'Angular, React, Python, Node.js, TypeScript, FastAPI, Flask, PostgreSQL, MongoDB, Portafolio, Web, Proyectos, Contacto, Blog, Cali, Colombia' },
      { name: 'robots', content: 'index, follow' },
      { name: 'theme-color', content: '#677365' },
      // Open Graph
      { property: 'og:type', content: 'website' },
      { property: 'og:url', content: 'https://carlosjsanchez.dev/' },
      { property: 'og:title', content: 'Carlos Sánchez - Desarrollador Full Stack' },
      { property: 'og:description', content: 'Portafolio profesional de Carlos Sánchez, desarrollador Full Stack.' },
      { property: 'og:image', content: '/assets/og-image.png' },
      { property: 'og:locale', content: 'es_ES' },
      // Twitter Card
      { name: 'twitter:card', content: 'summary_large_image' },
      { name: 'twitter:title', content: 'Carlos Sánchez - Desarrollador Full Stack' },
      { name: 'twitter:description', content: 'Portafolio profesional de Carlos Sánchez, desarrollador Full Stack.' },
      { name: 'twitter:image', content: '/assets/og-image.png' }
    ]);
  }
}
