from Tournoi import Tournoi
import unittest


class TestTournoi(unittest.TestCase):
    def setUp(self):
        self.tournoi = Tournoi("Test", "23/03/2024", "Simple", ((12, 34), "Intermediaire"))

    def test_nom_tournoi_alphanumerique(self):
        assert self.tournoi.nom.isalnum(), "Le nom doit être alphanumérique"

    if __name__ == "__main__":
        unittest.main()
