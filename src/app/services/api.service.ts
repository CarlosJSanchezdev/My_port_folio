import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse, HttpHeaders } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, retry } from 'rxjs/operators';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private apiUrl = environment.apiUrl;

  private jsonHeaders = new HttpHeaders({
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  });

  constructor(private http: HttpClient) {}

  private options(withCredentials = false) {
    return {
      headers: this.jsonHeaders,
      withCredentials
    };
  }

  /**
   * GET request
   */
  get<T>(endpoint: string, withCredentials = false): Observable<T> {
    return this.http.get<T>(`${this.apiUrl}/${endpoint}`, this.options(withCredentials))
      .pipe(
        retry(1),
        catchError(this.handleError)
      );
  }

  /**
   * POST request
   */
  post<T>(endpoint: string, data: any, withCredentials = false): Observable<T> {
    return this.http.post<T>(`${this.apiUrl}/${endpoint}`, JSON.stringify(data), this.options(withCredentials))
      .pipe(
        catchError(this.handleError)
      );
  }

  /**
   * PUT request
   */
  put<T>(endpoint: string, data: any, withCredentials = false): Observable<T> {
    return this.http.put<T>(`${this.apiUrl}/${endpoint}`, JSON.stringify(data), this.options(withCredentials))
      .pipe(
        catchError(this.handleError)
      );
  }

  /**
   * DELETE request
   */
  delete<T>(endpoint: string, withCredentials = false): Observable<T> {
    return this.http.delete<T>(`${this.apiUrl}/${endpoint}`, this.options(withCredentials))
      .pipe(
        catchError(this.handleError)
      );
  }

  /**
   * Error handling
   */
  private handleError(error: HttpErrorResponse) {
    let errorMessage = 'An unknown error occurred';
    
    // Server-side error
    if (error.status === 0) {
      // Network error or CORS issue
      errorMessage = 'Network error. Please check your connection.';
    } else {
      errorMessage = `Error Code: ${error.status}\nMessage: ${error.message}`;
      
      if (error.error && error.error.error) {
        errorMessage = error.error.error;
      }
    }
    
    console.error('API Error:', errorMessage);
    return throwError(() => new Error(errorMessage));
  }
}
