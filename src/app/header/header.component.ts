import { CommonModule } from '@angular/common';
import { Component, OnInit, signal } from '@angular/core';
import { RouterModule } from '@angular/router';
import { AuthService } from '../services/auth.service';
import { environment } from '../../environments/environment';

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent implements OnInit {
  // Signals para estado reactivo
  readonly mobileMenuOpen = signal(false);
  readonly accessLevel = signal<number>(1);
  readonly cvUrl = `${environment.apiUrl}/protected/cv`;

  constructor(
    private authService: AuthService
  ) {}

  ngOnInit() {
    this.authService.authStatus$.subscribe(status => {
      this.accessLevel.set(Number(status.access_level));
    });
  }

  toggleMobileMenu(): void {
    this.mobileMenuOpen.update(value => !value);
  }

  closeMobileMenu(): void {
    this.mobileMenuOpen.set(false);
  }
}
