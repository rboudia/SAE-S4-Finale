import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class JoueurService {

  constructor(private http: HttpClient) {}

  getTournois(): Observable<any> {
    return this.http.get('http://127.0.0.1:5000/tournoi');
  }

  rechercheJoueur(nomJoueur: string): Observable<any> {
    return this.http.get(`http://127.0.0.1:5000/joueurs/${nomJoueur}`);
  }

}
