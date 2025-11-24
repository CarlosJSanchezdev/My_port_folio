import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ContactService } from '../services/contact.service';

@Component({
  selector: 'app-contact',
  standalone: true,
  imports: [CommonModule, FormsModule, ReactiveFormsModule],
  templateUrl: './contact.component.html',
  styleUrls: ['./contact.component.css']
})
export class ContactComponent {
  contactForm: FormGroup;
  formMessage = '';
  messageType: 'success' | 'error' = 'success';
  isSubmitting = false;

  constructor(
    private fb: FormBuilder,
    private contactService: ContactService
  ) {
    this.contactForm = this.fb.group({
      name: ['', [Validators.required, Validators.minLength(2)]],
      email: ['', [Validators.required, Validators.email]],
      subject: [''],
      message: ['', [Validators.required, Validators.minLength(10)]]
    });
  }

  onSubmit() {
    if (this.contactForm.valid) {
      this.isSubmitting = true;
      this.formMessage = '';
      
      const messageData = {
        name: this.contactForm.value.name,
        email: this.contactForm.value.email,
        subject: this.contactForm.value.subject || '',
        message: this.contactForm.value.message
      };

      // Send to API
      this.contactService.sendMessage(messageData).subscribe({
        next: (response) => {
          this.formMessage = '✅ ¡Gracias por tu mensaje! Te responderé pronto.';
          this.messageType = 'success';
          this.isSubmitting = false;
          this.contactForm.reset();
          
          // Clear message after 5 seconds
          setTimeout(() => {
            this.formMessage = '';
          }, 5000);
        },
        error: (err) => {
          console.error('Error sending message:', err);
          this.formMessage = '❌ Hubo un error al enviar el mensaje. Por favor, intenta de nuevo o contáctame directamente por email.';
          this.messageType = 'error';
          this.isSubmitting = false;
          
          // Clear error message after 7 seconds
          setTimeout(() => {
            this.formMessage = '';
          }, 7000);
        }
      });
    } else {
      this.formMessage = '❌ Por favor, completa todos los campos correctamente.';
      this.messageType = 'error';
      
      // Mark all fields as touched to show errors
      Object.keys(this.contactForm.controls).forEach(key => {
        this.contactForm.get(key)?.markAsTouched();
      });
    }
  }
}

