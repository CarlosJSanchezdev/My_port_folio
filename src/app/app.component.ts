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
    this.title.setTitle('Portafolio de Carlos Sánchez');
    this.meta.addTags([
      { name: 'description', content: 'Portafolio profesional de Carlos Sánchez, desarrollador web full stack.' },
      { name: 'author', content: 'Carlos Sánchez' },
      { name: 'keywords', content: 'Angular, Portafolio, Web, Proyectos, Contacto, Blog' }
    ]);
  }
}
