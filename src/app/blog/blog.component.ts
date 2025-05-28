import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-blog',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './blog.component.html',
  styleUrls: ['./blog.component.css']
})
export class BlogComponent {
  articles = [
  {title: 'Article Title 1', summary: 'This is a summary of the first blog article. Click to read more!'},
  {title: 'Article Title 2', summary: 'This is a summary of the second blog article. Click to red more!'}
  ];
}
