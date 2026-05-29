import sys
import os
import pytest
import json
from unittest.mock import patch, mock_open

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import viewMyTour


def makeTours(pseudo, tours):
    return [{"pseudo": pseudo, "tours": tours}]


TOUR_1 = {
    "id": 1,
    "distance": 340,
    "visibility": "public",
    "villes": ["Paris", "London"]
}
TOUR_2 = {
    "id": 2,
    "distance": 880,
    "visibility": "private",
    "villes": ["Paris", "Berlin", "Warsaw"]
}


class TestViewMyTours:

    def testFileNotFoundPrintsNoTours(self, capsys):
        with patch("connexion.login.currentUser", "alice"), \
             patch("builtins.open", side_effect=FileNotFoundError):
            viewMyTour.viewMyTours()
        assert "No tours found" in capsys.readouterr().out

    def testUserNotInFilePrintsNoTours(self, capsys):
        data = makeTours("bob", [TOUR_1])
        with patch("connexion.login.currentUser", "alice"), \
             patch("builtins.open", mock_open(read_data=json.dumps(data))):
            viewMyTour.viewMyTours()
        assert "no tours" in capsys.readouterr().out

    def testUserWithNoToursPrintsEmpty(self, capsys):
        data = makeTours("alice", [])
        with patch("connexion.login.currentUser", "alice"), \
             patch("builtins.open", mock_open(read_data=json.dumps(data))):
            viewMyTour.viewMyTours()
        assert "no tours" in capsys.readouterr().out

    def testPrintsTourInfo(self, capsys):
        data = makeTours("alice", [TOUR_1])
        with patch("connexion.login.currentUser", "alice"), \
             patch("builtins.open", mock_open(read_data=json.dumps(data))):
            viewMyTour.viewMyTours()
        out = capsys.readouterr().out
        assert "340" in out
        assert "public" in out

    def testPrintsCityPath(self, capsys):
        data = makeTours("alice", [TOUR_1])
        with patch("connexion.login.currentUser", "alice"), \
             patch("builtins.open", mock_open(read_data=json.dumps(data))):
            viewMyTour.viewMyTours()
        assert "Paris" in capsys.readouterr().out

    def testPrintsMultipleTours(self, capsys):
        data = makeTours("alice", [TOUR_1, TOUR_2])
        with patch("connexion.login.currentUser", "alice"), \
             patch("builtins.open", mock_open(read_data=json.dumps(data))):
            viewMyTour.viewMyTours()
        out = capsys.readouterr().out
        assert "340" in out
        assert "880" in out

    def testDoesNotShowOtherUsersTours(self, capsys):
        data = [
            {"pseudo": "alice", "tours": [TOUR_1]},
            {"pseudo": "bob",   "tours": [TOUR_2]},
        ]
        with patch("connexion.login.currentUser", "alice"), \
             patch("builtins.open", mock_open(read_data=json.dumps(data))):
            viewMyTour.viewMyTours()
        out = capsys.readouterr().out
        assert "340" in out
        assert "880" not in out
