import { Component, OnInit, Pipe, PipeTransform, Inject, PLATFORM_ID } from '@angular/core';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { BlogService, BlogPost } from '../services/blog.service';

@Pipe({
  name: 'nl2br',
  standalone: true
})
export class Nl2brPipe implements PipeTransform {
  transform(value: string): string {
    if (!value) return value;
    return value.replace(/\n/g, '<br>');
  }
}


interface Article {
  title: string;
  summary: string;
  content: string;
  date: string;
  author: string;
  category: string;
  tags: string[];
  readTime: string;
  image?: string;
}

@Component({
  selector: 'app-blog',
  standalone: true,
  imports: [CommonModule, Nl2brPipe],
  templateUrl: './blog.component.html',
  styleUrls: ['./blog.component.css']
})
export class BlogComponent implements OnInit {
  articles: Article[] = [];
  selectedArticle: Article | null = null;
  filteredArticles: Article[] = [];
  selectedCategory: string = 'all';
  categories: string[] = ['all', 'Frontend', 'Backend', 'Mobile', 'DevOps', 'AI'];
  loading: boolean = true;
  error: string = '';

  constructor(
    @Inject(PLATFORM_ID) private platformId: Object,
    private blogService: BlogService
  ) {}

  ngOnInit() {
    this.loadPosts();
  }

  loadPosts() {
    this.loading = true;
    this.error = '';
    
    this.blogService.getPosts(true).subscribe({
      next: (posts) => {
        this.articles = posts.map(post => this.mapToArticle(post));
        this.filteredArticles = this.articles;
        this.loading = false;
      },
      error: (err) => {
        console.error('Error loading blog posts:', err);
        this.error = 'Error al cargar los artículos';
        this.loading = false;
      }
    });
  }

  private mapToArticle(post: BlogPost): Article {
    return {
      title: post.title,
      summary: post.excerpt,
      content: post.content,
      date: post.published_at ? new Date(post.published_at).toISOString().split('T')[0] : new Date().toISOString().split('T')[0],
      author: 'Carlos Sánchez',
      category: this.getCategoryFromTags(post.tags),
      tags: post.tags,
      readTime: `${post.read_time} min`,
      image: post.featured_image
    };
  }

  private getCategoryFromTags(tags: string[]): string {
    const tagLower = tags.map(t => t.toLowerCase());
    if (tagLower.some(t => t.includes('angular') || t.includes('react') || t.includes('typescript'))) return 'Frontend';
    if (tagLower.some(t => t.includes('python') || t.includes('fastapi') || t.includes('flask'))) return 'Backend';
    if (tagLower.some(t => t.includes('react native') || t.includes('flutter') || t.includes('mobile'))) return 'Mobile';
    if (tagLower.some(t => t.includes('git') || t.includes('devops'))) return 'DevOps';
    if (tagLower.some(t => t.includes('ai') || t.includes('openai') || t.includes('gpt'))) return 'AI';
    return 'General';
  }

  selectArticle(article: Article) {
    this.selectedArticle = article;
    if (isPlatformBrowser(this.platformId)) {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  }

  closeArticle() {
    this.selectedArticle = null;
  }

  filterByCategory(category: string) {
    this.selectedCategory = category;
    if (category === 'all') {
      this.filteredArticles = this.articles;
    } else {
      this.filteredArticles = this.articles.filter(a => a.category === category);
    }
  }
}
