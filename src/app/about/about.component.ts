import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';

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
export class AboutComponent {
  stats = PERSONAL_INFO.stats;

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
}
