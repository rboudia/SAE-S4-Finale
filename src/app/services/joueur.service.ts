import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse} from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class JoueurService {

  constructor(private http: HttpClient) {}

  ajouterJoueur(joueurData: any): Observable<any> {
    return this.http.post('/api/joueurs', joueurData);
  }

  ajouterJoueurFichier(joueurData: any): Observable<any> {
    return this.http.post('/api/joueurs/insertion_fichier', joueurData);
  }
  rechercheJoueur(nomJoueur: string): Observable<any> {
    return this.http.get(`/api/joueurs/${nomJoueur}`).pipe(
      catchError((error: HttpErrorResponse) => {
        return throwError(error);
      })
    );
  }
  afficherJoueur(): Observable<any> {
    return this.http.get('/api/joueurs/');
  }

  supprimerJoueur(id: string): Observable<any> {
    return this.http.delete(`/api/joueurs/${id}`);
  }

}
