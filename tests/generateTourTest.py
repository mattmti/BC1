import sys
import os
import pytest
from unittest.mock import patch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ittineraire import generateTour


PARIS  = ["Paris",  48.8566,  2.3522]
LONDON = ["London", 51.5074, -0.1278]
BERLIN = ["Berlin", 52.5200, 13.4050]
MADRID = ["Madrid", 40.4168, -3.7038]


class TestDistanceBetween2Cities:

    def testSameCityIsZero(self):
        result = generateTour.distanceBetween2cities(PARIS, PARIS)
        assert result == pytest.approx(0, abs=1)

    def testParisToLondonApprox340km(self):
        result = generateTour.distanceBetween2cities(PARIS, LONDON)
        assert result == pytest.approx(340, abs=20)

    def testIsSymmetric(self):
        d1 = generateTour.distanceBetween2cities(PARIS, LONDON)
        d2 = generateTour.distanceBetween2cities(LONDON, PARIS)
        assert d1 == pytest.approx(d2, rel=1e-6)

    def testParisToMadridGreaterThanParisToLondon(self):
        dLondon = generateTour.distanceBetween2cities(PARIS, LONDON)
        dMadrid = generateTour.distanceBetween2cities(PARIS, MADRID)
        assert dMadrid > dLondon


class TestNearestNeighbor:

    def testFindsNearestCity(self):
        nn, _ = generateTour.nearestNeighbor(PARIS, [LONDON, BERLIN, MADRID], ["Paris"])
        assert nn == LONDON

    def testSkipsVisitedCity(self):
        nn, _ = generateTour.nearestNeighbor(PARIS, [LONDON, BERLIN, MADRID], ["Paris", "London"])
        assert nn == BERLIN

    def testReturnsCorrectDistance(self):
        _, dist = generateTour.nearestNeighbor(PARIS, [LONDON], ["Paris"])
        expected = generateTour.distanceBetween2cities(PARIS, LONDON)
        assert dist == pytest.approx(expected, rel=1e-6)

    def testAllVisitedReturnsEmpty(self):
        nn, _ = generateTour.nearestNeighbor(PARIS, [LONDON], ["Paris", "London"])
        assert nn == ""


class TestNearestNeighborPath:

    def testPrintsAllCities(self, capsys):
        generateTour.nearestNeighborPath(PARIS, [PARIS, LONDON, BERLIN])
        out = capsys.readouterr().out
        assert "Paris" in out
        assert "London" in out
        assert "Berlin" in out

    def testPrintsTotalDistance(self, capsys):
        generateTour.nearestNeighborPath(PARIS, [PARIS, LONDON])
        assert "Distance totale" in capsys.readouterr().out

    def testStartsAndEndsAtStartCity(self, capsys):
        generateTour.nearestNeighborPath(PARIS, [PARIS, LONDON, BERLIN])
        lines = [l for l in capsys.readouterr().out.strip().splitlines() if l]
        assert lines[0] == "Paris"
        assert lines[-2] == "Paris"


class TestLoadCitiesInFiles:

    def testUserNotFoundPrintsError(self, capsys):
        data = [{"pseudo": "bob", "villes": []}]
        with patch("ittineraire.generateTour.loadCities", return_value=data):
            generateTour.loadCitiesInFiles("alice")
        assert "not found" in capsys.readouterr().out

    def testNotEnoughCitiesPrintsError(self, capsys):
        data = [{"pseudo": "alice", "villes": [
            {"nom": "Paris", "lat": 48.8566, "long": 2.3522}
        ]}]
        with patch("ittineraire.generateTour.loadCities", return_value=data):
            generateTour.loadCitiesInFiles("alice")
        assert "Not enough" in capsys.readouterr().out

    def testCallsNearestNeighborPath(self):
        data = [{"pseudo": "alice", "villes": [
            {"nom": "Paris",  "lat": 48.8566, "long":  2.3522},
            {"nom": "London", "lat": 51.5074, "long": -0.1278},
        ]}]
        with patch("ittineraire.generateTour.loadCities", return_value=data), \
             patch("ittineraire.generateTour.nearestNeighborPath") as mock_path:
            generateTour.loadCitiesInFiles("alice")
        mock_path.assert_called_once()

    def testEmptyVillesListPrintsError(self, capsys):
        data = [{"pseudo": "alice", "villes": []}]
        with patch("ittineraire.generateTour.loadCities", return_value=data):
            generateTour.loadCitiesInFiles("alice")
        assert "Not enough" in capsys.readouterr().out
