import {Component} from '@angular/core';
import {CommonModule} from '@angular/common';
import {HttpClientModule} from '@angular/common/http';
import {TournoiService} from "../services/tournoi.service";
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-tournoi',
  standalone: true,
  imports: [CommonModule, HttpClientModule],
  providers: [TournoiService],
  templateUrl: './tournoi.component.html',
})
export class TournoiComponent {

  items: any;
  showItems = false;


  constructor(private http: HttpClient, private serviceTournoi: TournoiService) {
    this.getItems();
  }

  getItems() {
    this.serviceTournoi.getTournois().subscribe(
      data => {
        this.items = data;
      },
      erreur => {
        console.error('erreur!', erreur);
      }
    );
  }

  afficherTournois() {
    this.showItems = !this.showItems;
  }

}
