import {Component} from '@angular/core';
import {CommonModule} from '@angular/common';
import {HttpClientModule} from '@angular/common/http';
import {FormsModule} from '@angular/forms';
import {MatchService} from '../services/match.service';
import {RouterOutlet} from "@angular/router";

@Component({
  selector: 'app-match',
  standalone: true,
  imports: [CommonModule, RouterOutlet, HttpClientModule, FormsModule],
  providers: [MatchService],
  templateUrl: './match.component.html',
})

export class MatchComponent {
  nomTournoi: string = '';
  matchs: any[] = [];

  constructor(private serviceMatch: MatchService) { }

  rechercherMatchs(): void {
    if (this.nomTournoi.trim()) {
      this.serviceMatch.rechercherMatchsParNomTournoi(this.nomTournoi)
        .subscribe(matchs => {
          this.matchs = matchs;
        });
    }
  }
}
