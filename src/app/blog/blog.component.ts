import { Component, OnInit, Pipe, PipeTransform, Inject, PLATFORM_ID } from '@angular/core';
import { CommonModule, isPlatformBrowser } from '@angular/common';

// Pipe para convertir saltos de línea en <br>
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
  articles: Article[] = [
    {
      title: 'Construyendo Aplicaciones Modernas con Angular 19',
      summary: 'Descubre las nuevas características de Angular 19 y cómo aprovecharlas para crear aplicaciones web más rápidas y eficientes.',
      content: `Angular 19 trae consigo una serie de mejoras significativas que transforman la forma en que desarrollamos aplicaciones web. En este artículo, exploraremos las características más destacadas y cómo implementarlas en tus proyectos.

Standalone Components
Una de las mejoras más importantes es la consolidación de los componentes standalone, que simplifican la arquitectura de las aplicaciones eliminando la necesidad de módulos NgModule en muchos casos.

Mejoras en el Rendimiento
Angular 19 incluye optimizaciones en el change detection y mejoras en el compilador que resultan en aplicaciones más rápidas y eficientes.

Server-Side Rendering (SSR)
El SSR ha sido mejorado significativamente, ofreciendo mejor rendimiento y una experiencia de desarrollo más fluida.

Conclusión
Angular 19 representa un gran paso adelante en el ecosistema de desarrollo web, ofreciendo herramientas más potentes y una mejor experiencia para los desarrolladores.`,
      date: '2025-01-15',
      author: 'Carlos Sánchez',
      category: 'Frontend',
      tags: ['Angular', 'TypeScript', 'Web Development'],
      readTime: '5 min',
      image: '/assets/blog/angular-19.png'
    },
    {
      title: 'React Native vs Flutter: ¿Cuál Elegir en 2025?',
      summary: 'Comparativa detallada entre React Native y Flutter para ayudarte a decidir la mejor opción para tu próximo proyecto móvil.',
      content: `El desarrollo móvil multiplataforma ha evolucionado significativamente. Tanto React Native como Flutter ofrecen ventajas únicas. Analicemos cada uno.

React Native
- Basado en JavaScript/TypeScript
- Gran ecosistema y comunidad
- Ideal si ya conoces React
- Excelente para aplicaciones con mucha lógica de negocio

Flutter
- Basado en Dart
- Rendimiento nativo superior
- Widgets personalizables
- Mejor para aplicaciones con UI compleja

Mi Recomendación
Para proyectos con equipos JavaScript existentes, React Native es ideal. Para aplicaciones que requieren UI altamente personalizada y rendimiento óptimo, Flutter es la mejor opción.`,
      date: '2025-01-10',
      author: 'Carlos Sánchez',
      category: 'Mobile',
      tags: ['React Native', 'Flutter', 'Mobile Development'],
      readTime: '7 min',
      image: '/assets/blog/react-native-flutter.png'
    },
    {
      title: 'FastAPI: El Framework Python para APIs Modernas',
      summary: 'Aprende por qué FastAPI se ha convertido en la opción preferida para construir APIs REST de alto rendimiento con Python.',
      content: `FastAPI ha revolucionado el desarrollo de APIs en Python. Su combinación de velocidad, facilidad de uso y características modernas lo hace ideal para proyectos de cualquier escala.

Características Principales
- Validación automática de datos con Pydantic
- Documentación automática con Swagger/OpenAPI
- Rendimiento comparable a NodeJS y Go
- Type hints nativos de Python

Ventajas sobre Flask
Aunque Flask es excelente, FastAPI ofrece:
- Mejor rendimiento
- Validación de datos integrada
- Async/await nativo
- Documentación automática

Cuándo Usar FastAPI
- APIs REST modernas
- Microservicios
- Aplicaciones que requieren alto rendimiento
- Proyectos que necesitan documentación automática

FastAPI es mi elección para nuevos proyectos backend en Python.`,
      date: '2025-01-05',
      author: 'Carlos Sánchez',
      category: 'Backend',
      tags: ['Python', 'FastAPI', 'API Development'],
      readTime: '6 min',
      image: '/assets/blog/fastapi.png'
    },
    {
      title: 'Mejores Prácticas de Git para Equipos',
      summary: 'Estrategias y convenciones de Git que mejorarán la colaboración y productividad de tu equipo de desarrollo.',
      content: `Un buen flujo de trabajo con Git es esencial para equipos productivos. Aquí comparto las prácticas que he encontrado más efectivas.

Commits Significativos
- Usa mensajes descriptivos
- Sigue la convención: tipo(scope): mensaje
- Ejemplos: feat(auth): add login functionality

Branching Strategy
- main: código en producción
- develop: código en desarrollo
- feature/*: nuevas características
- hotfix/*: correcciones urgentes

Code Review
- Siempre usa Pull Requests
- Revisa el código antes de mergear
- Usa herramientas de CI/CD

Conclusión
Estas prácticas han mejorado significativamente la calidad del código y la colaboración en mis proyectos.`,
      date: '2024-12-28',
      author: 'Carlos Sánchez',
      category: 'DevOps',
      tags: ['Git', 'Version Control', 'Best Practices'],
      readTime: '4 min',
      image: '/assets/blog/git-practices.png'
    },
    {
      title: 'Integrando IA en Aplicaciones Web con OpenAI',
      summary: 'Guía práctica para integrar capacidades de inteligencia artificial en tus aplicaciones usando la API de OpenAI.',
      content: `La inteligencia artificial está transformando las aplicaciones web. Veamos cómo integrar OpenAI en tus proyectos.

Configuración Inicial
1. Obtén tu API key de OpenAI
2. Instala el SDK correspondiente
3. Configura las variables de entorno

Casos de Uso Comunes
- Chatbots inteligentes
- Generación de contenido
- Análisis de texto
- Recomendaciones personalizadas

Ejemplo: Chatbot
Implementar un chatbot con GPT-4 es sorprendentemente simple. Con pocas líneas de código puedes tener un asistente inteligente funcionando.

Consideraciones
- Costos de API
- Límites de rate
- Privacidad de datos
- Manejo de errores

Proyecto Comai
En mi proyecto Comai, uso OpenAI para generar recomendaciones de recetas personalizadas basadas en ingredientes disponibles.`,
      date: '2024-12-20',
      author: 'Carlos Sánchez',
      category: 'AI',
      tags: ['OpenAI', 'AI', 'GPT-4', 'Web Development'],
      readTime: '8 min',
      image: '/assets/blog/openai-integration.png'
    }
  ];

  selectedArticle: Article | null = null;
  filteredArticles: Article[] = [];
  selectedCategory: string = 'all';
  categories: string[] = ['all', 'Frontend', 'Backend', 'Mobile', 'DevOps', 'AI'];

  constructor(@Inject(PLATFORM_ID) private platformId: Object) {}

  ngOnInit() {
    this.filteredArticles = this.articles;
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
