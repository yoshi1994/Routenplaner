import unittest
from geopy.distance import geodesic
from main import berechne_gesamtstrecke, berechne_kompakte_route, stadt_koordinaten
from parameterized import parameterized

class TestBerechneKompakteRoute(unittest.TestCase):
    @parameterized.expand([
        (["Berlin", "Hamburg", "München", "Düsseldorf", "Bremen"],),
        (["München", "Düsseldorf", "Berlin", "Bremen", "Hamburg"],),
        (["Hamburg", "Berlin", "Düsseldorf", "Bremen", "München"],),
        (["München", "Bremen", "Hamburg", "Düsseldorf", "Berlin"],),
        (["Bremen", "Hamburg", "Berlin", "Düsseldorf", "München"],),
        (["Berlin", "Hamburg", "München", "Stuttgart", "Bremen"],),
        (["Berlin", "Hamburg", "München", "Düsseldorf", "Bremen", "Schwerin"],),
        # Weitere Routenoptionen hier hinzufügen
    ])
    def test_berechne_kompakte_route(self, selected_cities):
        tour = berechne_kompakte_route(selected_cities)
        self.assertEqual(tour[0], selected_cities[0])
        self.assertEqual(tour[-1], selected_cities[0])
        self.assertEqual(set(tour), set(selected_cities))

    @parameterized.expand([
        (["Hannover", "Bremen", "Schwerin", "Potsdam", "Kiel"], 760),
        (["Stuttgart", "Erfurt", "Saarbrücken", "Dresden", "Magdeburg"], 1250),
        (["Mainz", "Wiesbaden", "Kiel", "Potsdam", "Hamburg"], 1200),
        (["Düsseldorf", "München", "Schwerin", "Berlin", "Hannover"], 1600),
        (["Hamburg", "Schwerin", "Bremen", "Stuttgart", "Dresden"], 1650),
        (["Saarbrücken", "Erfurt", "Kiel", "Hannover", "Wiesbaden"], 1350),
        (["Mainz", "Magdeburg", "Düsseldorf", "Kiel", "Hannover"], 1300),
        (["Wiesbaden", "Stuttgart", "Hamburg", "Bremen", "Dresden"], 1400),
        (["Potsdam", "Saarbrücken", "Hannover", "Magdeburg", "Stuttgart"], 1300),
        (["Kiel", "Mainz", "Bremen", "Erfurt", "Stuttgart"], 1450),
        (["Kiel", "Erfurt", "Stuttgart", "Mainz", "Bremen"], 1450),
        # Weitere Routenoptionen hier hinzufügen
    ])
    def test_berechne_kompakte_route_kuerzeste_route(self, selected_cities, expected_length):
        tour = berechne_kompakte_route(selected_cities)
        tour_length = 0
        for i in range(len(tour) - 1):
            tour_length += geodesic(
                stadt_koordinaten[tour[i]], stadt_koordinaten[tour[i + 1]]
            ).kilometers
        self.assertAlmostEqual(tour_length, expected_length, delta=50)


class TestBerechneGesamtstrecke(unittest.TestCase):
    @parameterized.expand([
        (['Bremen', 'Hamburg', 'Kiel'], 182.0),
        (['Kiel', 'Hamburg', 'Bremen'], 182.0),
        (['Hamburg', 'Bremen', 'Kiel'], 259.0),
        (['Kiel', 'Bremen', 'Hamburg'], 259.0),
        (['Bremen', 'Hamburg', 'Kiel', 'Schwerin'], 295.0),
        (['Bremen', 'Hamburg', 'Kiel', 'Stuttgart'], 802.0),
        (['Bremen', 'Hamburg', 'Kiel', 'Potsdam'], 472.0),
        (['Bremen', 'Hamburg', 'Kiel', 'Hannover'], 400.0),
        (['Bremen', 'Hamburg', 'Kiel', 'Saarbrücken'], 787.0),
        (['Bremen', 'Hamburg', 'Kiel', 'Mainz'], 679.0),
        (['Bremen', 'Hamburg', 'Kiel', 'Wiesbaden'], 671.0),
        (['Bremen', 'Hamburg', 'Kiel', 'Düsseldorf'], 594.0),
        (['Bremen', 'Hamburg', 'Kiel', 'Magdeburg'], 446),
        # Weitere Routenoptionen hier hinzufügen
    ])
    def test_berechne_gesamtstrecke(self, selected_cities, expected_gesamtstrecke):
        actual_gesamtstrecke = berechne_gesamtstrecke(selected_cities)
        self.assertEqual(expected_gesamtstrecke, actual_gesamtstrecke)


if __name__ == '__main__':
    unittest.main()
