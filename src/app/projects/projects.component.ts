import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-projects',
  imports: [CommonModule],
  templateUrl: './projects.component.html',
  styleUrl: './projects.component.css'
})
export class ProjectsComponent {
  projects = [
    {title: 'Project 1', description: 'A brief description of the project goes here.'},
    {title: 'Project 2', description: 'A brief description of the project goes here.'}
  ]

}
