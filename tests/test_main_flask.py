import unittest
from main import app

class TestFlaskRoutes(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
    def test_index_get(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Berechnen Sie Ihre Rundreise", response.data)
    def test_index_post_selected_cities(self):
        response = self.app.post("/", data={"Stuttgart": "on", "München": "on"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("Ausgewählte Städte: Stuttgart, München".encode(), response.data)

    def test_index_post_invalid_cities(self):
        response = self.app.post("/", data={"Stuttgart": "on"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("Bitte mindestens 2 Städte auswählen, um eine Strecke zu berechnen.".encode(), response.data)

if __name__ == '__main__':
    unittest.main()
