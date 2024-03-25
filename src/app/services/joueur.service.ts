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
        'Content-Type': 'application/json'
      })
    };

    return this.http.post('http://127.0.0.1:5000/api/joueurs', joueurData, httpOptions);
  }

  rechercheJoueur(nomJoueur: string): Observable<any> {
    return this.http.get(`http://127.0.0.1:5000/api/joueurs/${nomJoueur}`);
  }

}
