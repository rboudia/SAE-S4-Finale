import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { JoueurService } from '../services/joueur.service';
import {RouterOutlet} from "@angular/router";

@Component({
  selector: 'app-joueur',
  standalone: true,
  imports: [CommonModule, RouterOutlet, HttpClientModule, FormsModule],
  providers: [JoueurService],
  templateUrl: './joueur.component.html',
})
export class JoueurComponent {
  title = 'Projet';
  showItems2 = false;
  nomJoueur = '';
  joueurInfo: any = null;

  constructor(private joueurService: JoueurService) {}

  rechercheJoueur() {
    if (!this.nomJoueur) {
      alert('Entrez un nom de joueur.');
      return;
    }
    this.joueurService.rechercheJoueur(this.nomJoueur).subscribe(
      data => {
        this.joueurInfo = data;
        this.showItems2 = true;
      },
      erreur => {
        console.error('Erreur!', erreur);
      }
    );
  }
}
