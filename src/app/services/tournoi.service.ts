import {Injectable} from '@angular/core';
import {HttpClient, HttpHeaders} from "@angular/common/http";
import { Observable } from 'rxjs';

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
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json',
      })
    };

    return this.http.patch(`/api/tournois/ajout_joueurs/${idTournoi}/${idJoueur}`, {}, httpOptions);
  }
  supprimerTournoi(idTournoi: string): Observable<any> {
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json',
        // Vous pouvez ajouter des en-têtes d'autorisation ou d'autres en-têtes si nécessaire
      })
    };

    return this.http.delete(`/api/tournois/${idTournoi}`, httpOptions);
  }
}
