import sys
import os
import pytest
import json
from unittest.mock import patch, mock_open

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gestion import deleteAll


def makeCities(*pseudos):
    return [{"pseudo": p, "villes": [{"nom": "Paris"}, {"nom": "Lyon"}]} for p in pseudos]


class TestDeleteEveryCity:

    def testDeletesCitiesForCurrentUser(self, capsys):
        data = makeCities("alice", "bob")
        with patch("connexion.login.currentUser", "alice"), \
             patch("builtins.open", mock_open(read_data=json.dumps(data))), \
             patch("json.dump") as mock_dump:
            deleteAll.DeleteEveryCity()
        saved = mock_dump.call_args[0][0]
        alice = next(u for u in saved if u["pseudo"] == "alice")
        assert alice["villes"] == []

    def testDoesNotAffectOtherUsers(self):
        data = makeCities("alice", "bob")
        with patch("connexion.login.currentUser", "alice"), \
             patch("builtins.open", mock_open(read_data=json.dumps(data))), \
             patch("json.dump") as mock_dump:
            deleteAll.DeleteEveryCity()
        saved = mock_dump.call_args[0][0]
        bob = next(u for u in saved if u["pseudo"] == "bob")
        assert bob["villes"] == [{"nom": "Paris"}, {"nom": "Lyon"}]

    def testPrintsConfirmationMessage(self, capsys):
        data = makeCities("alice")
        with patch("connexion.login.currentUser", "alice"), \
             patch("builtins.open", mock_open(read_data=json.dumps(data))), \
             patch("json.dump"):
            deleteAll.DeleteEveryCity()
        assert "alice" in capsys.readouterr().out

    def testPrintsErrorWhenUserNotFound(self, capsys):
        data = makeCities("bob")
        with patch("connexion.login.currentUser", "alice"), \
             patch("builtins.open", mock_open(read_data=json.dumps(data))), \
             patch("json.dump") as mock_dump:
            deleteAll.DeleteEveryCity()
        assert "introuvable" in capsys.readouterr().out
        mock_dump.assert_not_called()

    def testDoesNotSaveWhenUserNotFound(self):
        data = makeCities("bob")
        with patch("connexion.login.currentUser", "alice"), \
             patch("builtins.open", mock_open(read_data=json.dumps(data))), \
             patch("json.dump") as mock_dump:
            deleteAll.DeleteEveryCity()
        mock_dump.assert_not_called()

    def testEmptyUserListPrintsError(self, capsys):
        with patch("connexion.login.currentUser", "alice"), \
             patch("builtins.open", mock_open(read_data=json.dumps([]))), \
             patch("json.dump"):
            deleteAll.DeleteEveryCity()
        assert "introuvable" in capsys.readouterr().out
