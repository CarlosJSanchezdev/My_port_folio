import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { CommonModule } from '@angular/common';
import { RouterModule,Routes } from '@angular/router';
import { AboutComponent } from './about/about.component';
import { ProjectsComponent } from './projects/projects.component';
import { BlogComponent } from './blog/blog.component';
import { ContactComponent } from './contact/contact.component';
import { FooterComponent } from './footer/footer.component';

export const routes: Routes = [
    {path: '', redirectTo: '/about', pathMatch: 'full'},
    {path: 'about', component: AboutComponent },
    {path: 'projects', component: ProjectsComponent },
    {path: 'blog', component: BlogComponent },
    {path: 'contact', component: ContactComponent },
    {path: 'footer', component: FooterComponent}
];
@NgModule ({
    imports: [
        RouterModule.forRoot(routes),
        BrowserModule,
    ],
    exports: [RouterModule]
})

export class AppRoutingModule {}
