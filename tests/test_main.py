import unittest
from geopy.distance import geodesic
from main import berechne_gesamtstrecke, berechne_kompakte_route, stadt_koordinaten

class TestBerechneKompakteRoute(unittest.TestCase):
    def test_berechne_kompakte_route(self):
        selected_cities = ["Berlin", "Hamburg", "München", "Düsseldorf", "Bremen"]
        tour = berechne_kompakte_route(selected_cities)
        self.assertEqual(tour[0], "Berlin")
        self.assertEqual(tour[-1], "Berlin")
        self.assertEqual(set(tour), set(selected_cities))

    def test_berechne_kompakte_route_kuerzeste_route(self):
        selected_cities = ["Berlin", "Hamburg", "München", "Düsseldorf", "Bremen"]
        tour = berechne_kompakte_route(selected_cities)
        tour_length = 0
        for i in range(len(tour) - 1):
            tour_length += geodesic(
                stadt_koordinaten[tour[i]], stadt_koordinaten[tour[i + 1]]
            ).kilometers
        #Der Algorithmus berechnet eine kurze, aber nicht unbedingt die kürzeste
        #Distanz. Wir akzeptieren alles, was 1550 bis 1650.
        self.assertAlmostEqual(tour_length, 1600, delta=50)
class TestBerechneGesamtstrecke(unittest.TestCase):

    def test_berechne_gesamtstrecke(self):
        selected_cities = ['Bremen', 'Hamburg', 'Kiel']
        expected_gesamtstrecke = 182.0  # Beispielwert der erwarteten Gesamtstrecke

        actual_gesamtstrecke = berechne_gesamtstrecke(selected_cities)

        self.assertEqual(actual_gesamtstrecke, expected_gesamtstrecke)


if __name__ == '__main__':
    unittest.main()
