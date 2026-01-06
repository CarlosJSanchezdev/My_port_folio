import { Injectable, Inject, PLATFORM_ID } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { BehaviorSubject, Observable } from 'rxjs';
import { tap } from 'rxjs/operators';
import { environment } from '../../environments/environment';

export interface AuthStatus {
  authenticated: boolean;
  access_level: number;
  user?: any;
}

export interface OwnerInfo {
  key: string;
  value: string;
  type: string;
  required_level: number;
  label: string;
  icon: string;
  order: number;
}

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = `${environment.apiUrl}/auth`;
  private authStatusSubject = new BehaviorSubject<AuthStatus>({
    authenticated: false,
    access_level: 1
  });
  
  public authStatus$ = this.authStatusSubject.asObservable();

  constructor(
    private http: HttpClient,
    @Inject(PLATFORM_ID) private platformId: Object
  ) {
    if (isPlatformBrowser(this.platformId)) {
      this.checkAuthStatus();
    }
  }

  checkAuthStatus(): void {
    this.http.get<AuthStatus>(`${this.apiUrl}/status`, { withCredentials: true }).subscribe({
      next: (status) => this.authStatusSubject.next(status),
      error: () => this.authStatusSubject.next({ authenticated: false, access_level: 1 })
    });
  }

  requestVerification(email: string, name: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/request-verification`, { email, name }, { withCredentials: true });
  }

  verifyCode(email: string, code: string, name: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/verify-code`, { email, code, name }, { withCredentials: true }).pipe(
      tap((response: any) => {
        if (response.success && response.user) {
          this.authStatusSubject.next({
            authenticated: true,
            access_level: response.user.access_level,
            user: response.user
          });
        }
      })
    );
  }

  getOwnerInfo(): Observable<{ success: boolean; access_level: number; data: OwnerInfo[] }> {
    return this.http.get<any>(`${this.apiUrl}/owner-info`, { withCredentials: true });
  }

  logout(): Observable<any> {
    return this.http.post(`${this.apiUrl}/logout`, {}, { withCredentials: true }).pipe(
      tap(() => {
        this.authStatusSubject.next({
          authenticated: false,
          access_level: 1
        });
      })
    );
  }

  getAccessLevel(): number {
    return this.authStatusSubject.value.access_level;
  }

  isAuthenticated(): boolean {
    return this.authStatusSubject.value.authenticated;
  }
}
