import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from "@angular/router";
import {routes} from "./app.routes";
import {BrowserModule} from "@angular/platform-browser";
import {TournoiService} from "./services/tournoi.service";





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
