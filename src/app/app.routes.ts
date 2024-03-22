import { Routes } from '@angular/router';
import {TournoiComponent} from "./tournoi/tournoi.component";
import {JoueurComponent} from "./joueur/joueur.component";

export const routes: Routes = [
  {path:'tournois', component: TournoiComponent},
  {path:'joueurs', component: JoueurComponent},
];
