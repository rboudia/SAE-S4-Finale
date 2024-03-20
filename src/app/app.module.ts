import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from "@angular/router";
import {routes} from "./app.routes";
import {BrowserModule} from "@angular/platform-browser";
import {TournoiComponent} from "./tournoi/tournoi.component";
import {TournoiService} from "./tournoi/tournoi.service";



@NgModule({
  declarations: [],
  imports: [
    CommonModule,
    BrowserModule,
    RouterModule.forRoot(routes),
  ],
  providers: [TournoiService]
})
export class AppModule { }
