from Tournoi import Tournoi
import unittest


class TestTournoi(unittest.TestCase):
    def setUp(self):
        self.tournoi = Tournoi("Test", "23/03/2024", "Simple", ((12, 34), "Intermediaire"))
        self.jour, self.mois, self.annee = self.tournoi.date.split("/")

    def test_is_instance_of_tournoi(self):
        self.assertIsInstance(self.tournoi, Tournoi)

    def test_nom_tourn_is_str(self):
        self.assertIsInstance(self.tournoi.nom, str)

    def test_date_is_str(self):
        self.assertIsInstance(self.tournoi.date, str)

    def test_long_jour(self):
        self.assertEqual(len(self.jour), 2)

    def test_long_mois(self):
        self.assertEqual(len(self.mois), 2)

    def test_long_annee(self):
        self.assertEqual(len(self.annee), 4)

    def test_format_is_str(self):
        self.assertIsInstance(self.tournoi.format, str)

    def test_niveau_is_str(self):
        self.assertIsInstance(self.tournoi.categorie[1], str)

    if __name__ == "__main__":
        unittest.main()
