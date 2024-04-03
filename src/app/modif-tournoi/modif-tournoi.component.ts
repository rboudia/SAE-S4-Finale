import {Component, OnInit} from '@angular/core';
import {ActivatedRoute, Router} from '@angular/router';
import {TournoiService} from '../services/tournoi.service';
import {JoueurService} from '../services/joueur.service';
import {CommonModule} from '@angular/common';
import {HttpClientModule} from '@angular/common/http';
import {RouterModule} from '@angular/router';
import {FormsModule} from '@angular/forms';


@Component({
  selector: 'app-modif-tournoi',
  standalone: true,
  imports: [CommonModule, HttpClientModule, RouterModule, FormsModule],
  providers: [TournoiService, JoueurService],
  templateUrl: './modif-tournoi.component.html',
})
export class ModifTournoiComponent implements OnInit {
  tournoi: any;
  joueurs: any[] | undefined;
  nouveauChamp: string = '';
  nouveauChamp2: string = '';
  nouveauChamp3: string = '';

  constructor(private router: Router, private route: ActivatedRoute, private tournoiService: TournoiService, private joueurService: JoueurService) {
  }

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
    const idTournoi = this.tournoi._id;
    this.tournoiService.inscrireJoueurAuTournoi(idTournoi, idJoueur).subscribe(
      (response: any) => {
        console.log(response);
        this.router.navigate([`/modifier-tournoi/${idTournoi}`]);
      },
      error => {
        console.error('Erreur lors de l\'inscription du joueur au tournoi:', error);
      }
    );
  }

  confirmerSuppression() {
    if (confirm("Êtes-vous sûr de vouloir supprimer ce tournoi ?")) {
      this.supprimerTournoi();
    }
  }

  supprimerTournoi(): void {
    const idTournoi = this.tournoi._id;
    this.tournoiService.supprimerTournoi(idTournoi).subscribe(
      (response: any) => {
        console.log(response);
      },
      error => {
        console.error('Erreur lors de la suppression du tournoi:', error);
      }
    );
  }

  creerMatch(): void {
    const idTournoi = this.tournoi._id;
    this.tournoiService.creerMatch(idTournoi).subscribe(
      (response: any) => {
        console.log(response);
      },
      error => {
        console.error('Erreur lors de la creation de match:', error);
      }
    );
  }

  modifierChampTournoi(idTournoi: string, champ: string, ancienNom: string, nouveauNom: string): void {
    this.tournoiService.modifierNomTournoi(idTournoi, champ, ancienNom, nouveauNom).subscribe(
      () => {
        console.log('Tournoi modifié avec succès');
      },
      error => {
        console.error('Erreur lors de la modification du tournoi:', error);
      }
    );
  }


}

