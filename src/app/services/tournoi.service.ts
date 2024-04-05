import {Injectable} from '@angular/core';
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {Observable} from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class TournoiService {

  constructor(private http: HttpClient) {
  }

  getTournois() {
    return this.http.get("/api/tournois")
  }

  insererTournoi(tournoi: any): Observable<any> {
    return this.http.post<any>("/api/tournois", tournoi);
  }

  getTournoiById(id: string) {
    return this.http.get(`/api/tournois/${id}`);
  }

  inscrireJoueurAuTournoi(idTournoi: string, idJoueur: string): Observable<any> {
    return this.http.patch(`/api/tournois/ajout_joueurs/${idTournoi}/${idJoueur}`, {});
  }

  supprimerTournoi(idTournoi: string): Observable<any> {
    return this.http.delete(`/api/tournois/${idTournoi}`);
  }

  creerMatch(idTournoi: string): Observable<any> {
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json',
      })
    };
    return this.http.patch(`/api/tournois/creer_match/${idTournoi}`, httpOptions);
  }

  modifierNomTournoi(idTournoi: string, champ: string, ancienNom: string, nouveauNom: string): Observable<any> {
    return this.http.patch(`/api/tournois/modif/${idTournoi}/${champ}/${ancienNom}/${nouveauNom}`, {});
  }

  nbMaxInscrits(idTournoi: string) {
    return this.http.get(`api/tournois/nb_max_inscription/${idTournoi}`);
  }

  recupNbMatchsTournoi(nomTournoi: string): Observable<any> {
    return this.http.get(`/api/tournois/nb_matchs_tournoi/${nomTournoi}`);
  }
}
