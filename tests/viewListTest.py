import sys
import os
import pytest
import json
from unittest.mock import patch, mock_open

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gestion import viewList


def makeData(pseudo, villes):
    return [{"pseudo": pseudo, "villes": villes}]


class TestViewList:

    def testFileNotFoundPrintsNoCities(self, capsys):
        with patch("connexion.login.currentUser", "alice"), \
             patch("builtins.open", side_effect=FileNotFoundError):
            viewList.viewList()
        assert "No cities found" in capsys.readouterr().out

    def testUserNotInFilePrintsNoCities(self, capsys):
        data = makeData("bob", [{"nom": "Paris"}])
        with patch("connexion.login.currentUser", "alice"), \
             patch("builtins.open", mock_open(read_data=json.dumps(data))):
            viewList.viewList()
        assert "No cities found" in capsys.readouterr().out

    def testUserWithNoCitiesPrintsEmpty(self, capsys):
        data = makeData("alice", [])
        with patch("connexion.login.currentUser", "alice"), \
             patch("builtins.open", mock_open(read_data=json.dumps(data))):
            viewList.viewList()
        assert "empty" in capsys.readouterr().out

    def testPrintsCityName(self, capsys):
        data = makeData("alice", [{"nom": "Paris"}])
        with patch("connexion.login.currentUser", "alice"), \
             patch("builtins.open", mock_open(read_data=json.dumps(data))):
            viewList.viewList()
        assert "Paris" in capsys.readouterr().out

    def testPrintsAllCities(self, capsys):
        data = makeData("alice", [{"nom": "Paris"}, {"nom": "Lyon"}, {"nom": "Berlin"}])
        with patch("connexion.login.currentUser", "alice"), \
             patch("builtins.open", mock_open(read_data=json.dumps(data))):
            viewList.viewList()
        out = capsys.readouterr().out
        assert "Paris" in out
        assert "Lyon" in out
        assert "Berlin" in out

    def testDoesNotShowOtherUsersCities(self, capsys):
        data = [
            {"pseudo": "alice", "villes": [{"nom": "Paris"}]},
            {"pseudo": "bob",   "villes": [{"nom": "Berlin"}]},
        ]
        with patch("connexion.login.currentUser", "alice"), \
             patch("builtins.open", mock_open(read_data=json.dumps(data))):
            viewList.viewList()
        out = capsys.readouterr().out
        assert "Paris" in out
        assert "Berlin" not in out
