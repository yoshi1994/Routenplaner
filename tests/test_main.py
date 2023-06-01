import unittest
from geopy.distance import geodesic
from main import berechne_gesamtstrecke, stadt_koordinaten

class TestBerechneGesamtstrecke(unittest.TestCase):

    def test_berechne_gesamtstrecke(self):
        selected_cities = ['Bremen', 'Hamburg', 'Kiel']
        expected_gesamtstrecke = 182.0  # Beispielwert der erwarteten Gesamtstrecke

        actual_gesamtstrecke = berechne_gesamtstrecke(selected_cities)

        self.assertEqual(actual_gesamtstrecke, expected_gesamtstrecke)


if __name__ == '__main__':
    unittest.main()
