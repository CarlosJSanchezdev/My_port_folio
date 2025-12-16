import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ContactService } from '../services/contact.service';
import { AuthService, OwnerInfo } from '../services/auth.service';
import { VerificationModalComponent } from '../components/verification-modal/verification-modal.component';

@Component({
  selector: 'app-contact',
  standalone: true,
  imports: [CommonModule, FormsModule, ReactiveFormsModule, VerificationModalComponent],
  templateUrl: './contact.component.html',
  styleUrls: ['./contact.component.css']
})
export class ContactComponent implements OnInit {
  contactForm: FormGroup;
  formMessage = '';
  messageType: 'success' | 'error' = 'success';
  isSubmitting = false;
  
  // Auth & Owner Info
  accessLevel = 1;
  ownerInfo: OwnerInfo[] = [];
  isVerificationModalOpen = false;
  verificationEmail = '';
  verificationName = '';
  isLoadingInfo = false;

  constructor(
    private fb: FormBuilder,
    private contactService: ContactService,
    private authService: AuthService
  ) {
    this.contactForm = this.fb.group({
      name: ['', [Validators.required, Validators.minLength(2)]],
      email: ['', [Validators.required, Validators.email]],
      subject: [''],
      message: ['', [Validators.required, Validators.minLength(10)]]
    });
  }

  ngOnInit() {
    // Suscribirse a cambios de estado de autenticación
    this.authService.authStatus$.subscribe(status => {
      this.accessLevel = status.access_level;
      this.loadOwnerInfo();
    });
  }

  loadOwnerInfo() {
    this.isLoadingInfo = true;
    this.authService.getOwnerInfo().subscribe({
      next: (response) => {
        if (response.success) {
          this.ownerInfo = response.data;
        }
        this.isLoadingInfo = false;
      },
      error: (err) => {
        console.error('Error loading owner info:', err);
        this.isLoadingInfo = false;
      }
    });
  }

  openVerificationModal() {
    // Si el usuario ya llenó el formulario, usamos esos datos
    if (this.contactForm.get('email')?.valid && this.contactForm.get('name')?.valid) {
      this.verificationEmail = this.contactForm.get('email')?.value;
      this.verificationName = this.contactForm.get('name')?.value;
      this.requestVerificationCode();
    } else {
      // Si no, pedimos que llene al menos nombre y email
      this.formMessage = '⚠️ Por favor ingresa tu nombre y email para verificar tu identidad.';
      this.messageType = 'error';
      this.contactForm.get('name')?.markAsTouched();
      this.contactForm.get('email')?.markAsTouched();
    }
  }

  requestVerificationCode() {
    this.isSubmitting = true;
    this.authService.requestVerification(this.verificationEmail, this.verificationName).subscribe({
      next: () => {
        this.isSubmitting = false;
        this.isVerificationModalOpen = true;
      },
      error: (err) => {
        this.isSubmitting = false;
        this.formMessage = err.error?.error || 'Error al solicitar código. Intenta de nuevo.';
        this.messageType = 'error';
      }
    });
  }

  onVerified() {
    this.formMessage = '✅ ¡Verificación exitosa! Has desbloqueado información adicional.';
    this.messageType = 'success';
    setTimeout(() => this.formMessage = '', 5000);
  }

  closeVerificationModal() {
    this.isVerificationModalOpen = false;
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
