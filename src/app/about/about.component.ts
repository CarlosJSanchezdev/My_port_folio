import { CommonModule } from '@angular/common';
import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { RouterModule } from '@angular/router';
import { AuthService } from '../services/auth.service';
import { environment } from '../../environments/environment';

import { PERSONAL_INFO, SKILLS } from '../config/portfolio.config';

interface Skill {
  name: string;
  icon: string;
  level: number;
}

interface SkillCategory {
  name: string;
  skills: Skill[];
}

@Component({
  selector: 'app-about',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './about.component.html',
  styleUrls: ['./about.component.css']
})
export class AboutComponent implements OnInit {
  stats = PERSONAL_INFO.stats;
  accessLevel = 1;
  cvUrl = `${environment.apiUrl}/protected/cv`;

  skillCategories: SkillCategory[] = [
    {
      name: 'Frontend',
      skills: SKILLS.frontend
    },
    {
      name: 'Backend',
      skills: SKILLS.backend
    },
    {
      name: 'Mobile',
      skills: SKILLS.mobile
    },
    {
      name: 'Tools & Others',
      skills: SKILLS.tools
    }
  ];

  constructor(
    private authService: AuthService,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit() {
    this.authService.authStatus$.subscribe(status => {
      this.accessLevel = Number(status.access_level);
      this.cdr.detectChanges();
    });
  }
}
