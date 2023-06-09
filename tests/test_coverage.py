import coverage
import unittest
# Erstelle ein Coverage-Objekt
cov = coverage.Coverage()
def run_tests():
    # Starte die Messung der Codeabdeckung
    cov.start()
    # Führe die Tests aus
    suite = unittest.defaultTestLoader.discover(start_dir=".", pattern="test_main*.py")
    runner = unittest.TextTestRunner()
    runner.run(suite)
    # Beende die Messung der Codeabdeckung
    cov.stop()
    # Generiere den Coverage-Bericht
    cov.report()
if __name__ == "__main__":
    run_tests()
