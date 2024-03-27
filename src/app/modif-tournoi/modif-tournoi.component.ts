import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { TournoiService } from '../services/tournoi.service';
import { JoueurService } from '../services/joueur.service';
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-modif-tournoi',
  standalone: true,
  imports: [CommonModule, HttpClientModule, RouterModule],
  providers: [TournoiService, JoueurService],
  templateUrl: './modif-tournoi.component.html',
})
export class ModifTournoiComponent implements OnInit {
  tournoi: any;
  joueurs: any[] | undefined;

  constructor(private route: ActivatedRoute, private tournoiService: TournoiService, private joueurService: JoueurService) { }

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      const id = params['id'];
      this.tournoiService.getTournoiById(id).subscribe(
        (data: any) => {
          this.tournoi = data;
        },
        error => {
          console.error('Erreur lors de la récupération du tournoi:', error);
        }
      );
    });
    this.joueurService.afficherJoueur().subscribe(
      (data: any[]) => {
        this.joueurs = data;
      },
      error => {
        console.error('Erreur lors de la récupération des joueurs:', error);
      }
    );
  }
  inscrireJoueur(idJoueur: string): void {
    const idTournoi = this.tournoi._id; // Récupérer l'ID du tournoi actuel
    this.tournoiService.inscrireJoueurAuTournoi(idTournoi, idJoueur).subscribe(
      (response: any) => {
        console.log(response); // Afficher la réponse du serveur après l'inscription
        // Ajoutez ici toute logique supplémentaire après l'inscription du joueur
      },
      error => {
        console.error('Erreur lors de l\'inscription du joueur au tournoi:', error);
      }
    );
  }
  supprimerTournoi(): void {
    const idTournoi = this.tournoi._id;
    this.tournoiService.supprimerTournoi(idTournoi).subscribe(
      (response: any) => {
        console.log(response); // Afficher la réponse du serveur après la suppression
        // Ajoutez ici toute logique supplémentaire après la suppression du tournoi
      },
      error => {
        console.error('Erreur lors de la suppression du tournoi:', error);
      }
    );
  }
}

