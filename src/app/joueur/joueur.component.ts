import {Component} from '@angular/core';
import {CommonModule} from '@angular/common';
import {HttpClientModule} from '@angular/common/http';
import {FormsModule} from '@angular/forms';
import {JoueurService} from '../services/joueur.service';
import {RouterOutlet} from "@angular/router";
import {Joueur} from './joueur.module';

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
  nom = '';
  prenom = '';
  age = '';
  niveau = '';
  joueurs: Joueur[] = [];
  fichierCharge: boolean = false;
  erreurMessage: string = '';

  constructor(private joueurService: JoueurService) {
  }

  rechercheJoueur() {
    if (!this.nomJoueur) {
      this.erreurMessage = 'Entrez un nom de joueur.';
      return;
    }
    this.joueurService.rechercheJoueur(this.nomJoueur).subscribe(
      (data) => {
        this.joueurInfo = data;
        this.showItems2 = true;
        this.erreurMessage = '';
      },
      (error) => {
        console.error('Erreur!', error);
        if (error.status === 404) {
          this.erreurMessage = "Aucun joueur n'a été trouvé avec ce nom.";
        } else {
          this.erreurMessage = 'Une erreur s\'est produite. Veuillez réessayer plus tard.';
        }
      }
    );
  }

  inscrireJoueur() {
    const joueurData = {
      nom: this.nom,
      prenom: this.prenom,
      age: this.age,
      niveau: this.niveau
    };
    this.joueurService.ajouterJoueur(joueurData).subscribe(
      data => {
        console.log('Joueur inscrit avec succès', data);
        alert("Joueur inscrit !");
      },
      erreur => {
        console.error('Erreur lors de l\'inscription du joueur', erreur);
      }
    );
  }
  onFileChange(event: any) {
    const file = event.target.files[0];
    const reader = new FileReader();
    reader.onload = () => {
      const jsonData = reader.result as string;
      this.joueurs = JSON.parse(jsonData);
      this.fichierCharge = true;
    };
    reader.readAsText(file);
  }

  inscrireJoueurFichier() {
    if (this.joueurs.length === 0) {
      alert("Aucun joueur à inscrire.");
      return;
    }
    this.joueurService.ajouterJoueurFichier(this.joueurs).subscribe(
      () => {
        console.log('Joueurs inscrits avec succès');
        alert("Joueurs inscrits !")
      },
      erreur => {
        console.error('Erreur lors de l\'inscription des joueurs', erreur);
      }
    );
  }

  supprimerJoueur(id: string) {
      this.joueurService.supprimerJoueur(id).subscribe(
        () => {
          console.log('Joueur supprimé avec succès');
          this.joueurInfo = null;
        },
        erreur => {
          console.error('Erreur lors de la suppression du joueur', erreur);
        }
      );
  }
}
