import sys
import os
import pytest
import json
from unittest.mock import patch, mock_open

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from connexion import login


class TestHashPassword:

    def testReturnsDifferentString(self):
        assert login.hashPassword("secret") != "secret"

    def testReturnsDifferentHashEachTime(self):
        h1 = login.hashPassword("secret")
        h2 = login.hashPassword("secret")
        assert h1 != h2


class TestCheckPassword:

    def testCorrectPasswordReturnsTrue(self):
        hashed = login.hashPassword("secret")
        assert login.checkPassword("secret", hashed) is True

    def testWrongPasswordReturnsFalse(self):
        hashed = login.hashPassword("secret")
        assert login.checkPassword("wrong", hashed) is False

    def testEmptyPasswordReturnsFalse(self):
        hashed = login.hashPassword("secret")
        assert login.checkPassword("", hashed) is False


class TestLoadAndSave:

    def testLoadFillsUsersFromJson(self):
        fake_users = [{"pseudo": "alice", "password": "hash"}]
        m = mock_open(read_data=json.dumps(fake_users))
        with patch("builtins.open", m):
            login.load()
        assert login.users == fake_users

    def testLoadCreatesEmptyListWhenFileNotFound(self):
        with patch("builtins.open", side_effect=FileNotFoundError):
            login.load()
        assert login.users == []

    def testSaveWritesUsersToJson(self):
        login.users = [{"pseudo": "alice", "password": "hash"}]
        m = mock_open()
        with patch("builtins.open", m):
            login.save()
        handle = m()
        written = "".join(call.args[0] for call in handle.write.call_args_list)
        assert json.loads(written) == login.users


class TestCreateAccount:

    def testCreatesNewUser(self):
        login.users = []
        with patch("builtins.input", side_effect=["alice", "secret"]), \
             patch("connexion.login.load"), \
             patch("connexion.login.save"):
            login.createAccount()
        assert any(u["pseudo"] == "alice" for u in login.users)

    def testPasswordIsHashed(self):
        login.users = []
        with patch("builtins.input", side_effect=["alice", "secret"]), \
             patch("connexion.login.load"), \
             patch("connexion.login.save"):
            login.createAccount()
        stored = next(u for u in login.users if u["pseudo"] == "alice")
        assert stored["password"] != "secret"

    def testCallsSave(self):
        login.users = []
        with patch("builtins.input", side_effect=["alice", "secret"]), \
             patch("connexion.login.load"), \
             patch("connexion.login.save") as mock_save:
            login.createAccount()
        mock_save.assert_called_once()


class TestLogin:

    def testSuccessfulLoginSetsCurrentUser(self):
        hashed = login.hashPassword("secret")
        login.users = [{"pseudo": "alice", "password": hashed}]
        with patch("builtins.input", side_effect=["yes", "alice", "secret"]), \
             patch("connexion.login.load"):
            login.login()
        assert login.currentUser == "alice"

    def testWrongPasswordPrintsError(self, capsys):
        hashed = login.hashPassword("secret")
        login.users = [{"pseudo": "alice", "password": hashed}]
        with patch("builtins.input", side_effect=["yes", "alice", "wrong", "alice", "secret"]), \
             patch("connexion.login.load"):
            login.login()
        assert "Invalid" in capsys.readouterr().out

    def testNoAccountRedirectsToCreateAccount(self):
        with patch("builtins.input", side_effect=["no", "bob", "pass"]), \
             patch("connexion.login.load"), \
             patch("connexion.login.createAccount") as mock_create:
            login.login()
        mock_create.assert_called_once()

    def testInvalidAnswerPrintsError(self, capsys):
        with patch("builtins.input", side_effect=["maybe", "no", "bob", "pass"]), \
             patch("connexion.login.load"), \
             patch("connexion.login.createAccount"):
            login.login()
        assert "yes or no" in capsys.readouterr().out
