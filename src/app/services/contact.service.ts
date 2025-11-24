import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { ApiService } from './api.service';

export interface ContactMessage {
  name: string;
  email: string;
  subject?: string;
  message: string;
}

export interface ContactResponse {
  success: boolean;
  data?: any;
  message: string;
}

@Injectable({
  providedIn: 'root'
})
export class ContactService {
  constructor(private api: ApiService) {}

  /**
   * Send a contact message
   */
  sendMessage(message: ContactMessage): Observable<ContactResponse> {
    return this.api.post<ContactResponse>('contact', message);
  }

  /**
   * Validate email format
   */
  isValidEmail(email: string): boolean {
    const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    return emailRegex.test(email);
  }

  /**
   * Validate message data before sending
   */
  validateMessage(message: ContactMessage): { valid: boolean; errors: string[] } {
    const errors: string[] = [];

    if (!message.name || message.name.trim().length < 2) {
      errors.push('Name must be at least 2 characters long');
    }

    if (!message.email || !this.isValidEmail(message.email)) {
      errors.push('Please provide a valid email address');
    }

    if (!message.message || message.message.trim().length < 10) {
      errors.push('Message must be at least 10 characters long');
    }

    return {
      valid: errors.length === 0,
      errors
    };
  }
}
