import { Component, EventEmitter, Input, Output, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-verification-modal',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './verification-modal.component.html',
  styleUrls: ['./verification-modal.component.css']
})
export class VerificationModalComponent implements OnInit, OnDestroy {
  @Input() isOpen = false;
  @Input() email = '';
  @Input() name = '';
  @Output() verified = new EventEmitter<void>();
  @Output() closed = new EventEmitter<void>();

  code = '';
  isVerifying = false;
  errorMessage = '';
  timeRemaining = 900; // 15 minutos
  canResend = false;
  resendTimer = 60;
  
  private timerInterval: any;
  private resendInterval: any;

  constructor(private authService: AuthService) {}

  ngOnInit() {
    if (this.isOpen) {
      this.startTimer();
      this.startResendTimer();
    }
  }

  ngOnDestroy() {
    this.clearTimers();
  }

  ngOnChanges() {
    if (this.isOpen) {
      this.code = '';
      this.errorMessage = '';
      this.timeRemaining = 900;
      this.resendTimer = 60;
      this.canResend = false;
      this.clearTimers();
      this.startTimer();
      this.startResendTimer();
    }
  }

  clearTimers() {
    if (this.timerInterval) clearInterval(this.timerInterval);
    if (this.resendInterval) clearInterval(this.resendInterval);
  }

  startTimer() {
    this.timerInterval = setInterval(() => {
      this.timeRemaining--;
      if (this.timeRemaining <= 0) {
        clearInterval(this.timerInterval);
        this.errorMessage = 'Código expirado. Solicita uno nuevo.';
      }
    }, 1000);
  }

  startResendTimer() {
    this.resendInterval = setInterval(() => {
      this.resendTimer--;
      if (this.resendTimer <= 0) {
        this.canResend = true;
        clearInterval(this.resendInterval);
      }
    }, 1000);
  }

  formatTime(seconds: number): string {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  }

  onCodeInput() {
    this.errorMessage = '';
    // Permitir solo números
    this.code = this.code.replace(/[^0-9]/g, '');
    
    if (this.code.length === 6) {
      this.verify();
    }
  }

  verify() {
    if (this.code.length !== 6) return;
    
    this.isVerifying = true;
    this.errorMessage = '';

    this.authService.verifyCode(this.email, this.code, this.name).subscribe({
      next: (response) => {
        this.isVerifying = false;
        this.verified.emit();
        this.close();
      },
      error: (err) => {
        this.isVerifying = false;
        this.errorMessage = err.error?.error || 'Error al verificar el código';
        this.code = '';
      }
    });
  }

  resendCode() {
    if (!this.canResend) return;
    
    this.authService.requestVerification(this.email, this.name).subscribe({
      next: () => {
        this.canResend = false;
        this.resendTimer = 60;
        this.timeRemaining = 900;
        this.startResendTimer();
        this.errorMessage = '';
        this.code = '';
      },
      error: (err) => {
        this.errorMessage = err.error?.error || 'Error al reenviar código';
      }
    });
  }

  close() {
    this.closed.emit();
  }
}
