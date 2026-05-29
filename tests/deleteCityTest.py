import sys
import os
import pytest
import json
from unittest.mock import patch, mock_open

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gestion import deleteCity


def makeData():
    return [
        {"pseudo": "alice", "villes": [{"nom": "Paris"}, {"nom": "Lyon"}]},
        {"pseudo": "bob",   "villes": [{"nom": "Berlin"}]},
    ]


class TestDeleteCity:

    def testDeletesCityFromList(self):
        data = makeData()
        with patch("builtins.input", return_value="Paris"), \
             patch("connexion.login.currentUser", "alice"), \
             patch("builtins.open", mock_open(read_data=json.dumps(data))), \
             patch("json.dump") as mock_dump:
            deleteCity.deleteCity()
        saved = mock_dump.call_args[0][0]
        alice = next(u for u in saved if u["pseudo"] == "alice")
        assert not any(v["nom"] == "Paris" for v in alice["villes"])

    def testKeepsOtherCitiesOfUser(self):
        data = makeData()
        with patch("builtins.input", return_value="Paris"), \
             patch("connexion.login.currentUser", "alice"), \
             patch("builtins.open", mock_open(read_data=json.dumps(data))), \
             patch("json.dump") as mock_dump:
            deleteCity.deleteCity()
        saved = mock_dump.call_args[0][0]
        alice = next(u for u in saved if u["pseudo"] == "alice")
        assert any(v["nom"] == "Lyon" for v in alice["villes"])

    def testCaseInsensitiveDelete(self):
        data = makeData()
        with patch("builtins.input", return_value="paris"), \
             patch("connexion.login.currentUser", "alice"), \
             patch("builtins.open", mock_open(read_data=json.dumps(data))), \
             patch("json.dump") as mock_dump:
            deleteCity.deleteCity()
        saved = mock_dump.call_args[0][0]
        alice = next(u for u in saved if u["pseudo"] == "alice")
        assert not any(v["nom"] == "Paris" for v in alice["villes"])

    def testPrintsSuccessMessage(self, capsys):
        data = makeData()
        with patch("builtins.input", return_value="Paris"), \
             patch("connexion.login.currentUser", "alice"), \
             patch("builtins.open", mock_open(read_data=json.dumps(data))), \
             patch("json.dump"):
            deleteCity.deleteCity()
        assert "delete" in capsys.readouterr().out

    def testCityNotFoundPrintsError(self, capsys):
        data = makeData()
        with patch("builtins.input", return_value="Tokyo"), \
             patch("connexion.login.currentUser", "alice"), \
             patch("builtins.open", mock_open(read_data=json.dumps(data))), \
             patch("json.dump"):
            deleteCity.deleteCity()
        assert "not found" in capsys.readouterr().out

    def testDoesNotAffectOtherUsers(self):
        data = makeData()
        with patch("builtins.input", return_value="Berlin"), \
             patch("connexion.login.currentUser", "alice"), \
             patch("builtins.open", mock_open(read_data=json.dumps(data))), \
             patch("json.dump") as mock_dump:
            deleteCity.deleteCity()
        saved = mock_dump.call_args[0][0]
        bob = next(u for u in saved if u["pseudo"] == "bob")
        assert any(v["nom"] == "Berlin" for v in bob["villes"])
