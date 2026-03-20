import { Component, OnInit, Inject, PLATFORM_ID, signal } from '@angular/core';
import { CommonModule, isPlatformBrowser } from '@angular/common';
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
  // Signals para estado reactivo
  readonly contactForm: FormGroup;
  readonly formMessage = signal<string>('');
  readonly messageType = signal<'success' | 'error' | 'info'>('info');
  readonly isSubmitting = signal(false);
  readonly accessLevel = signal<number>(1);
  readonly ownerInfo = signal<OwnerInfo[]>([]);
  readonly isVerificationModalOpen = signal(false);
  readonly verificationEmail = signal('');
  readonly verificationName = signal('');
  readonly isLoadingInfo = signal(false);
  readonly isVerified = signal(false);

  // Claves para localStorage
  private readonly VERIFIED_KEY = 'portfolio_verified';
  private readonly VERIFIED_EMAIL_KEY = 'portfolio_verified_email';
  private readonly VERIFIED_EXPIRY_KEY = 'portfolio_verified_expiry';

  constructor(
    private fb: FormBuilder,
    private contactService: ContactService,
    private authService: AuthService,
    @Inject(PLATFORM_ID) private platformId: Object
  ) {
    this.contactForm = this.fb.group({
      name: ['', [Validators.required, Validators.minLength(2)]],
      email: ['', [Validators.required, Validators.email]],
      subject: [''],
      message: ['', [Validators.required, Validators.minLength(10)]]
    });
  }

  ngOnInit() {
    if (isPlatformBrowser(this.platformId)) {
      // Verificar si ya está verificado en localStorage
      this.checkStoredVerification();

      // Suscribirse a cambios de autenticación
      this.authService.authStatus$.subscribe(status => {
        this.accessLevel.set(status.access_level);
        
        // Si el nivel es 3 o más, marcar como verificado
        if (status.access_level >= 3) {
          this.isVerified.set(true);
        }
        
        this.loadOwnerInfo();
      });
    }
  }

  /**
   * Verifica si hay una verificación guardada en localStorage
   */
  checkStoredVerification() {
    const isVerified = localStorage.getItem(this.VERIFIED_KEY);
    const expiry = localStorage.getItem(this.VERIFIED_EXPIRY_KEY);
    
    if (isVerified === 'true' && expiry) {
      const expiryDate = new Date(expiry);
      const now = new Date();
      
      // Verificación válida por 30 días
      if (now < expiryDate) {
        this.isVerified.set(true);
        const email = localStorage.getItem(this.VERIFIED_EMAIL_KEY);
        if (email) {
          this.verificationEmail.set(email);
        }
      } else {
        // Expirado, limpiar
        this.clearStoredVerification();
      }
    }
  }

  /**
   * Guarda la verificación en localStorage (30 días)
   */
  storeVerification(email: string) {
    if (isPlatformBrowser(this.platformId)) {
      const now = new Date();
      const expiry = new Date(now.getTime() + (30 * 24 * 60 * 60 * 1000)); // 30 días
      
      localStorage.setItem(this.VERIFIED_KEY, 'true');
      localStorage.setItem(this.VERIFIED_EMAIL_KEY, email);
      localStorage.setItem(this.VERIFIED_EXPIRY_KEY, expiry.toISOString());
      
      this.isVerified.set(true);
    }
  }

  /**
   * Limpia la verificación almacenada
   */
  clearStoredVerification() {
    if (isPlatformBrowser(this.platformId)) {
      localStorage.removeItem(this.VERIFIED_KEY);
      localStorage.removeItem(this.VERIFIED_EMAIL_KEY);
      localStorage.removeItem(this.VERIFIED_EXPIRY_KEY);
      this.isVerified.set(false);
    }
  }

  loadOwnerInfo() {
    this.isLoadingInfo.set(true);
    this.authService.getOwnerInfo().subscribe({
      next: (response) => {
        if (response.success) {
          this.ownerInfo.set(response.data);
        }
        this.isLoadingInfo.set(false);
      },
      error: (err) => {
        console.error('Error loading owner info:', err);
        this.isLoadingInfo.set(false);
      }
    });
  }

  openVerificationModal() {
    // Si ya está verificado, no hacer nada
    if (this.isVerified()) {
      return;
    }

    const emailControl = this.contactForm.get('email');
    const nameControl = this.contactForm.get('name');
    
    if (emailControl?.valid && nameControl?.valid) {
      this.verificationEmail.set(emailControl.value);
      this.verificationName.set(nameControl.value);
      this.requestVerificationCode();
    } else {
      this.formMessage.set('⚠️ Por favor ingresa tu nombre y email para verificar tu identidad.');
      this.messageType.set('info');
      emailControl?.markAsTouched();
      nameControl?.markAsTouched();
    }
  }

  requestVerificationCode() {
    this.isSubmitting.set(true);
    this.authService.requestVerification(this.verificationEmail(), this.verificationName()).subscribe({
      next: () => {
        this.isSubmitting.set(false);
        this.isVerificationModalOpen.set(true);
      },
      error: (err) => {
        this.isSubmitting.set(false);
        this.formMessage.set(err.error?.error || 'Error al solicitar código. Intenta de nuevo.');
        this.messageType.set('error');
      }
    });
  }

  onVerified() {
    // Guardar verificación en localStorage
    this.storeVerification(this.verificationEmail());
    
    this.formMessage.set('✅ ¡Verificación exitosa! Información desbloqueada por 30 días.');
    this.messageType.set('success');
    
    // Recargar información de owner
    this.loadOwnerInfo();
    
    setTimeout(() => this.formMessage.set(''), 5000);
  }

  closeVerificationModal() {
    this.isVerificationModalOpen.set(false);
  }

  onSubmit() {
    if (this.contactForm.valid) {
      this.isSubmitting.set(true);
      this.formMessage.set('');

      const messageData = {
        name: this.contactForm.value.name,
        email: this.contactForm.value.email,
        subject: this.contactForm.value.subject || '',
        message: this.contactForm.value.message
      };

      this.contactService.sendMessage(messageData).subscribe({
        next: (response) => {
          this.formMessage.set('✅ ¡Gracias por tu mensaje! Te responderé pronto.');
          this.messageType.set('success');
          this.isSubmitting.set(false);
          this.contactForm.reset();
          setTimeout(() => this.formMessage.set(''), 5000);
        },
        error: (err) => {
          console.error('Error sending message:', err);
          this.formMessage.set('❌ Hubo un error. Por favor contáctame directamente por email.');
          this.messageType.set('error');
          this.isSubmitting.set(false);
          setTimeout(() => this.formMessage.set(''), 7000);
        }
      });
    } else {
      this.formMessage.set('❌ Por favor, completa todos los campos correctamente.');
      this.messageType.set('error');
      Object.keys(this.contactForm.controls).forEach(key => {
        this.contactForm.get(key)?.markAsTouched();
      });
    }
  }
}
