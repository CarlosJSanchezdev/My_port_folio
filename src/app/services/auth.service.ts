import { Injectable, Inject, PLATFORM_ID } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
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
  private TOKEN_KEY = 'portfolio_auth_token';
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

  /**
   * Guarda el token en localStorage
   */
  private saveToken(token: string): void {
    if (isPlatformBrowser(this.platformId)) {
      localStorage.setItem(this.TOKEN_KEY, token);
    }
  }

  /**
   * Obtiene el token de localStorage
   */
  private getToken(): string | null {
    if (isPlatformBrowser(this.platformId)) {
      return localStorage.getItem(this.TOKEN_KEY);
    }
    return null;
  }

  /**
   * Elimina el token de localStorage
   */
  private removeToken(): void {
    if (isPlatformBrowser(this.platformId)) {
      localStorage.removeItem(this.TOKEN_KEY);
    }
  }

  /**
   * Crea headers con el token JWT
   */
  private createAuthHeaders(): HttpHeaders {
    const token = this.getToken();
    if (token) {
      return new HttpHeaders({
        'Authorization': `Bearer ${token}`
      });
    }
    return new HttpHeaders();
  }

  checkAuthStatus(): void {
    const token = this.getToken();
    if (token) {
      // Decodificar token para obtener access_level
      try {
        const payload = JSON.parse(atob(token.split('.')[1]));
        if (payload.exp * 1000 > Date.now()) {
          // Token válido - verificar con el backend
          this.http.get<AuthStatus>(`${this.apiUrl}/status`, { 
            headers: this.createAuthHeaders(),
            withCredentials: true 
          }).subscribe({
            next: (status) => {
              if (status.authenticated) {
                this.authStatusSubject.next(status);
              } else {
                // Token inválido en backend
                this.removeToken();
                this.authStatusSubject.next({ authenticated: false, access_level: 1 });
              }
            },
            error: () => {
              // Error al verificar con backend, usar datos locales
              this.authStatusSubject.next({
                authenticated: true,
                access_level: payload.access_level || 1
              });
            }
          });
          return;
        }
      } catch (e) {
        // Token inválido
      }
      this.removeToken();
    }
    this.authStatusSubject.next({ authenticated: false, access_level: 1 });
  }

  requestVerification(email: string, name: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/request-verification`, { email, name }, { withCredentials: true });
  }

  verifyCode(email: string, code: string, name: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/verify-code`, { email, code, name }, { withCredentials: true }).pipe(
      tap((response: any) => {
        if (response.success && response.token) {
          this.saveToken(response.token);
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
    return this.http.get<any>(`${this.apiUrl}/owner-info`, { headers: this.createAuthHeaders() });
  }

  logout(): Observable<any> {
    this.removeToken();
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
