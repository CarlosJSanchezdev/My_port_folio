import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';

interface Project {
  title: string;
  description: string;
  url: string;
  github?: string;
}

@Component({
  selector: 'app-projects',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './projects.component.html',
  styleUrls: ['./projects.component.css']
})
export class ProjectsComponent implements OnInit {
  projects: Project[] = [
    // Ejemplo local
    {
      title: 'Project 1',
      description: 'A brief description of the project goes here.',
      url: 'https://miweb.com/project1',
      github: 'https://github.com/usuario/project1'
    },
    // Puedes agregar más proyectos locales aquí
  ];

  ngOnInit() {
    // Aquí podrías cargar más proyectos desde un backend o API en el futuro
  }
}
