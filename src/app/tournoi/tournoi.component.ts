import {Component} from '@angular/core';
import {CommonModule} from '@angular/common';
import {HttpClientModule} from '@angular/common/http';
import {TournoiService} from "../services/tournoi.service";
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-tournoi',
  standalone: true,
  imports: [CommonModule, HttpClientModule],
  providers: [TournoiService],
  templateUrl: './tournoi.component.html',
})
export class TournoiComponent {

  items: any;
  showItems = false;
  tournois: any[] | undefined;
  joueurs: any[] | undefined;


  constructor(private http: HttpClient, private serviceTournoi: TournoiService) {
    this.getItems();
    this.getJoueurs();
  }

  getJoueurs() {
    this.serviceTournoi.getJoueurs().subscribe(
      data => {
        this.joueurs = data;
      },
      erreur => {
        console.error('Erreur lors de la récupération des joueurs!', erreur);
      }
    );
  }

  getNomJoueur(idJoueur: string): string {
    // @ts-ignore
    const joueur = this.joueurs.find(joueur => joueur._id === idJoueur);
    return joueur ? joueur.nom + ' ' + joueur.prenom : 'Joueur inconnu';
  }

  getItems() {
    this.serviceTournoi.getTournois().subscribe(
      data => {
        this.items = data;
      },
      erreur => {
        console.error('erreur!', erreur);
      }
    );
  }

  afficherTournois() {
    this.showItems = !this.showItems;
  }

}
