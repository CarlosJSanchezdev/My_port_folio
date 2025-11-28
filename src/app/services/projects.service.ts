import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { ApiService } from './api.service';

export interface Project {
  id?: number;
  title: string;
  description: string;
  longDescription?: string;
  github_url?: string;
  live_demo_url?: string;
  technologies: string[];
  featured_image?: string;
  category: string;
  is_featured: boolean;
  created_at?: string;
}

export interface ProjectsResponse {
  success: boolean;
  data: Project[];
  count: number;
}

@Injectable({
  providedIn: 'root'
})
export class ProjectsService {
  constructor(private api: ApiService) {}

  /**
   * Get all projects
   */
  getProjects(category?: string, featured?: boolean): Observable<Project[]> {
    let endpoint = 'projects/';
    const params: string[] = [];
    
    if (category) {
      params.push(`category=${category}`);
    }
    if (featured !== undefined) {
      params.push(`featured=${featured}`);
    }
    
    if (params.length > 0) {
      endpoint += `?${params.join('&')}`;
    }
    
    return this.api.get<ProjectsResponse>(endpoint).pipe(
      map(response => {
        // Convert technologies from string to array if needed
        return response.data.map(project => ({
          ...project,
          technologies: typeof project.technologies === 'string' 
            ? (project.technologies as any).split(',').map((t: string) => t.trim())
            : project.technologies
        }));
      })
    );
  }

  /**
   * Get a single project by ID
   */
  getProject(id: number): Observable<Project> {
    return this.api.get<{ success: boolean; data: Project }>(`projects/${id}`).pipe(
      map(response => response.data)
    );
  }

  /**
   * Get featured projects
   */
  getFeaturedProjects(): Observable<Project[]> {
    return this.getProjects(undefined, true);
  }

  /**
   * Get projects by category
   */
  getProjectsByCategory(category: string): Observable<Project[]> {
    return this.getProjects(category);
  }
}
