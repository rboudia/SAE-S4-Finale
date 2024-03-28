import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class JoueurService {

  constructor(private http: HttpClient) {}

  ajouterJoueur(joueurData: any): Observable<any> {
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': 'http://127.0.0.1:5000',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS, PUT, DELETE',
        'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept',
      })
    };

    return this.http.post('/api/joueurs', joueurData, httpOptions);
  }

  ajouterJoueurFichier(joueurData: any): Observable<any> {
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': 'http://127.0.0.1:5000',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS, PUT, DELETE',
        'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept',
      })
    };

    return this.http.post('/api/joueurs/insertion_fichier', joueurData, httpOptions);
  }
  rechercheJoueur(nomJoueur: string): Observable<any> {
    return this.http.get(`/api/joueurs/${nomJoueur}`);
  }
  afficherJoueur(): Observable<any> {
    return this.http.get('/api/joueurs/');
  }

  supprimerJoueur(id: string): Observable<any> {
    return this.http.delete(`/api/joueurs/${id}`);
  }

}
