import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

interface Article {
  title: string;
  summary: string;
  content: string;
  date: string;
}

@Component({
  selector: 'app-blog',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './blog.component.html',
  styleUrls: ['./blog.component.css']
})
export class BlogComponent {
  articles: Article[] = [
    {
      title: 'Artículo de ejemplo',
      summary: 'Este es un resumen del primer artículo. ¡Haz clic para leer más!',
      content: 'Contenido completo del artículo de ejemplo.',
      date: '2025-06-05'
    }
    // Puedes agregar más artículos aquí
  ];
  selectedArticle: Article | null = null;

  selectArticle(article: Article) {
    this.selectedArticle = article;
  }
  closeArticle() {
    this.selectedArticle = null;
  }
}
