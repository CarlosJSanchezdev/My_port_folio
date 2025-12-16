import { ComponentFixture, TestBed, fakeAsync, tick } from '@angular/core/testing';
import { ContactComponent } from './contact.component';
import { ReactiveFormsModule } from '@angular/forms';
import { ContactService } from '../services/contact.service';
import { AuthService } from '../services/auth.service';
import { of, throwError, BehaviorSubject } from 'rxjs';
import { CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';

describe('ContactComponent', () => {
  let component: ContactComponent;
  let fixture: ComponentFixture<ContactComponent>;
  let contactServiceSpy: jasmine.SpyObj<ContactService>;
  let authServiceSpy: jasmine.SpyObj<AuthService>;
  
  // Mock para authStatus$
  const mockAuthStatus = new BehaviorSubject({ isAuthenticated: false, accessLevel: 1 });

  beforeEach(async () => {
    // Crear spies para los servicios
    const cSpy = jasmine.createSpyObj('ContactService', ['sendMessage']);
    const aSpy = jasmine.createSpyObj('AuthService', ['getOwnerInfo'], {
      authStatus$: mockAuthStatus.asObservable()
    });

    // Configurar retorno por defecto de getOwnerInfo
    aSpy.getOwnerInfo.and.returnValue(of([]));

    await TestBed.configureTestingModule({
      declarations: [ContactComponent],
      imports: [ReactiveFormsModule],
      providers: [
        { provide: ContactService, useValue: cSpy },
        { provide: AuthService, useValue: aSpy }
      ],
      schemas: [CUSTOM_ELEMENTS_SCHEMA] // Para ignorar componentes hijos como app-verification-modal en tests superficiales
    }).compileComponents();

    contactServiceSpy = TestBed.inject(ContactService) as jasmine.SpyObj<ContactService>;
    authServiceSpy = TestBed.inject(AuthService) as jasmine.SpyObj<AuthService>;

    fixture = TestBed.createComponent(ContactComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
