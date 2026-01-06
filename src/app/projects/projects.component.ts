import { Component, OnInit, Inject, PLATFORM_ID } from '@angular/core';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { ProjectsService, Project } from '../services/projects.service';
import { PROJECTS } from '../config/portfolio.config';

@Component({
  selector: 'app-projects',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './projects.component.html',
  styleUrls: ['./projects.component.css']
})
export class ProjectsComponent implements OnInit {
  projects: Project[] = [];
  filteredProjects: Project[] = [];
  selectedCategory: string = 'all';
  categories: string[] = ['all', 'Web', 'Mobile', 'Backend'];
  
  // Loading and error states
  isLoading: boolean = true;
  error: string | null = null;
  useStaticData: boolean = false;

  constructor(
    private projectsService: ProjectsService,
    @Inject(PLATFORM_ID) private platformId: Object
  ) {}

  ngOnInit() {
    if (isPlatformBrowser(this.platformId)) {
      this.loadProjects();
    } else {
      // Server side: use static data directly
      this.projects = PROJECTS as any;
      this.filterProjects('all');
      this.isLoading = false;
    }
  }

  /**
   * Load projects from API with fallback to static data
   */
  loadProjects() {
    this.isLoading = true;
    this.error = null;

    this.projectsService.getProjects().subscribe({
      next: (projects) => {
        this.projects = projects;
        this.filterProjects('all');
        this.isLoading = false;
        this.useStaticData = false;
      },
      error: (err) => {
        console.error('Error loading projects from API:', err);
        this.error = 'Could not load projects from server. Using static data.';
        
        // Fallback to static data
        this.projects = PROJECTS as any;
        this.filterProjects('all');
        this.isLoading = false;
        this.useStaticData = true;
      }
    });
  }

  filterProjects(category: string) {
    this.selectedCategory = category;
    if (category === 'all') {
      this.filteredProjects = this.projects;
    } else {
      this.filteredProjects = this.projects.filter(p => p.category === category);
    }
  }

  get featuredProjects(): Project[] {
    return this.projects.filter(p => p.is_featured);
  }

  /**
   * Retry loading from API
   */
  retry() {
    this.loadProjects();
  }
}
