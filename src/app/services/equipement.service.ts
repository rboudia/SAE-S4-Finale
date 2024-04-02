import { Injectable } from '@angular/core';
import { HttpClient} from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class EquipementService {

  constructor(private http: HttpClient) {}

  afficherEquipements(): Observable<any> {
    return this.http.get('/api/equipements/');
  }

  insererEquipement(type: string, nombre: string): Observable<any> {
    const equipement = { type };
    return this.http.post(`/api/equipements/${nombre}`, equipement);
  }

  supprimerEquipement(id: string): Observable<any> {
    return this.http.delete(`/api/equipements/${id}`);
  }
}
