import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { EquipementService } from '../services/equipement.service';

@Component({
  selector: 'app-equipement',
  standalone: true,
  imports: [CommonModule, HttpClientModule, FormsModule],
  providers: [EquipementService],
  templateUrl: './equipement.component.html',
})
export class EquipementComponent implements OnInit {
  equipements: any[] = [];
  type: string = '';
  nombre: string = '';

  constructor(private equipementService: EquipementService) {}

  ngOnInit(): void {
    this.afficherEquipements();
  }

  afficherEquipements(): void {
    this.equipementService.afficherEquipements().subscribe(
      (data: any) => {
        this.equipements = data;
      },
      (error) => {
        console.error('Erreur lors de la récupération des équipements :', error);
      }
    );
  }

  insererEquipement(): void {
    if (this.type.trim() === '' || this.nombre.trim() === '') {
      return;
    }
    this.equipementService.insererEquipement(this.type.trim(), this.nombre.trim()).subscribe(
      () => {
        console.log('Equipement inséré avec succès');
        this.type = '';
        this.nombre = '';
      },
      (error) => {
        console.error('Erreur lors de l\'insertion de l\'équipement :', error);
      }
    );
  }



  supprimerEquipement(id: string): void {
    this.equipementService.supprimerEquipement(id).subscribe(
      () => {
        console.log('Equipement supprimé avec succès');
        this.afficherEquipements();
      },
      (error) => {
        console.error('Erreur lors de la suppression de l\'équipement :', error);
      }
    );
  }
}
