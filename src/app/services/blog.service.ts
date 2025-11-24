import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { ApiService } from './api.service';

export interface BlogPost {
  id?: number;
  title: string;
  content: string;
  excerpt: string;
  slug: string;
  featured_image?: string;
  published: boolean;
  tags: string[];
  read_time: number;
  published_at?: string;
  created_at?: string;
}

export interface BlogResponse {
  success: boolean;
  data: BlogPost[];
  count: number;
}

@Injectable({
  providedIn: 'root'
})
export class BlogService {
  constructor(private api: ApiService) {}

  /**
   * Get all blog posts
   */
  getPosts(publishedOnly: boolean = true, tag?: string): Observable<BlogPost[]> {
    let endpoint = 'blog';
    const params: string[] = [];
    
    params.push(`published=${publishedOnly}`);
    
    if (tag) {
      params.push(`tag=${tag}`);
    }
    
    if (params.length > 0) {
      endpoint += `?${params.join('&')}`;
    }
    
    return this.api.get<BlogResponse>(endpoint).pipe(
      map(response => {
        // Convert tags from string to array if needed
        return response.data.map(post => ({
          ...post,
          tags: typeof post.tags === 'string' 
            ? (post.tags as any).split(',').map((t: string) => t.trim())
            : post.tags
        }));
      })
    );
  }

  /**
   * Get a single blog post by slug
   */
  getPost(slug: string): Observable<BlogPost> {
    return this.api.get<{ success: boolean; data: BlogPost }>(`blog/${slug}`).pipe(
      map(response => response.data)
    );
  }

  /**
   * Get posts by tag
   */
  getPostsByTag(tag: string): Observable<BlogPost[]> {
    return this.getPosts(true, tag);
  }
}
